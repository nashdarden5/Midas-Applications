#!/usr/bin/env python3
"""Snapshot-only monitoring; no auction requests or credentials."""
import datetime as dt,json,os,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';STATE=Path(os.getenv('WATCHDOG_STATE_PATH',str(ROOT/'watchdog-state.json')))
NOW=dt.datetime.now(dt.timezone.utc)
def parse(s):
 try:
  t=dt.datetime.fromisoformat(s.replace('Z','+00:00'))
  return t.astimezone(dt.timezone.utc) if t.tzinfo else None
 except (ValueError,TypeError,AttributeError):return None
def source_data(name):
 try:return json.loads((DOCS/name).read_text())
 except (OSError,ValueError):return {}
def extract(title):
 m=re.search(r'\b(19\d{2}|20\d{2})\s+(Ford|Chevrolet|Chevy|Dodge|Jeep|Toyota|Honda|Nissan|Hyundai|Kia|GMC|Ram|Buick|Chrysler)\s+([A-Za-z0-9-]+)',title,re.I)
 return (int(m[1]),m[2].lower().replace('chevy','chevrolet'),m[3].lower()) if m else None
def score(x,comps):
 identity=extract(x.get('title',''));bid=x.get('price');bid=float(bid) if isinstance(bid,(int,float)) and bid>=0 else None
 if not identity or bid is None:return None,None
 sales=[c['price'] for c in comps if isinstance(c.get('price'),(int,float)) and (z:=extract(c.get('title',''))) and z[1:]==identity[1:] and abs(z[0]-identity[0])<=2 and c.get('sold_date')]
 if not sales:return None,None
 sales.sort();resale=sales[len(sales)//2];transport=675;repairs=1800 if re.search(r'non.running|salvage|engine issue|parts only',x.get('title',''),re.I) else 650
 premium=.125 if x.get('source','').startswith('GovDeals') else 0
 profit=round(resale-bid*(1+premium)-resale*.07-transport-repairs)
 ceiling=max(0,(resale*.93-transport-repairs-500)/(1+premium));headroom=max(0,min(20,round((ceiling-bid)/ceiling*40))) if ceiling else 0
 evidence=15 if len(sales)>=3 else 10 if len(sales)==2 else 5
 risk=12 if repairs==650 else 4
 return profit,max(0,min(35,round(profit/3000*35)))+risk+headroom+evidence
def run(state=None,gov=None,gsa=None,sold=None,now=None):
 now=now or NOW;state=state if isinstance(state,dict) else {};previous=state.get('snapshots',{});events=state.get('events',[]);current={};sources=[gov or {},gsa or {}];comps=(sold or {}).get('listings',[])
 if not comps:comps=(sold or {}).get('sales',[])
 for source in sources:
  for x in source.get('listings',[]):
   url=x.get('url','');id=x.get('id','');observed=parse(x.get('observed_at') or source.get('fetched_at'))
   if not id or not url.startswith('https://') or not observed or observed>now+dt.timedelta(minutes=5) or now-observed>dt.timedelta(hours=48):continue
   profit,ranking=score(x,comps);ends=x.get('ends');record={'id':id,'url':url,'title':x.get('title','Unknown'),'source':x.get('source',source.get('source','Unknown')),'observed_at':observed.isoformat(),'bid':x.get('price') if isinstance(x.get('price'),(int,float)) else None,'profit':profit,'score':ranking,'ends':ends}
   old=previous.get(id)
   if old and parse(old.get('observed_at')) and observed>parse(old['observed_at']):
    for key,label in [('bid','Reported bid'),('profit','Illustrative modeled profit'),('score','Server Deal Score')]:
     if old.get(key) is not None and record[key] is not None and old[key]!=record[key]:events.append({'type':key,'id':id,'title':record['title'],'message':f'{label}: {old[key]} → {record[key]}','observed_at':record['observed_at'],'detected_at':now.isoformat(),'source':record['source']})
   current[id]=record
 # Compare relative ranks only among listings with comparable evidence.
 ranked=sorted((v for v in current.values() if v['score'] is not None),key=lambda v:(-v['score'],v['id']))
 for i,v in enumerate(ranked):
  v['rank']=i+1;old=previous.get(v['id'])
  if old and old.get('rank') and old['rank']!=v['rank'] and parse(old.get('observed_at')) and parse(v['observed_at'])>parse(old['observed_at']):events.append({'type':'rank','id':v['id'],'title':v['title'],'message':f'Server Deal Score position: #{old["rank"]} → #{v["rank"]}','observed_at':v['observed_at'],'detected_at':now.isoformat(),'source':v['source']})
 for id,v in current.items():
  ending=parse(v.get('ends'))
  if not ending:continue
  hours=(ending-now).total_seconds()/3600
  if not 0<hours<=24:continue
  window='1h' if hours<=1 else '24h';key=f'{id}|{ending.isoformat()}|{window}'
  if key not in state.get('closing_alerts',[]):events.append({'type':'closing','id':id,'title':v['title'],'message':f'Reported closing within {window}','observed_at':v['observed_at'],'detected_at':now.isoformat(),'source':v['source']});state.setdefault('closing_alerts',[]).append(key)
 # Preserve last good snapshots for missing feed items, without treating them as fresh.
 previous.update(current);state['snapshots']=dict(list(previous.items())[-1000:]);state['events']=events[-500:];state['closing_alerts']=state.get('closing_alerts',[])[-1000:];state['checked_at']=now.isoformat()
 return state
if __name__=='__main__':
 old=json.loads(STATE.read_text()) if STATE.exists() else {}
 new=run(old,source_data('govdeals-vehicles.json'),source_data('gsa-vehicles.json'),source_data('verified-sold-comps.json'))
 STATE.parent.mkdir(parents=True,exist_ok=True);STATE.write_text(json.dumps(new,separators=(',',':'))+'\n')
 public={'checked_at':new['checked_at'],'events':new['events'][-100:],'coverage':'Published source snapshots only; no official GovDeals live verification','notification':'Public activity feed; no email or push configured'}
 (DOCS/'watchdog-activity.json').write_text(json.dumps(public,separators=(',',':'))+'\n')
 print('Watchdog snapshots:',len(new['snapshots']),'events:',len(new['events']))
