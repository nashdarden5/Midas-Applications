from pathlib import Path
root=Path(__file__).resolve().parents[1];html=(root/'docs/index.html').read_text();css=(root/'docs/dashboard.css').read_text();js=(root/'docs/dashboard.js').read_text();sw=(root/'docs/sw.js').read_text()
for view in ['discover','browser','saved','add','help']:
 assert f'data-nav="{view}"' in html
 assert f'id="view-{view}"' in html
for identifier in ['metric-total','metric-watch','metric-profit','vehicle-carousel','top-deals-list','watchdog-events','deal-winner-list']:
 assert f'id="{identifier}"' in html,identifier
for name in ['hero-tagline','overview-heading','metric-icon','nav-icon']:
 assert name in html and f'.{name}' in css,name
for token in ['.nav button[aria-current=page]','@media(max-width:600px)','@media(max-width:390px)','@media(prefers-reduced-motion:reduce)','.top-deal-card:hover','.watchdog-event','.deal-winner-card','.feed-health-item']:
 assert token in css,token
assert 'blakeypoo-shell-v42-1' in sw
assert "function renderTopDeals()" in js
print('Dashboard navigation, view IDs, metric bindings, responsive layout, visual hierarchy and reduced motion PASS')
