"""Build the same-origin IGCSE PDF library from hash-verified public archives."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse, hashlib, json, time, urllib.request

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
MANIFEST = DIST / 'data/igcse-online-files.json'

def valid(path, entry):
    return path.is_file() and path.stat().st_size == entry['bytes'] and hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256']

def obtain(entry):
    path = DIST / entry['path']
    assert path.parent == DIST / 'assets/igcse'
    if valid(path, entry):
        return 'cached'
    path.parent.mkdir(parents=True, exist_ok=True)
    last = None
    for attempt in range(4):
        try:
            request = urllib.request.Request(entry['url'], headers={'User-Agent': 'Pure-Practice-IGCSE-PDF-Build/1.0'})
            with urllib.request.urlopen(request, timeout=90) as response:
                content = response.read()
            if len(content) != entry['bytes'] or hashlib.sha256(content).hexdigest() != entry['sha256']:
                raise ValueError('PDF/archive does not match the verified source bytes')
            signature = b'%PDF-' if entry['filename'].endswith('.pdf') else b'PK'
            if not content.startswith(signature):
                raise ValueError('Unexpected PDF/archive signature')
            temporary = path.with_suffix(path.suffix + '.part')
            temporary.write_bytes(content)
            temporary.replace(path)
            return 'downloaded'
        except Exception as error:
            last = error
            if attempt < 3:
                time.sleep(2 ** attempt)
    raise RuntimeError(entry['filename'] + ': ' + str(last))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--subject', choices=['physics', 'cs'])
    parser.add_argument('--types', nargs='+', choices=['qp', 'ms', 'er', 'gt', 'ci', 'pm'])
    args = parser.parse_args()
    entries = json.loads(MANIFEST.read_text())['files']
    if args.subject:
        entries = [entry for entry in entries if entry['subject'] == args.subject]
    if args.types:
        entries = [entry for entry in entries if entry['type'] in args.types]
    failures = []
    if args.verify_only:
        failures = [entry['filename'] for entry in entries if not valid(DIST / entry['path'], entry)]
    else:
        with ThreadPoolExecutor(max_workers=8) as pool:
            jobs = {pool.submit(obtain, entry): entry for entry in entries}
            for count, future in enumerate(as_completed(jobs), 1):
                try:
                    future.result()
                except Exception as error:
                    failures.append(str(error))
                if count % 50 == 0 or count == len(entries):
                    print(f'IGCSE resources checked: {count}/{len(entries)}', flush=True)
    if failures:
        raise SystemExit('Cannot publish an incomplete IGCSE PDF library:\n' + '\n'.join(failures))
    size = sum(path.stat().st_size for path in DIST.rglob('*') if path.is_file())
    if size >= 950 * 1024 * 1024:
        raise SystemExit(f'Published static site is too large: {size} bytes')
    print(f'PASS: {len(entries)} source files, exact SHA-256; static site {size / 1024 / 1024:.1f} MiB')

if __name__ == '__main__':
    main()
