#!/usr/bin/env python3
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'docs'
gov=json.loads((root/'govdeals-vehicles.json').read_text());sold=json.loads((root/'verified-sold-comps.json').read_text())
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
