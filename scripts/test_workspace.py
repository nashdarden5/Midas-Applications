from pathlib import Path
root=Path(__file__).resolve().parents[1];js=(root/'docs/dashboard.js').read_text();css=(root/'docs/dashboard.css').read_text();html=(root/'docs/index.html').read_text()
for part in ['workspaceComps(x)','workspaceProfit(x)','workspaceCeilings(x)','riskScoreElement(x)','workspaceNotes(x)','nativeDetailFields(x)']:
 assert part in js,part
assert 'function showNativeAuction(x)' in js and '🔎 Research workspace' in js
assert 'comps.slice(0,8)' in js and 'median(comps.map(c=>c.price))' in js
assert "$('auction-detail-dialog').close();openResale(x)" in js
assert '#auction-detail-dialog' in css and 'max-height:95dvh' in css
assert 'Unified vehicle research workspace' in html
print('Unified workspace composition, mobile layout and modal handoff PASS')
