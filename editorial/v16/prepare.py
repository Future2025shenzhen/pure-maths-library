"""One idempotent release entry point; do not let legacy layers overwrite V16."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
bank=json.loads((ROOT/'dist/data/bank.json').read_text())
if bank.get('version',0)<16:
 subprocess.run(['npm','run','prepare:v15'],cwd=ROOT,check=True)
for script in ('build_content.py','figures.py','apply.py'):
 subprocess.run([sys.executable,str(Path(__file__).parent/script)],cwd=ROOT,check=True)
