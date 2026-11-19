import datetime as dt
from server_watchdog import run
now=dt.datetime.now(dt.timezone.utc)
def record(bid,when):return {'source':'GSA Auctions official API','fetched_at':when.isoformat(),'listings':[{'id':'fixture','url':'https://www.gsaauctions.gov/auctions/preview/123','title':'2015 Ford F350','source':'GSA Auctions official API','price':bid,'ends':(now+dt.timedelta(hours=20)).isoformat()}]}
sold={'listings':[{'title':'2015 Ford F350','price':14000,'sold_date':'2026-11-18'}]}
a=run({},record(4000,now-dt.timedelta(hours=2)),{},sold,now);assert len(a['snapshots'])==1
b=run(a,record(4500,now-dt.timedelta(hours=1)),{},sold,now);assert any(e['type']=='bid' for e in b['events'])
assert any(e['type']=='profit' for e in b['events'])
assert any(e['type']=='closing' for e in b['events'])
c=run(b,record(4500,now-dt.timedelta(hours=1)),{},sold,now);assert len(c['events'])==len(b['events'])
d=run(c,record(4700,now-dt.timedelta(days=3)),{},sold,now);assert len(d['events'])==len(c['events'])
print('Server Watchdog state, change detection, deduplication and stale-data tests PASS')
