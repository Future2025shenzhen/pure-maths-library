"""Turn the seven source-pinned CS pre-release ZIPs into seven readable PDFs.

The original ZIP bytes are downloaded and SHA-256-checked by prepare-igcse-pdfs.py
before this runs. Each ZIP contains a main pre-release PDF and NOTICE PDF.
The published PDF has the main paper first, then the NOTICE as an appendix.
Only the generated build manifest is edited, not the committed source manifest.
"""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
from hashlib import sha256
import json

from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MANIFEST = DIST / "data/igcse-online-files.json"

def convert(entry):
    old_filename = entry["filename"]
    source = DIST / entry["path"]
    expected_hash = entry["sha256"]
    original_bytes = source.read_bytes()
    if sha256(original_bytes).hexdigest() != expected_hash:
        raise ValueError("Source ZIP hash mismatch: " + old_filename)
    with ZipFile(BytesIO(original_bytes)) as archive:
        members = [m for m in archive.infolist() if not m.is_dir()]
        if len(members) != 2 or any(not m.filename.lower().endswith(".pdf") for m in members):
            raise ValueError("Unexpected ZIP contents, cannot safely convert: " + old_filename)
        if archive.testzip() is not None:
            raise ValueError("Source ZIP member CRC mismatch: " + old_filename)
        notice = [m for m in members if "NOTICE" in m.filename.upper()]
        main = [m for m in members if "NOTICE" not in m.filename.upper()]
        if len(notice) != 1 or len(main) != 1:
            raise ValueError("Cannot distinguish main PDF and NOTICE: " + old_filename)
        ordered = main + notice
        writer = PdfWriter()
        pages_by_part = []
        for member in ordered:
            raw = archive.read(member)
            if not raw.startswith(b"%PDF-"):
                raise ValueError("Invalid embedded PDF: " + member.filename)
            reader = PdfReader(BytesIO(raw), strict=False)
            if reader.is_encrypted or len(reader.pages) == 0:
                raise ValueError("Encrypted or empty embedded PDF: " + member.filename)
            pages_by_part.append(len(reader.pages))
            writer.append(reader)
        writer.add_metadata({
            "/Title": old_filename.replace(".zip", "") + " - Pre-release Materials and Notice",
            "/Subject": "Combined Cambridge IGCSE Computer Science pre-release package",
            "/Creator": "Pure Practice: original PDFs merged without rewriting their page content"
        })
        out_filename = old_filename[:-4] + ".pdf"
        target = source.with_suffix(".pdf")
        with target.open("wb") as output:
            writer.write(output)
        result = target.read_bytes()
        expected_pages = sum(pages_by_part)
        if not result.startswith(b"%PDF-") or len(PdfReader(BytesIO(result)).pages) != expected_pages:
            target.unlink(missing_ok=True)
            raise ValueError("Converted PDF failed page-count validation: " + old_filename)
    # Only delete the ZIP from the *published artifact*. The original source,
    # pinned URL, size and SHA are preserved in committed manifest for rebuilds.
    source.unlink()
    entry.update({
        "filename": out_filename,
        "path": "assets/igcse/" + out_filename,
        "bytes": len(result),
        "sha256": sha256(result).hexdigest(),
        "pages": expected_pages,
        "sourceArchiveFilename": old_filename,
        "sourceArchiveSha256": expected_hash,
        "conversion": "merged-original-PDFs-main-then-notice",
        "sourceArchiveUrl": entry["url"],
        "includedPdfParts": [
            {"name": member.filename, "pages": count}
            for member, count in zip(ordered, pages_by_part)
        ]
    })
    print("CONVERTED " + old_filename + " -> " + out_filename +
          " | pages=" + str(expected_pages) +
          " (" + "+".join(map(str,pages_by_part)) + ")", flush=True)
    return out_filename

def main():
    catalog=json.loads(MANIFEST.read_text())
    files=catalog["files"]
    archives=[entry for entry in files if entry["filename"].endswith(".zip")]
    if len(archives) != 7:
        raise SystemExit("Expected exactly 7 source ZIP archives, got "+str(len(archives)))
    output=[convert(entry) for entry in archives]
    filenames=[entry["filename"] for entry in files]
    if len(filenames)!=len(set(filenames)):
        raise SystemExit("Duplicate output filenames")
    if any(not entry["filename"].endswith(".pdf") for entry in files):
        raise SystemExit("Archive conversion incomplete")
    catalog["derivedPdfPackages"] = {
        "count": len(output),
        "files": output,
        "note": "Source ZIPs contained a main PDF and a NOTICE PDF. PDFs were merged, not renamed."
    }
    MANIFEST.write_text(json.dumps(catalog, ensure_ascii=False, indent=2)+"\n")
    print("PASS: 7 ZIP packages converted into 7 page-checked PDFs; "+
          str(len(files))+" site-readable PDF resources.", flush=True)

if __name__ == "__main__":
    main()
