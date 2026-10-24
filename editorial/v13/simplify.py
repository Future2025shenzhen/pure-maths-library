"""Apply reviewed withdrawals deterministically before tests and publication."""
import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
path = ROOT/'dist/data/bank.json'
bank = json.loads(path.read_text())
manifest = json.loads((ROOT/'editorial/v13/withdrawals.json').read_text())
records = {r['id']: r for r in manifest['records']}
def digest(q):
    return hashlib.sha256(json.dumps(q, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
seen = set()
for q in bank['questions']:
    if q['id'] not in records:
        continue
    r = records[q['id']]
    assert digest(q) in (r['beforeHash'], r['afterHash']), q['id']+' changed since review'
    q['withdrawn'] = True
    q['withdrawalReason'] = r['reason']
    assert digest(q) == r['afterHash'], q['id']
    seen.add(q['id'])
assert seen == set(records) and len(seen) == 6
assert len(bank['questions']) == 770
assert sum(not q.get('withdrawn') for q in bank['questions']) == 753
path.write_text(json.dumps(bank, ensure_ascii=False, indent=2)+'\n')
assert hashlib.sha256(path.read_bytes()).hexdigest() == 'a64e3e5755082fb985bbf6ea207c26cd66869bf4d36fbdb43b2843bad8918797'
print('PASS deterministic V13 bank: 753 active; 770 historical IDs preserved.')
