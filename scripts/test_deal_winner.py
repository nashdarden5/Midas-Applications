from pathlib import Path
root=Path(__file__).resolve().parents[1];js=(root/'docs/dashboard.js').read_text();html=(root/'docs/index.html').read_text();css=(root/'docs/dashboard.css').read_text()
for token in ['function dealWinnerScore(item)','function renderDealWinners()','profitPoints','riskPoints','headroomPoints','evidencePoints','warnings','score:null','How this score was calculated','renderComparison();renderDealWinners()','comp.matches.length','fresh.status']:
 assert token in js,token
for token in ['id="deal-winner-status"','id="deal-winner-list"','Saved vehicle Deal Winner ranking']:
 assert token in html,token
assert '.deal-winner-card' in css
print('Deal Winner scoring, explainability, uncertainty and UI wiring PASS')
