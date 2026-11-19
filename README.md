# Midas Applications 📱

Public, shareable applications built by Project Midas. **The Midas automation engine and private development repository are not included.**

## Applications

| App | Description | Source | Build |
| --- | --- | --- | --- |
| **BlakeyPoo** | SwiftUI iPhone browser for GovDeals | [Source](apps/BlakeyPoo/) | [iOS CI / downloadable unsigned device IPA](.github/workflows/blakeypoo-ios.yml) |

### Installing BlakeyPoo on an iPhone using Windows
After a successful GitHub Actions build, download the **BlakeyPoo-unsigned-iPhone-IPA** artifact, extract its ZIP, and sign/install the IPA locally with a free Apple ID using [Sideloadly](https://sideloadly.io/). See [BlakeyPoo instructions](apps/BlakeyPoo/README.md).

An unsigned IPA is **not** directly installable. Simulator builds are not iPhone installers.

### Publishing policy
Only app source, app tests, and public build workflows belong here. Private Midas infrastructure, credentials, internal endpoints, logs, handoff, and development history stay in the private Midas repository. New shareable apps get their own `apps/<AppName>/` directory.

## BlakeyPoo web app (recommended for friends)

The no-signing, installable web companion lives in [`docs/`](docs/) and is deployed via [GitHub Pages](.github/workflows/blakeypoo-pages.yml) at **https://nashdarden5.github.io/Midas-Applications/** once GitHub Pages is enabled in repository Settings → Pages → Build and deployment → GitHub Actions. Open the URL in Safari and choose Share → Add to Home Screen. This avoids Sideloadly and developer provisioning. The web app now uses the agreed 1024×1024 BlakeyPoo icon from the private iOS app assets, resized for PWA use. GovDeals opens directly in a browser tab because third-party embedding is unreliable; no automated bidding or account access is provided. Saved auction shortcuts are stored locally on the device.

## BlakeyPoo 2.0 dashboard
The public PWA now includes Discover (opens official GovDeals for real inventory), a local saved-listings dashboard with title/notes search, category and status filters, sorting, a form to save GovDeals URLs with user-entered estimated purchase/fees/resale, and estimated upside totals. Old URL shortcuts are migrated automatically on the same browser. All data is local to each browser; it is **not** a real-time GovDeals feed, cross-device sync, verified market-price service, or bidding system. Approved BlakeyPoo icon remains fixed in the top-right corner of all in-app sections. External GovDeals pages cannot display our icon. `node tests-blakeypoo.cjs` runs security, estimate and migration checks.

### Nearby passenger-vehicle swipe carousel
The Explore page now shows real active **GSA Auctions** vehicle candidates via the official federal GSA Auctions API. A GitHub Pages deployment job refreshes a public, read-only `gsa-vehicles.json` snapshot every six hours. Source photos, latest reported high bid, end date and official listing URL are displayed in a swipeable carousel. A visitor can grant browser location permission to filter by **100 miles**, using GeoNames ZIP centroids (approximate, not street-level). Visitor location stays on device; no coordinates are sent to our server. Results may be empty in areas with no matching federal auctions. GSA feed does **not** cover GovDeals or all auctions, and listing status/prices may change between updates. The app keeps the original approved BlakeyPoo icon and URL. For reliable unattended refresh, configure a personal `GSA_API_KEY` repository secret from api.data.gov; until then the workflow uses the official limited `DEMO_KEY`. Do not expose private keys in client-side JavaScript. GeoNames ZIP data: https://download.geonames.org/export/zip/US.zip (CC BY 4.0).

### GovDeals browsing and transitions
The Browse tab attempts to show the official GovDeals site in an iframe and always provides an Open official GovDeals button for Safari. GovDeals may prohibit iframe embedding using CSP/X-Frame-Options or other security restrictions; BlakeyPoo does not bypass those restrictions, proxy credentials, or impersonate GovDeals. The approved original portrait/gear icon is enlarged to 118px (96px on narrow iPhones), fixed top-left. Navigation uses a brief icon-centered loading overlay that dismisses on the next rendered frame, not an artificial wait. The embedded GovDeals view is not guaranteed to function and must be tested on iPhone.

### Ending-soon and location filters (v10)
The home carousel defaults to **all nationwide active GSA passenger-vehicle candidates, ending soon first** (ascending closing date), without requiring location permission. Optional **Location within** selector: Anywhere, 25, 50, 100, 250 or 500 miles, using ZIP-centroid approximate distances and browser geolocation only when a radius is selected. The GovDeals search button opens the real GovDeals website where its own native location filters can be used; no unverified GovDeals preset URLs or undocumented GovDeals APIs are used. BlakeyPoo does not currently index all GovDeals passenger vehicles. GSA closing timestamps in the current public feed contain dates only, so same-day ordering cannot be guaranteed.

### Real listing photographs and bid cards (v11)
The nationwide ending-soon carousel uses actual current GSA Auctions API records and now snapshots their official public listing photographs as optimized local JPEGs during each six-hour data refresh. Each swipe card prominently displays the auction photograph, item title, **reported current high bid** (not a final sale price), city/state, auction end date, and a link directly to the specific official auction. The photo snapshot is necessary because the GSA image endpoint responds as `application/octet-stream`, which can be unreliable in some mobile browsers. No fictitious photos, listings or prices are generated. This is still a GSA-only feed, not GovDeals inventory; the GovDeals Browse tab links to its official site.
