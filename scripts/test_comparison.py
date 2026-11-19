from pathlib import Path
root=Path(__file__).resolve().parents[1];js=(root/'docs/dashboard.js').read_text();css=(root/'docs/dashboard.css').read_text();html=(root/'docs/index.html').read_text()
for token in ['function comparisonSelection()','function toggleComparison(url)','function comparisonData(item)','function renderComparison()','renderComparison()}','comparisonSelection().includes(x.url)','showNativeAuction(vehicle)','comparison-clear']:
 assert token in js,token
for metric in ['Current reported bid','Estimated resale','Expected net profit','Expected max bid','Risk score','Auction freshness','Sold comparison confidence']:
 assert metric in js,metric
assert 'slice(0,4)' in js and 'selected.length<4' in js
assert 'comparison-scroll' in css and 'overflow-x:auto' in css and 'position:sticky' in css
assert 'id="comparison-table"' in html and 'id="comparison-status"' in html
print('Vehicle comparison selection, metrics, responsive table and controls PASS')
