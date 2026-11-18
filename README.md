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
