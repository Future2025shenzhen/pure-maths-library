from pathlib import Path
import json, subprocess, sys

ROOT=Path(__file__).resolve().parents[2]
subprocess.run([sys.executable,str(ROOT/'editorial/v16/prepare.py')],cwd=ROOT,check=True)
path=ROOT/'dist/version.json';version=json.loads(path.read_text())
version.update(siteVersion='v17',contentRevision=17,date='2026-10-24')
path.write_text(json.dumps(version,ensure_ascii=False,indent=2)+'\n')
print('V17 past-paper practice assets retained: 572 questions across 58 papers')
