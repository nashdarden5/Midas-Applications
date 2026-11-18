import SwiftUI
import WebKit

struct AuctionBrowser: View {
    @State private var page = URL(string: "https://www.govdeals.com")!
    @State private var showHome = false
    var body: some View {
        NavigationStack {
            OfficialAuctionWebView(url: page)
                .navigationTitle("BlakeyPoo")
                .navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .topBarLeading) {
                        Button("GovDeals Home") { page = URL(string: "https://www.govdeals.com")!; showHome.toggle() }
                    }
                }
                .id(showHome)
        }
    }
}

struct OfficialAuctionWebView: UIViewRepresentable {
    let url: URL
    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.websiteDataStore = .default()
        let view = WKWebView(frame: .zero, configuration: config)
        view.allowsBackForwardNavigationGestures = true
        view.load(URLRequest(url: url))
        return view
    }
    func updateUIView(_ uiView: WKWebView, context: Context) {}
}
