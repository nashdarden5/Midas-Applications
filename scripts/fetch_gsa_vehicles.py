#!/usr/bin/env python3
"""Build public, read-only GSA vehicle feed from official GSA API and GeoNames US ZIP centroids."""
import datetime as dt
import io
import json
import os
import re
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'gsa-vehicles.json'
GSA = 'https://api.gsa.gov/assets/gsaauctions/v2/auctions?format=JSON&api_key='
GEONAMES = 'https://download.geonames.org/export/zip/US.zip'
PATTERN = re.compile(r'\b(?:sedan|coupe|hatchback|station wagon|crossover|suv|sport utility|passenger (?:car|van|vehicle)|minivan|automobile|pickup(?: truck)?|crew cab|cab pickup|jeep|ford (?:escape|explorer|focus|fusion|taurus|edge|expedition|mustang|f150|f-150)|chevrolet (?:impala|malibu|tahoe|suburban|silverado|equinox)|toyota (?:camry|corolla|rav4|prius|tacoma)|honda (?:civic|accord|cr-v)|dodge (?:charger|challenger|caravan)|nissan (?:altima|sentra|rogue)|hyundai (?:elantra|sonata|tucson))\b', re.I)
EXCLUDE = re.compile(r'\b(?:parts only|engine only|transmission only|tires only|forklift|tractor|fire truck|ambulance|school bus|dump truck|semi truck|trailer|golf cart|atv|utv|motorcycle|snowmobile|toy|model car)\b', re.I)

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'BlakeyPoo/1.0 (public GSA auctions feed)'})
    with urllib.request.urlopen(req, timeout=35) as resp:
        return resp.read()

def zip_coords():
    raw = get(GEONAMES)
    result = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        with archive.open('US.txt') as fh:
            for line in fh:
                cols = line.decode('utf-8').rstrip('\n').split('\t')
                if len(cols) >= 11 and re.fullmatch(r'\d{5}', cols[1]):
                    try:result[cols[1]] = (float(cols[9]), float(cols[10]))
                    except ValueError:pass
    return result

def main():
    key = (os.environ.get('GSA_API_KEY') or 'DEMO_KEY')
    rows = json.loads(get(GSA + key)).get('Results', [])
    if not isinstance(rows, list):raise RuntimeError('GSA API returned unexpected shape')
    coords = zip_coords()
    listings = []
    for x in rows:
        title = str(x.get('itemName') or '').strip()
        if not PATTERN.search(title) or EXCLUDE.search(title):continue
        if str(x.get('auctionStatus') or '').lower() not in ('active','a'):continue
        zip_code = str(x.get('propertyZip') or '')[:5]
        if zip_code not in coords:continue
        link = str(x.get('itemDescURL') or '')
        photo = str(x.get('imageURL') or '')
        if not link.startswith('https://www.gsaauctions.gov/'):continue
        if photo and not photo.startswith(('https://www.ppms.gov/','https://www.gsaauctions.gov/')):photo = ''
        bid = x.get('highBidAmount')
        try:bid = round(float(bid),2) if bid is not None else None
        except (ValueError,TypeError):bid = None
        lat,lon = coords[zip_code]
        listings.append({'id':str(x.get('saleNo') or '')+':'+str(x.get('lotNo') or ''),'title':title[:180], 'url':link,'image':photo,'price':bid,'lat':lat,'lon':lon,'city':str(x.get('propertyCity') or '').strip()[:80],'state':str(x.get('propertyState') or '').strip()[:2], 'zip':zip_code,'ends':str(x.get('aucEndDt') or '')[:10],'source':'GSA Auctions'})
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    payload={'source':'GSA Auctions official API','fetched_at':now,'geolocation_precision':'ZIP code centroid (approximate)','count':len(listings),'listings':listings}
    OUT.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n')
    print('Fetched',len(rows),'GSA lots;',len(listings),'active geocoded passenger vehicle candidates; output',OUT)
if __name__=='__main__':main()
