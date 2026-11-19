# BlakeyPoo changelog

2026-11-19: Confirmed project independence from Project Midas; no Midas handoff or changelog edits going forward. Existing public URL retained.
2026-11-19: Added 2-second full-screen startup splash with original icon rotating 360 degrees, fixed large upper-left icon while scrolling, and preserved verified GSA auction photos, reported bids, and direct listing URLs. Service worker v12.
2026-11-19: Fixed GSA photo refresh reliability: GitHub Actions was denied by the GSA image CDN (HTTP 403) and erased all photos in the generated feed. Retain previously verified local official photos across refreshes; no placeholder photos. Commit 03271d5.
2026-11-19: Added Resale Analysis modal for every live GSA vehicle. Green bottom-right star shows saved estimated profit or Analyze if not yet calculated. Calculates purchase cost, shipping/transport, buyer premium %, other costs and user-entered resale value. Persists each estimate locally, avoids invented premium/shipping/resale values. Added seven calculation edge-case tests. Service worker v13.
