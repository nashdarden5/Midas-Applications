# BlakeyPoo

SwiftUI iOS wrapper for https://www.govdeals.com. This uses the official website in WKWebView, not an official GovDeals API.

## What is verified
- macOS GitHub Actions simulator build and XCTest app-launch/Home smoke test: successful, private Midas CI run 44280094950 (public repo CI must verify independently).
- Downloadable simulator artifact: `BlakeyPoo-iOS-simulator` on that run, subject to GitHub artifact retention.

## What remains unverified
- GovDeals search, sign-in, saved items, bidding, payments, and other account functionality inside WKWebView.
- Signed IPA installation on a real iPhone. Apple signing credentials and provisioning profile are required.
- Website terms and App Store distribution requirements.

## Build
`xcodegen generate` then `xcodebuild -project BlakeyPoo.xcodeproj -scheme BlakeyPoo -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO build`.

CI: https://github.com/nashdarden5/Midas-Applications/actions/workflows/blakeypoo-ios.yml

## Windows + free Apple ID installation route

The macOS CI workflow compiles a separate **iPhoneOS arm64** build and packages an **unsigned IPA**.
The simulator ZIP is not usable on a real iPhone. The unsigned IPA must be signed for the specific iPhone before installation.

1. Download the `BlakeyPoo-unsigned-iPhone-IPA` artifact from a successful GitHub Actions run and extract its ZIP to obtain `BlakeyPoo-unsigned-device.ipa`.
2. On Windows, install Sideloadly from https://sideloadly.io/ and its official Apple iTunes/iCloud prerequisites as documented there.
3. Connect your iPhone over USB, unlock it, and select **Trust This Computer**.
4. Drag the IPA into Sideloadly, select the phone, and sign/install using your own free Apple ID **locally**. Do not send credentials to Midas or store them in GitHub.
5. On the iPhone, enable Developer Mode if required and trust the developer profile under Settings > General > VPN & Device Management.
6. Launch BlakeyPoo and manually verify site search, sign-in and navigation. Do not assume bidding or payment workflows work until tested.

Free Apple ID provisioning lasts around **7 days**; Sideloadly supports refreshing with a connected or Wi-Fi-paired Windows PC. This is personal device testing, not public App Store distribution.

Sideloadly is third-party software; use its official website and review its security/privacy implications before supplying your Apple ID.
