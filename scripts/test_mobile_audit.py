from pathlib import Path
r=Path(__file__).resolve().parents[1];h=(r/'docs/index.html').read_text();c=(r/'docs/dashboard.css').read_text();j=(r/'docs/dashboard.js').read_text();sw=(r/'docs/sw.js').read_text()
assert 'Used cars. Questionable history. Unbeatable prices.' in h
for id in ['view-discover','view-browser','view-saved','view-add','view-help','auction-detail-dialog','resale-dialog','bid-dialog','watchdog-events','top-deals-list']:
 assert f'id="{id}"' in h,id
for selector in ['.resale-dialog{max-width:calc(100vw - 16px)', '.watchdog-events{max-height:52dvh', '.comparison-scroll{overscroll-behavior-x:contain}', '.top-deal-card .watchlist-actions button{min-height:44px}', '.field input,.field select,.field textarea', '@media(max-width:390px)', '.nav button{min-width:0']:
 assert selector in c,selector
for token in ['function renderTopDeals()', 'function renderWatchdog()', 'function renderAlertSettings()']:
 assert token in j,token
assert 'blakeypoo-shell-v42-1' in sw
print('Mobile usability layout contracts, navigation, dialogs, saved auctions, Watchdog, slogan PASS')
