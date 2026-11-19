#!/usr/bin/env python3
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'docs'
gov=json.loads((root/'govdeals-vehicles.json').read_text());sold=json.loads((root/'verified-sold-comps.json').read_text())
assert gov['refresh_status'] in ('ok','partial','failed') and gov['last_attempt_at']
assert sold['refresh_status'] in ('ok','partial','failed') and sold['last_attempt_at']
assert gov['count']==len(gov['listings']) and gov['count']>0
assert len({x['url'] for x in gov['listings']})==gov['count']
for x in gov['listings']:
 assert re.fullmatch(r'https://www\.govdeals\.com/asset/\d+/\d+',x['url'])
 assert x['source'].startswith('GovDeals') and x['title'] and (x['price'] is None or x['price']>=0)
 assert not x['image'] or x['image'].startswith(('https://files.lqdt1.com/photos/','https://webassets.lqdt1.com/assets/photos/'))
assert sold['listings'] and len({x['url'] for x in sold['listings']})==len(sold['listings'])
for x in sold['listings']:
 assert x['verified'] is True and x['price']>=0 and re.fullmatch(r'\d{4}-\d{2}-\d{2}',x['sold_date'])
 assert x['url'].startswith(('https://uxsearch.app/sold/','https://govauctions.app/auction/'))
print('Market feed validation PASS:',gov['count'],'GovDeals auctions,',len(sold['listings']),'sold comparisons')

# Cross-check derived GovDeals links against the original source-page seller/asset identifiers.
for x in gov['listings']:
 if x.get('source_page','').startswith('https://govauctions.app/'):
  import re
  m=re.search(r'-govdeals-(\d+)-(\d+)$',x['source_page'])
  assert m and x['url']==f'https://www.govdeals.com/asset/{m.group(2)}/{m.group(1)}'
print('Official-link derivation PASS:',sum(x.get('source_page','').startswith('https://govauctions.app/') for x in gov['listings']),'source-backed GovDeals links')

for x in gov['listings']:
 for key,field in x.get('details',{}).items():
  assert key in {'seller','county','category','closing_text','first_seen','description','vin','mileage','condition','terms'}
  assert field['value'] and field['source_url'].startswith('https://uxsearch.app/auction/')
  assert field['verification']=='third_party_observed' and field['observed_at']
print('Native detail provenance PASS:',sum(bool(x.get('details')) for x in gov['listings']),'enriched GovDeals records')
