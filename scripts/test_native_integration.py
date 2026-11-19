from pathlib import Path
s=(Path(__file__).resolve().parents[1]/'docs/dashboard.js').read_text()
assert 'feedHealth.gsa=payload' in s
assert 'feedHealth.licensed=await r.json()' in s
assert 'Licensed GovDeals details' in s
assert 'Source observation:' in s
assert 'user_supplied_unverified' in s
assert 'licensed_provider' in (Path(__file__).resolve().parents[1]/'scripts/import_licensed_govdeals.py').read_text()
print('Native feed status and provenance integration PASS')
