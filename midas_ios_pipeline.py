#!/usr/bin/env python3
"""Reusable iOS app build specification, source generation, and static acceptance checks."""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def validate(name,url):
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9]{2,35}',name):raise ValueError('invalid app name')
    from urllib.parse import urlparse
    u=urlparse(url)
    if u.scheme!='https' or not u.hostname or u.username or u.password or u.port or u.fragment:
        raise ValueError('public HTTPS website required')
    return name,url
def generate(name,url,root=ROOT):
    validate(name,url)
    base=root/'apps'/name
    src=base/name
    src.mkdir(parents=True,exist_ok=True)
    (base/'project.yml').write_text(f'''name: {name}
options:
  bundleIdPrefix: com.projectmidas
targets:
  {name}:
    type: application
    platform: iOS
    deploymentTarget: "17.0"
    sources: [{name}]
    settings:
      base:
        SWIFT_VERSION: "5.9"
        GENERATE_INFOPLIST_FILE: YES
        INFOPLIST_KEY_UILaunchScreen_Generation: YES
        TARGETED_DEVICE_FAMILY: "1,2"
        CODE_SIGN_STYLE: Automatic
''')
    (src/f'{name}App.swift').write_text(f'''import SwiftUI
@main
struct {name}App: App {{
    var body: some Scene {{
        WindowGroup {{ SiteBrowser() }}
    }}
}}
''')
    (src/'SiteBrowser.swift').write_text('''import SwiftUI
import WebKit

struct SiteBrowser: View {
    @State private var homeVersion = 0
    var body: some View {
        NavigationStack {
            SiteWebView()
                .id(homeVersion)
                .navigationTitle(APP_TITLE)
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
        web.load(URLRequest(url: URL(string: APP_URL)!))
        return web
    }
    func updateUIView(_ uiView: WKWebView, context: Context) {}
}
'''.replace('APP_TITLE',json.dumps(name)).replace('APP_URL',json.dumps(url)))
    (base/'README.md').write_text(f'# {name}\n\nNative SwiftUI WKWebView wrapper for {url}.\nWebsite capabilities require live device testing. This is not an API integration.\n')
    from midas_application_catalog import sync
    sync(root)
    return base
def check(name,root=ROOT):
    base=root/'apps'/name
    files=[base/'project.yml',base/name/f'{name}App.swift',base/name/'SiteBrowser.swift']
    missing=[str(f) for f in files if not f.is_file()]
    if missing:return {'passed':False,'missing':missing}
    source=files[-1].read_text()
    return {'passed':all(x in source for x in ('WKWebView','websiteDataStore = .default()','allowsBackForwardNavigationGestures','URLRequest')),
            'missing':[]}
def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['generate','check']);p.add_argument('--name',required=True);p.add_argument('--url',default='https://www.govdeals.com')
    a=p.parse_args()
    print(json.dumps({'path':str(generate(a.name,a.url))} if a.action=='generate' else check(a.name),indent=2))
if __name__=='__main__':main()
