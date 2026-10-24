"""Inspect the original seven 0478 ZIP materials without modifying their contents."""
from pathlib import Path
from zipfile import ZipFile
from collections import Counter
import json
root=Path(__file__).resolve().parents[1]
items=json.loads((root/'dist/data/igcse-online-files.json').read_text())['files']
for item in items:
    if not item['filename'].endswith('.zip'):continue
    path=root/'dist'/item['path']
    with ZipFile(path) as z:
        files=[i for i in z.infolist() if not i.is_dir()]
        print('ZIP '+item['filename']+' members='+str(len(files))+' total_uncompressed='+str(sum(x.file_size for x in files)),flush=True)
        for f in files[:45]:
            print('  '+f.filename+' size='+str(f.file_size),flush=True)
        if len(files)>45:print('  ... '+str(len(files)-45)+' more',flush=True)
