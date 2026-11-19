import json
from pathlib import Path
from urllib.parse import urlparse
feed=json.loads(Path('docs/gsa-vehicles.json').read_text())
assert isinstance(feed['listings'],list)
assert feed['count']==len(feed['listings'])
assert feed['fetched_at']
for x in feed['listings']:
 assert -90<=x['lat']<=90 and -180<=x['lon']<=180
 assert urlparse(x['url']).hostname=='www.gsaauctions.gov'
 assert x['source']=='GSA Auctions'
 assert x['image'].startswith('./auction-images/') if x['image'] else True
 if x['image']:
  photo=Path('docs')/x['image'][2:]
  assert photo.is_file() and photo.stat().st_size>1000
 assert x['title']
 assert x['price'] is None or x['price']>=0
print('GSA live feed schema/security checks PASS:',feed['count'],'vehicle listings')
