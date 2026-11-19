#!/usr/bin/env python3
"""Explicitly configured SMTP delivery of source-backed saved-auction events."""
import datetime as dt,hashlib,json,os,re,smtplib,ssl
from email.message import EmailMessage
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STATE=Path(os.getenv('WATCHDOG_EMAIL_STATE_PATH',str(ROOT/'watchdog-email-state.json')))
def iso(s):
 try:
  t=dt.datetime.fromisoformat(s.replace('Z','+00:00'));return t.astimezone(dt.timezone.utc) if t.tzinfo else None
 except (ValueError,AttributeError,TypeError):return None
def eligible(events,ids,seen,now):
 output=[]
 for e in events:
  observed=iso(e.get('observed_at'));detected=iso(e.get('detected_at'))
  if e.get('id') not in ids or not observed or not detected:continue
  if not (dt.timedelta(0)<=now-observed<=dt.timedelta(hours=48) and dt.timedelta(0)<=now-detected<=dt.timedelta(hours=48)):continue
  key=hashlib.sha256(json.dumps([e.get('id'),e.get('type'),e.get('observed_at'),e.get('message')],separators=(',',':')).encode()).hexdigest()
  if key not in seen:output.append((key,e))
 return output
def main():
 if os.getenv('BLAKEYPOO_EMAIL_ENABLED','').lower()!='true':print('Email delivery disabled (opt-in required)');return
 ids=set(json.loads(os.getenv('BLAKEYPOO_EMAIL_WATCH_IDS','[]')))
 ids={x for x in ids if isinstance(x,str) and re.fullmatch(r'[A-Za-z0-9:_-]{1,100}',x)}
 if not ids:print('No explicitly selected auction IDs; no email sent');return
 opted_in=iso(os.getenv('BLAKEYPOO_EMAIL_OPTED_IN_AT'))
 if not opted_in:raise ValueError('Explicit BLAKEYPOO_EMAIL_OPTED_IN_AT timestamp required')
 host=os.environ['BLAKEYPOO_SMTP_HOST'];port=int(os.environ.get('BLAKEYPOO_SMTP_PORT','465'))
 user=os.environ['BLAKEYPOO_SMTP_USER'];password=os.environ['BLAKEYPOO_SMTP_PASSWORD'];recipient=os.environ['BLAKEYPOO_EMAIL_TO'];sender=os.environ['BLAKEYPOO_EMAIL_FROM']
 if not 1<=port<=65535 or not recipient or not sender:raise ValueError('Invalid mail configuration')
 now=dt.datetime.now(dt.timezone.utc);activity=json.loads((ROOT/'docs/watchdog-activity.json').read_text());state=json.loads(STATE.read_text()) if STATE.exists() else {'seen':[]}
 seen=set(state.get('seen',[]));pending=[(key,e) for key,e in eligible(activity.get('events',[]),ids,seen,now) if iso(e['detected_at'])>opted_in]
 if not pending:print('No new fresh selected-auction events');return
 msg=EmailMessage();msg['Subject']=f'BlakeyPoo: {len(pending)} saved auction alert(s)';msg['From']=sender;msg['To']=recipient
 lines=['Selected auction changes from published source snapshots (not live auction verification).','']
 for _,e in pending:lines.extend([f"{e.get('title','Auction')}: {e.get('message','Change')}",f"Source observed: {e['observed_at']}; detected: {e['detected_at']}",f"Source: {e.get('source','Unknown')}",''])
 lines.append('Verify current bid, terms and closing time with the official auction before acting.')
 msg.set_content('\n'.join(lines))
 if os.getenv('BLAKEYPOO_EMAIL_DRY_RUN','').lower()=='true':print('DRY RUN: would send',len(pending),'selected events; no email sent');return
 context=ssl.create_default_context()
 with smtplib.SMTP_SSL(host,port,context=context,timeout=20) as smtp:
  smtp.login(user,password);smtp.send_message(msg)
 # Only mark delivered after SMTP acceptance. Failed deliveries are retried on next run.
 state['seen']=list(seen.union(key for key,_ in pending))[-2000:];state['last_sent_at']=now.isoformat();STATE.write_text(json.dumps(state,separators=(',',':'))+'\n')
 print('SMTP accepted',len(pending),'selected-auction alerts')
if __name__=='__main__':main()
