#!/usr/bin/env python3
"""Public UX Search GovDeals listing discovery; never fabricate auction fields."""
import datetime as dt,json,re,urllib.request,urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'/'govdeals-vehicles.json'
BASE='https://uxsearch.app'
SECONDARY='https://govauctions.app/auctions/vehicles'
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'BlakeyPoo/1.0 public auction research'})
 with urllib.request.urlopen(req,timeout=25) as response:return BeautifulSoup(response.read(),'html.parser')
def main():
 items=[];errors=[];sources=[]
 try:
  page=fetch(BASE+'/platforms/govdeals?category=vehicles')
  for card in page.select('a.v2-lot[data-cat="vehicles"][href^="/auction/"]')[:30]:
   title=card.select_one('.v2-lot-title');where=card.select_one('.v2-lot-where');closing=card.select_one('[data-closes]');photo=card.select_one('img[src]')
   if not title or not where:continue
   raw=card.get('data-p','');price=float(raw) if re.fullmatch(r'\d+(?:\.\d+)?',raw) else None
   try:
    detail=fetch(BASE+card['href']);link=next((a['href'] for a in detail.select('a[href]') if re.fullmatch(r'https://www\.govdeals\.com/asset/\d+/\d+',a['href'])),None)
   except Exception:continue
   if not link or any(x['url']==link for x in items):continue
   image=photo.get('src','') if photo else ''
   if not image.startswith('https://webassets.lqdt1.com/'):image=''
   loc=where.get_text(' ',strip=True);parts=loc.rsplit(',',1)
   items.append({'id':'govdeals:'+link.rsplit('/',2)[-2]+'-'+link.rsplit('/',1)[-1], 'title':title.get_text(' ',strip=True)[:180], 'url':link,'image':image,'price':price,'ends':closing.get('data-closes','') if closing else '', 'city':parts[0].strip(),'state':parts[1].strip() if len(parts)>1 else '', 'source':'GovDeals via UX Search','lat':None,'lon':None})
 except Exception as exc:errors.append('UX Search: '+str(exc)[:120]);print('GovDeals discovery unavailable:',exc)
 # Additional GovDeals listings from a separate public government-auction aggregator.
 # Its slug encodes the original GovDeals seller and asset IDs; use only strict numeric matches.
 try:
  page=fetch(SECONDARY)
  for card in page.select('a.listing-link[href*="-govdeals-"]'):
   match=re.search(r'-govdeals-(\d+)-(\d+)$',card.get('href',''))
   heading=card.select_one('h3')
   if not match or not heading:continue
   seller,asset=match.groups();link=f'https://www.govdeals.com/asset/{asset}/{seller}'
   if any(x['url']==link for x in items):continue
   content=card.get_text(' ',strip=True)
   price_match=re.search(r'\$([\d,]+(?:\.\d{2})?)',content)
   price=float(price_match.group(1).replace(',','')) if price_match else None
   photo=card.select_one('img[src]');image=''
   if photo:
    raw=photo.get('src','');parsed=urllib.parse.urlparse(raw)
    if parsed.path=='/api/image':
     source=urllib.parse.parse_qs(parsed.query).get('url',[''])[0]
     if source.startswith('https://files.lqdt1.com/photos/'):image=source
   location=re.search(r'\b([A-Za-z .-]+),\s*([A-Z]{2})\b',content)
   items.append({'id':'govdeals:'+asset+'-'+seller,'title':heading.get_text(' ',strip=True)[:180], 'url':link,'image':image,'price':price,'ends':'','city':location.group(1)[-80:].strip() if location else '', 'state':location.group(2) if location else '', 'source':'GovDeals via GovAuctions.app','lat':None,'lon':None,'source_page':'https://govauctions.app'+card['href']})
 except Exception as exc:errors.append('GovAuctions.app: '+str(exc)[:120]);print('Secondary GovDeals discovery unavailable:',exc)
 if not items and OUT.exists():
  old=json.loads(OUT.read_text());old['last_attempt_at']=dt.datetime.now(dt.timezone.utc).isoformat();old['refresh_status']='failed';old['refresh_errors']=errors or ['No listings returned from discovery sources'];OUT.write_text(json.dumps(old,separators=(',',':'))+'\n');print('Keeping previous GovDeals feed; upstream unavailable');return
 OUT.write_text(json.dumps({'source':'GovDeals public listings via UX Search','fetched_at':dt.datetime.now(dt.timezone.utc).isoformat(),'count':len(items),'last_attempt_at':dt.datetime.now(dt.timezone.utc).isoformat(),'refresh_status':'partial' if errors else 'ok','refresh_errors':errors,'listings':items},separators=(',',':'))+'\n')
 print('GovDeals listings',len(items))
if __name__=='__main__':main()
