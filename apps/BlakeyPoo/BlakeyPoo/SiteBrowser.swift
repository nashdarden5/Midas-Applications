import SwiftUI
import WebKit

struct SiteBrowser: View {
    @State private var homeVersion = 0
    var body: some View {
        NavigationStack {
            SiteWebView()
                .id(homeVersion)
                .navigationTitle("BlakeyPoo")
                .navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .topBarLeading) {
                        Button("Home") { homeVersion += 1 }
                    }
                }
        }
    }
}

struct SiteWebView: UIViewRepresentable {
    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.websiteDataStore = .default()
        let web = WKWebView(frame: .zero, configuration: config)
        web.allowsBackForwardNavigationGestures = true
        web.load(URLRequest(url: URL(string: "https://www.govdeals.com")!))
        return web
    }
    func updateUIView(_ uiView: WKWebView, context: Context) {}
}
