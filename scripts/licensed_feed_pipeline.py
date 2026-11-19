#!/usr/bin/env python3
"""Opt-in, credential-protected ingestion of a contract-authorized provider JSON feed."""
import datetime as dt,json,os,re,urllib.parse,urllib.request
from pathlib import Path
from import_licensed_govdeals import merge
ROOT=Path(__file__).resolve().parents[1]
FEED=ROOT/'docs/govdeals-vehicles.json'
STATUS=ROOT/'docs/licensed-feed-status.json'

def validate(payload,now=None):
 now=now or dt.datetime.now(dt.timezone.utc)
 if not isinstance(payload,dict) or payload.get('license_authorized') is not True:raise ValueError('License attestation missing')
 if not all(isinstance(payload.get(k),str) and payload[k].strip() for k in ('provider','license_reference')):raise ValueError('Provider/license missing')
 if not isinstance(payload.get('listings'),list) or len(payload['listings'])>5000:raise ValueError('Invalid listing count')
 ids=set()
 for lot in payload['listings']:
  if not isinstance(lot,dict) or not re.fullmatch(r'govdeals:\d+-\d+',str(lot.get('id',''))):raise ValueError('Invalid listing id')
  if lot['id'] in ids:raise ValueError('Duplicate listing')
  ids.add(lot['id'])
  u=urllib.parse.urlsplit(lot.get('source_url',''))
  if u.scheme!='https' or not u.hostname or u.username or u.password:raise ValueError('Invalid provenance URL')
  try:
   observed=dt.datetime.fromisoformat(lot['observed_at'].replace('Z','+00:00'))
   if observed.tzinfo is None:raise ValueError('Timestamp requires timezone')
   observed=observed.astimezone(dt.timezone.utc)
   if observed>now+dt.timedelta(minutes=5) or now-observed>dt.timedelta(hours=48):raise ValueError('Stale/future record')
  except (KeyError,AttributeError):raise ValueError('Missing observation timestamp')
  fields=lot.get('fields')
  if not isinstance(fields,dict) or not fields:raise ValueError('Missing fields')
  for k,v in fields.items():
   if k not in {'vin','mileage','condition','description','seller','terms','photos','closing_text'} or not isinstance(v,str) or not v.strip() or len(v)>3000:raise ValueError('Invalid field')
 return len(ids)

def ingest(payload,feed=FEED,status=STATUS):
 count=validate(payload);current=json.loads(feed.read_text());updated=json.loads(json.dumps(current));n=merge(updated,payload)
 if n<1:raise ValueError('No matching licensed records')
 result={'status':'ok','provider':payload['provider'],'listing_count':count,'imported_fields':n,'checked_at':dt.datetime.now(dt.timezone.utc).isoformat()}
 tmp=feed.with_suffix('.tmp');tmp.write_text(json.dumps(updated,separators=(',',':'))+'\n');tmp.replace(feed)
 status.write_text(json.dumps(result,separators=(',',':'))+'\n');return result

def main():
 if os.getenv('BLAKEYPOO_LICENSED_FEED_ENABLED')!='true':print('Licensed feed disabled; preserved existing listings');return
 url=os.getenv('BLAKEYPOO_LICENSED_FEED_URL','');host=os.getenv('BLAKEYPOO_LICENSED_FEED_HOST','');parsed=urllib.parse.urlsplit(url)
 if parsed.scheme!='https' or not host or parsed.hostname!=host or parsed.username or parsed.password:raise ValueError('Provider URL/host configuration invalid')
 token=os.getenv('BLAKEYPOO_LICENSED_FEED_TOKEN','')
 if not token:raise ValueError('Provider token missing')
 class NoRedirect(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,*args,**kwargs):raise ValueError('Provider redirects are disabled')
 opener=urllib.request.build_opener(NoRedirect())
 request=urllib.request.Request(url,headers={'Authorization':'Bearer '+token,'Accept':'application/json'})
 with opener.open(request,timeout=20) as response:
  raw=response.read(2_000_001)
  if len(raw)>2_000_000:raise ValueError('Provider response too large')
 result=ingest(json.loads(raw));print('Licensed feed imported:',result['imported_fields'],'fields')
if __name__=='__main__':main()
