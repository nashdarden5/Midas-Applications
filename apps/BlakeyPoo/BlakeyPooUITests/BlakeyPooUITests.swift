import XCTest

final class BlakeyPooUITests: XCTestCase {
    func testAppLaunchAndHomeNavigation() {
        let app = XCUIApplication()
        app.launch()
        XCTAssertTrue(app.navigationBars["BlakeyPoo"].waitForExistence(timeout: 15))
        let home = app.buttons["Home"]
        XCTAssertTrue(home.exists)
        home.tap()
        XCTAssertTrue(app.navigationBars["BlakeyPoo"].exists)
    }
}
