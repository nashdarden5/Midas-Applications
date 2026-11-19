#!/usr/bin/env python3
"""Refresh documented sold-auction records from public UX Search sale pages."""
import concurrent.futures,datetime as dt,json,re,urllib.parse,urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs'/'verified-sold-comps.json'
HEADERS={'User-Agent':'BlakeyPoo/1.0 (public completed-auction price research)'}
MODEL=re.compile(r'\b(19\d{2}|20\d{2})\s+(Ford|Chevrolet|Chevy|Dodge|Jeep|Toyota|Honda|Nissan|Hyundai|Kia|GMC|Ram|Buick|Chrysler)\s+([A-Za-z0-9-]+)',re.I)
def fetch(url):
 req=urllib.request.Request(url,headers=HEADERS)
 with urllib.request.urlopen(req,timeout=18) as r:return BeautifulSoup(r.read(650000),'html.parser')
def identity(title):
 m=MODEL.search(title);return (m.group(1),m.group(2).lower().replace('chevy','chevrolet'),re.sub('[^a-z0-9]','',m.group(3).lower())) if m else None
def sold_detail(url):
 try:
  s=fetch(url);title=s.title.get_text(' ',strip=True) if s.title else ''
  m=re.search(r'(.+?)\s+Sold for\s+\$([\d,]+(?:\.\d{2})?)',title,re.I)
  body=s.get_text(' ',strip=True)
  date=re.search(r'Sale closed\s+([A-Za-z]+\s+\d{1,2},\s+20\d{2})',body)
  if not m or not date or not identity(m.group(1)):return None
  sold_date=dt.datetime.strptime(date.group(1),'%B %d, %Y').date()
  if sold_date>dt.datetime.now(dt.timezone.utc).date():return None
  return {'title':m.group(1).strip()[:180],'price':float(m.group(2).replace(',','')),'sold_date':sold_date.isoformat(),'url':url,'verified':True,'notes':'Completed public auction; verify mileage, trim and condition on source page'}
 except Exception as exc:print('Sold detail unavailable:',url,str(exc)[:65]);return None
def main():
 rows=json.loads((ROOT/'docs'/'gsa-vehicles.json').read_text())['listings']+json.loads((ROOT/'docs'/'govdeals-vehicles.json').read_text())['listings']
 keys=list(dict.fromkeys(identity(x['title']) for x in rows if identity(x['title'])))
 # Search specific year/make/model, plus selected high-frequency passenger models.
 queries=[' '.join(k) for k in keys[:42]]
 urls=set()
 def search(q):
  try:
   s=fetch('https://uxsearch.app/search?q='+urllib.parse.quote(q));return [a['href'] for a in s.select('a[href*="/sold/"]') if re.fullmatch(r'https://uxsearch\.app/sold/[a-z0-9-]+',a.get('href',''))][:6]
  except Exception:return []
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
  for result in pool.map(search,queries):urls.update(result)
 old=[]
 try:old=json.loads(OUT.read_text()).get('listings',[])
 except Exception:pass
 by_url={x['url']:x for x in old if x.get('verified') is True and x.get('url','').startswith(('https://uxsearch.app/sold/','https://govauctions.app/auction/'))}
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  for row in pool.map(sold_detail,sorted(urls)[:125]):
   if row:by_url[row['url']]=row
 if not by_url:raise RuntimeError('No verified sold records; refusing to replace previous feed')
 entries=sorted(by_url.values(),key=lambda x:x['sold_date'],reverse=True)[:350]
 OUT.write_text(json.dumps({'refresh_status':'ok' if urls else 'partial','refresh_errors':[] if urls else ['No new completed-sale search results; retained previously verified records'],'last_attempt_at':dt.datetime.now(dt.timezone.utc).isoformat(),'source':'UX Search public completed-auction pages + previously verified GovAuctions.app records','fetched_at':dt.datetime.now(dt.timezone.utc).isoformat(),'count':len(entries),'listings':entries},separators=(',',':'))+'\n')
 print('Sold comps:',len(entries),'unique search terms:',len(queries),'candidate pages:',len(urls))
if __name__=='__main__':main()
