from pathlib import Path
root=Path(__file__).resolve().parents[1];js=(root/'docs/dashboard.js').read_text();css=(root/'docs/dashboard.css').read_text();sw=(root/'docs/sw.js').read_text()
for token in ['top-deal-media','validPhoto','img.loading=\'lazy\'','img.decoding=\'async\'','Photo unavailable','No listing photo','top-deal-source','webassets\\.lqdt1','auction-images']:
 assert token in js,token
for token in ['.top-deal-media img','.top-deal-no-photo','.top-deal-card:nth-child(3n+2)','.top-deal-card:nth-child(3n)','.top-deal-source','.metric:nth-child(1)','.watchdog-panel','.deal-winner-panel']:
 assert token in css,token
assert 'blakeypoo-shell-v42' in sw
print('Top Deals image fallback, approved sources, section colors, responsive styles and cache version PASS')
