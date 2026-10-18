"""Copy the existing public website once; verify every file before publication."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import time
import urllib.request
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "scripts/migration-manifest.json").read_text())
DEST = ROOT / "dist"

def copy_file(entry):
    relative = Path(entry["path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Unsafe manifest path")
    target = DEST / relative
    def matches():
        return target.is_file() and target.stat().st_size == entry["bytes"] and hashlib.sha256(target.read_bytes()).hexdigest() == entry["sha256"]
    if matches():
        return
    url = MANIFEST["origin"] + "/" + urllib.parse.quote(relative.as_posix())
    last_error = None
    for attempt in range(4):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "PureMathsLibrary-Migration/1.0"})
            with urllib.request.urlopen(request, timeout=90) as response:
                body = response.read(entry["bytes"] + 1)
            if len(body) != entry["bytes"] or hashlib.sha256(body).hexdigest() != entry["sha256"]:
                raise ValueError("Website file does not match recorded checksum: " + str(relative))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            return
        except Exception as error:
            last_error = error
            time.sleep(attempt + 1)
    raise RuntimeError("Unable to import " + str(relative)) from last_error

with ThreadPoolExecutor(max_workers=6) as pool:
    list(pool.map(copy_file, MANIFEST["files"]))
(DEST / ".nojekyll").touch()
print("Verified", len(MANIFEST["files"]), "local website files.")
