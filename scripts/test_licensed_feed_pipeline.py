import datetime as dt,json,tempfile
from pathlib import Path
from licensed_feed_pipeline import validate,ingest
now=dt.datetime.now(dt.timezone.utc);stamp=now.isoformat()
base={'license_authorized':True,'provider':'Fixture','license_reference':'fixture-only','listings':[{'id':'govdeals:257-26703','source_url':'https://licensed.example/asset/1','observed_at':stamp,'fields':{'vin':'1HGCM82633A004352','condition':'unknown'}}]}
assert validate(base,now)==1
for altered in [{**base,'license_authorized':False},{**base,'listings':[dict(base['listings'][0],observed_at=(now-dt.timedelta(days=3)).isoformat())]},{**base,'listings':[dict(base['listings'][0],fields={'unapproved':'x'})]},{**base,'listings':[dict(base['listings'][0],source_url='http://unsafe.example')]}]:
 try:validate(altered,now)
 except ValueError:pass
 else:raise AssertionError('Invalid payload accepted')
with tempfile.TemporaryDirectory() as d:
 feed=Path(d)/'feed.json';status=Path(d)/'status.json';feed.write_text(json.dumps({'listings':[{'id':'govdeals:257-26703','title':'Fixture vehicle','details':{}}]}))
 result=ingest(base,feed,status)
 assert result['imported_fields']==2 and json.loads(feed.read_text())['listings'][0]['details']['vin']['verification']=='licensed_provider'
 before=feed.read_text()
 try:ingest({**base,'listings':[]},feed,status)
 except ValueError:pass
 else:raise AssertionError('Empty overwrite accepted')
 assert feed.read_text()==before
print('Licensed feed validation, stale protection and atomic import PASS')
