#!/usr/bin/env python3
"""Opt-in import of contract-authorized GovDeals field records; never fetch GovDeals."""
import argparse,datetime as dt,json,re
from pathlib import Path
FIELDS={'vin','mileage','condition','description','seller','terms','photos','closing_text'}
def merge(feed,licensed):
 if licensed.get('license_authorized') is not True or not licensed.get('provider') or not licensed.get('license_reference'):
  raise ValueError('Written license authorization, provider and license reference required')
 indexed={x['id']:x for x in feed['listings']};added=0
 for record in licensed.get('listings',[]):
  lot=record.get('id');target=indexed.get(lot)
  if not target or not lot.startswith('govdeals:'):continue
  fields=record.get('fields',{});source=record.get('source_url','');stamp=record.get('observed_at','')
  if not re.fullmatch(r'https://[^\s]+',source) or not stamp:continue
  for key,value in fields.items():
   if key not in FIELDS or not isinstance(value,str) or not value.strip():continue
   target.setdefault('details',{})[key]={'value':value.strip()[:3000],'source_url':source,'observed_at':stamp,'verification':'licensed_provider','provider':licensed['provider'],'license_reference':licensed['license_reference']};added+=1
 return added
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('licensed_json',type=Path);ap.add_argument('--feed',type=Path,default=Path(__file__).resolve().parents[1]/'docs/govdeals-vehicles.json');args=ap.parse_args()
 data=json.loads(args.feed.read_text());count=merge(data,json.loads(args.licensed_json.read_text()));args.feed.write_text(json.dumps(data,separators=(',',':'))+'\n');print('Imported licensed fields:',count)
