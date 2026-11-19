#!/usr/bin/env python3
"""Run public feed refreshes and preserve last good data with explicit failures."""
import datetime as dt,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FEEDS=[('GSA Auctions','fetch_gsa_vehicles.py','gsa-vehicles.json'),('GovDeals','fetch_govdeals_vehicles.py','govdeals-vehicles.json'),('Sold comparisons','fetch_sold_comps.py','verified-sold-comps.json')]
def main():
 failures=[]
 for name,script,file in FEEDS:
  dest=ROOT/'docs'/file
  try:
   result=subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,capture_output=True,text=True,timeout=150)
   if result.returncode:raise RuntimeError((result.stderr or result.stdout or 'Unknown error')[-350:])
   data=json.loads(dest.read_text());data.setdefault('refresh_status','ok');data.setdefault('refresh_errors',[])
   data['last_attempt_at']=dt.datetime.now(dt.timezone.utc).isoformat()
   dest.write_text(json.dumps(data,separators=(',',':'))+'\n')
   print(name,data.get('refresh_status'),len(data.get('listings',[])))
  except Exception as exc:
   failures.append(name)
   if dest.exists():
    data=json.loads(dest.read_text());data['refresh_status']='failed';data['refresh_errors']=[str(exc)[:350]];data['last_attempt_at']=dt.datetime.now(dt.timezone.utc).isoformat();dest.write_text(json.dumps(data,separators=(',',':'))+'\n')
   print(name,'FAILED:',str(exc)[:150])
 print('Feed refresh complete; failed:',', '.join(failures) or 'none')
if __name__=='__main__':main()
