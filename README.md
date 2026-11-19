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
