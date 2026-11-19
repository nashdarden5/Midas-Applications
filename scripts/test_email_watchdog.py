import datetime as dt,os,subprocess,sys
from email_watchdog import eligible
now=dt.datetime.now(dt.timezone.utc)
e={'id':'govdeals:1-2','title':'Test','type':'bid','observed_at':now.isoformat(),'detected_at':now.isoformat(),'message':'bid increased'}
assert len(eligible([e],{'govdeals:1-2'},set(),now))==1
key=eligible([e],{'govdeals:1-2'},set(),now)[0][0]
assert not eligible([e],{'govdeals:1-2'},{key},now)
assert not eligible([e],{'govdeals:other'},set(),now)
old=dict(e,observed_at=(now-dt.timedelta(days=3)).isoformat());assert not eligible([old],{e['id']},set(),now)
p=subprocess.run([sys.executable,'scripts/email_watchdog.py'],env={**os.environ,'BLAKEYPOO_EMAIL_ENABLED':'false'},capture_output=True,text=True,check=True)
assert 'disabled' in p.stdout
print('Opt-in SMTP guard, saved-auction allowlist, stale rejection and deduplication PASS')
