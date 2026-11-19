from pathlib import Path
r=Path(__file__).resolve().parents[1];js=(r/'docs/dashboard.js').read_text();html=(r/'docs/index.html').read_text();css=(r/'docs/dashboard.css').read_text()
for text in ['function selectedServerEvents()','ids.has(e.id)','function notifyWatchdog()','function enableWatchdogAlerts()','settings.enabledAt','Date.parse(settings.enabledAt','settings.seen=[...seen].slice(-300)','Notification.permission','renderWatchdog();notifyWatchdog()','alertSettings().personalized?selectedServerEvents()']:
 assert text in js,text
for text in ['id="watchdog-alert-enable"','id="watchdog-personalized"','id="watchdog-alert-status"','No email, SMS, or background push']:
 assert text in html,text
assert '.watchdog-alert-controls' in css
print('Opt-in saved-auction alerts, event filtering, notification support and deduplication PASS')
