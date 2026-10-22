"""Browser regression tests against a generated site, never the production site.

Run after mkdocs build. Chromium is installed separately by Playwright. Screenshots
are written to browser-test-results for CI review. 590 CSS px is the reflow width
observed at 200% zoom in an 1180px desktop window, not a claim of device testing.
"""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import unittest

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "browser-test-results"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


class NavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        RESULTS.mkdir(exist_ok=True)
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT / "site")))
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.context = self.browser.new_context(viewport={"width": 590, "height": 820})
        self.page = self.context.new_page()
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.goto(self.base)
        expect(self.page.locator("html.conf2git-drawer-ready")).to_have_count(1)
        self.sidebar = self.page.locator("#conf2git-navigation")
        expect(self.page.get_by_role("button", name="Open navigation", exact=True)).to_be_visible()
        # Keep resolving the element while its containing header is inert.
        self.opener = self.page.locator(".conf2git-drawer-toggle")
        self.close = self.page.get_by_role("button", name="Close navigation", exact=True)

    def tearDown(self):
        self.page.screenshot(path=str(RESULTS / f"{self._testMethodName}.png"))
        self.context.close()
        self.assertEqual(self.errors, [], "Unexpected browser errors")

    def open_keyboard(self, key="Enter"):
        # Exercise real sequential keyboard access, not programmatic focus.
        for _ in range(5):
            self.page.keyboard.press("Tab")
            if self.opener.evaluate("e => e === document.activeElement"):
                break
        expect(self.opener).to_be_focused()
        self.page.keyboard.press(key)
        expect(self.opener).to_have_attribute("aria-expanded", "true")
        expect(self.close).to_be_focused()

    def test_closed_drawer_excluded_from_tab_order(self):
        expect(self.sidebar).to_be_hidden()
        self.assertTrue(self.sidebar.evaluate("e => e.inert"))
        self.assertEqual(self.sidebar.locator("a").first.evaluate("e => getComputedStyle(e).visibility"), "hidden")
        self.assertEqual(self.sidebar.locator("a[href='getting-started/']").evaluate("e => getComputedStyle(e).visibility"), "hidden")
        for _ in range(35):
            self.page.keyboard.press("Tab")
            self.assertFalse(self.sidebar.evaluate("e => e.contains(document.activeElement)"))

    def test_enter_space_escape_and_focus_return(self):
        self.open_keyboard()
        self.page.keyboard.press("Escape")
        expect(self.opener).to_be_focused()
        expect(self.opener).to_have_attribute("aria-expanded", "false")
        self.page.keyboard.press("Space")
        expect(self.close).to_be_focused()
        self.page.keyboard.press("Enter")
        expect(self.opener).to_be_focused()
        expect(self.sidebar).to_be_hidden()

    def test_modal_tab_cycle_and_pointer_overlay(self):
        self.open_keyboard("Space")
        expect(self.sidebar).to_have_attribute("aria-modal", "true")
        self.page.keyboard.press("Shift+Tab")
        self.assertTrue(self.sidebar.evaluate("e => e.contains(document.activeElement)"))
        self.page.keyboard.press("Tab")
        expect(self.close).to_be_focused()
        for _ in range(25):
            self.page.keyboard.press("Tab")
            self.assertTrue(self.sidebar.evaluate("e => e.contains(document.activeElement)"))
            self.assertTrue(self.page.evaluate("() => {const e=document.activeElement;return e.getClientRects().length>0 && getComputedStyle(e).visibility==='visible'}"))
        self.page.locator(".md-overlay").click(position={"x": 500, "y": 500})
        expect(self.opener).to_be_focused()
        self.assertFalse(self.page.locator(".md-content").evaluate("e => !!e.closest('[inert]')"))

    def test_disclosures_hide_children_and_all_guides_reachable(self):
        self.open_keyboard()
        group = self.sidebar.get_by_role("button", name="Configure and sync", exact=True)
        child = self.sidebar.get_by_role("link", name="Synchronization schedules", exact=True)
        expect(child).to_be_hidden()
        group.press("Enter")
        expect(group).to_have_attribute("aria-expanded", "true")
        expect(child).to_be_visible()
        group.press("Space")
        expect(group).to_have_attribute("aria-expanded", "false")
        expect(child).to_be_hidden()
        expect(group).to_be_focused()
        self.page.keyboard.press("Tab")
        panel_id = group.get_attribute("aria-controls")
        self.assertFalse(self.page.locator(f"#{panel_id}").evaluate("e => e.contains(document.activeElement)"))
        for name in ["Configure and sync", "Security and limits", "Help and recovery"]:
            self.sidebar.get_by_role("button", name=name, exact=True).press("Enter")
        self.page.screenshot(path=str(RESULTS / "compact-expanded-590.png"))
        for path in (ROOT / "docs").glob("*.md"):
            route = "" if path.stem == "index" else path.stem + "/"
            # Home has a dedicated logo link as well as its active-page TOC.
            links = self.sidebar.locator("a[href]").all()
            self.assertTrue(any(link.is_visible() and link.evaluate("(e, route) => new URL(e.href).pathname === '/' + route", route) for link in links), route)
        self.sidebar.get_by_role("link", name="Conversion support", exact=True).press("Enter")
        expect(self.page).to_have_url(self.base + "/conversion-support/")
        expect(self.page.locator("h1")).to_contain_text("Conversion support and image behavior")

    def test_table_of_contents_moves_focus_to_article(self):
        self.open_keyboard()
        toc = self.sidebar.get_by_role("button", name="Table of contents for Home", exact=True)
        toc.press("Space")
        expect(toc).to_have_attribute("aria-expanded", "true")
        self.sidebar.get_by_role("link", name="Guides", exact=True).press("Enter")
        expect(self.page.locator("#guides")).to_be_focused()
        expect(self.sidebar).to_be_hidden()
        expect(self.page).to_have_url(self.base + "/#guides")

    def test_resize_desktop_and_back_restores_navigation(self):
        self.open_keyboard()
        self.page.set_viewport_size({"width": 1440, "height": 1000})
        expect(self.opener).to_be_hidden()
        expect(self.opener).to_have_attribute("aria-expanded", "false")
        self.assertFalse(self.sidebar.evaluate("e => e.inert"))
        self.assertIsNone(self.sidebar.get_attribute("aria-modal"))
        self.assertEqual(self.sidebar.locator(".conf2git-disclosure").count(), 0)
        expect(self.sidebar.get_by_role("link", name="Get started", exact=True)).to_be_visible()
        self.page.screenshot(path=str(RESULTS / "desktop-1440.png"))
        self.sidebar.get_by_role("link", name="Get started", exact=True).focus()
        self.page.set_viewport_size({"width": 590, "height": 820})
        expect(self.opener).to_be_focused()
        expect(self.sidebar).to_be_hidden()
        self.page.keyboard.press("Space")
        expect(self.close).to_be_focused()

    def test_compact_widths_and_tablet_toc(self):
        for width in [320, 390, 590, 1000]:
            with self.subTest(width=width):
                self.page.set_viewport_size({"width": width, "height": 820})
                self.opener.press("Enter")
                expect(self.close).to_be_focused()
                toc = self.sidebar.locator("[data-conf2git-toggle='__toc']")
                self.assertEqual(toc.is_visible(), width < 960)
                self.page.screenshot(path=str(RESULTS / f"compact-open-{width}.png"))
                self.page.keyboard.press("Escape")
                self.assertTrue(self.page.evaluate("() => document.documentElement.scrollWidth <= innerWidth"))
                self.page.screenshot(path=str(RESULTS / f"compact-{width}.png"))

    def test_desktop_search_and_appearance(self):
        self.page.set_viewport_size({"width": 1440, "height": 1000})
        search = self.page.get_by_role("textbox", name="Search", exact=True)
        search.click()
        expect(self.page.locator(".md-search-result__meta")).to_have_text("Type to start searching")
        search.press_sequentially("authorization")
        result = self.page.locator(".md-search-result a[href*='github-authorization/']").first
        expect(result).to_be_visible()
        result.click()
        expect(self.page.locator("h1")).to_contain_text("GitHub authorization and branch behavior")
        schemes = set()
        for _ in range(3):
            self.page.locator('.md-header label[for^="__palette_"]:visible').click()
            schemes.add(self.page.locator("body").get_attribute("data-md-color-scheme"))
        self.assertEqual(schemes, {"default", "slate"})

    def test_static_fallback_without_custom_script_or_javascript(self):
        for javascript in [True, False]:
            with self.subTest(javascript=javascript):
                context = self.browser.new_context(java_script_enabled=javascript, viewport={"width": 590, "height": 820})
                if javascript:
                    context.route("**/javascripts/navigation.js", lambda route: route.abort())
                page = context.new_page()
                page.goto(self.base)
                expect(page.locator("html.conf2git-drawer-ready")).to_have_count(0)
                nav = page.locator(".md-sidebar--primary .md-nav--primary")
                for name in ["Home", "FAQ", "Get started", "GitHub authorization", "Conversion support", "Backup limitations", "Recovery and lifecycle"]:
                    expect(nav.get_by_role("link", name=name, exact=True)).to_be_visible()
                before = nav.bounding_box()["x"]
                title = nav.locator(":scope > label.md-nav__title")
                title.click(position={"x": 200, "y": title.bounding_box()["height"] - 8})
                expect(page.locator("#__drawer")).to_be_checked()
                self.assertAlmostEqual(nav.bounding_box()["x"], before, delta=1)
                self.assertEqual(page.locator(".md-sidebar--primary").evaluate("e => getComputedStyle(e).transform"), "none")
                expect(nav.get_by_role("link", name="Home", exact=True)).to_be_visible()
                page.screenshot(path=str(RESULTS / f"fallback-js-{javascript}.png"))
                context.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
