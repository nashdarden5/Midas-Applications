from import_licensed_govdeals import merge
base={'listings':[{'id':'govdeals:1-2','details':{}}]}
record={'license_authorized':True,'provider':'Test Provider','license_reference':'test-contract','listings':[{'id':'govdeals:1-2','source_url':'https://provider.example/lot/1','observed_at':'2026-11-19T00:00:00Z','fields':{'vin':'1HGCM82633A004352','condition':'Unknown','bogus':'no'}}]}
assert merge(base,record)==2
assert base['listings'][0]['details']['vin']['verification']=='licensed_provider'
assert 'bogus' not in base['listings'][0]['details']
try:merge(base,{**record,'license_authorized':False})
except ValueError:pass
else:raise AssertionError('Unauthorized import accepted')
print('Licensed provider adapter tests PASS')
