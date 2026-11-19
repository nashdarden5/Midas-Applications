#!/usr/bin/env python3
"""Public UX Search GovDeals listing discovery; never fabricate auction fields."""
import datetime as dt,json,re,urllib.request
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'/'govdeals-vehicles.json'
BASE='https://uxsearch.app'
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'BlakeyPoo/1.0 public auction research'})
 with urllib.request.urlopen(req,timeout=25) as response:return BeautifulSoup(response.read(),'html.parser')
def main():
 items=[]
 try:
  page=fetch(BASE+'/platforms/govdeals')
  for card in page.select('a.v2-lot[data-cat="vehicles"][href^="/auction/"]')[:18]:
   title=card.select_one('.v2-lot-title');where=card.select_one('.v2-lot-where');closing=card.select_one('[data-closes]');photo=card.select_one('img[src]')
   if not title or not where:continue
   raw=card.get('data-p','');price=float(raw) if re.fullmatch(r'\d+(?:\.\d+)?',raw) else None
   try:
    detail=fetch(BASE+card['href']);link=next((a['href'] for a in detail.select('a[href]') if re.fullmatch(r'https://www\.govdeals\.com/asset/\d+/\d+',a['href'])),None)
   except Exception:continue
   if not link:continue
   image=photo.get('src','') if photo else ''
   if not image.startswith('https://webassets.lqdt1.com/'):image=''
   loc=where.get_text(' ',strip=True);parts=loc.rsplit(',',1)
   items.append({'id':'govdeals:'+link.rsplit('/',2)[-2]+'-'+link.rsplit('/',1)[-1], 'title':title.get_text(' ',strip=True)[:180], 'url':link,'image':image,'price':price,'ends':closing.get('data-closes','') if closing else '', 'city':parts[0].strip(),'state':parts[1].strip() if len(parts)>1 else '', 'source':'GovDeals via UX Search','lat':None,'lon':None})
 except Exception as exc:print('GovDeals discovery unavailable:',exc)
 if not items and OUT.exists():
  print('Keeping previous GovDeals feed; upstream unavailable');return
 OUT.write_text(json.dumps({'source':'GovDeals public listings via UX Search','fetched_at':dt.datetime.now(dt.timezone.utc).isoformat(),'count':len(items),'listings':items},separators=(',',':'))+'\n')
 print('GovDeals listings',len(items))
if __name__=='__main__':main()
