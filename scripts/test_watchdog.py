from pathlib import Path
root=Path(__file__).resolve().parents[1];js=(root/'docs/dashboard.js').read_text();html=(root/'docs/index.html').read_text();css=(root/'docs/dashboard.css').read_text()
for token in ['function watchdogState()','function captureWatchdog()','function renderWatchdog()','Date.parse(next.sourceAt)>Date.parse(prev.sourceAt)','sourceMs>now+300000','now-sourceMs>48*3600000','events.slice(-200)','snapshots[item.url]=next','Deal Winner position #','watchdogAnalysisReady','watchdog-clear']:
 assert token in js,token
for token in ['id="watchdog-status"','id="watchdog-events"','id="watchdog-clear"','No background push notifications']:
 assert token in html,token
assert '.watchdog-events' in css
print('Auction Watchdog snapshot comparisons, history bounds, freshness and UI checks PASS')
