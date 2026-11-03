"""Headless viewport and interaction smoke tests for RC Team preview."""
from pathlib import Path
import subprocess
import sys
import time
import unittest
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
BASE = "http://127.0.0.1:8765/"


class BrowserSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ARTIFACTS.mkdir(exist_ok=True)
        cls.server = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8765", "-d", str(ROOT)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        for _ in range(50):
            try:
                urlopen(BASE, timeout=0.3).close()
                break
            except OSError:
                time.sleep(0.1)
        else:
            cls.server.terminate()
            raise RuntimeError("Local preview server did not start")
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()
        cls.server.terminate()
        cls.server.wait(timeout=5)

    def page(self, width=390):
        page = self.browser.new_page(
            viewport={"width": width, "height": 900},
            reduced_motion="reduce",
            device_scale_factor=1
        )
        page.goto(BASE, wait_until="domcontentloaded")
        return page

    def test_no_horizontal_overflow_at_common_widths(self):
        for width in (320, 375, 390, 570, 768, 850, 1024, 1280, 1920):
            with self.subTest(width=width):
                page = self.page(width)
                overflow = page.evaluate(
                    "() => ({doc: document.documentElement.scrollWidth, "
                    "body: document.body.scrollWidth, viewport: innerWidth})"
                )
                self.assertLessEqual(
                    overflow["doc"], width + 2,
                    f"Document wider than viewport at {width}px: {overflow}"
                )
                self.assertLessEqual(
                    overflow["body"], width + 2,
                    f"Body wider than viewport at {width}px: {overflow}"
                )
                self.assertTrue(page.locator("h1").is_visible())
                self.assertTrue(page.locator("#contacto").count() == 1)
                if width in (390, 1280):
                    page.screenshot(path=str(ARTIFACTS / f"rc-team-{width}.png"), full_page=True)
                page.close()

    def test_mobile_menu_and_links(self):
        page = self.page(390)
        menu = page.locator(".menu-toggle")
        menu.click()
        self.assertEqual(menu.get_attribute("aria-expanded"), "true")
        page.get_by_role("navigation", name="Navegación principal").get_by_role(
            "link", name="Team"
        ).click()
        self.assertEqual(page.locator(".menu-toggle").get_attribute("aria-expanded"), "false")
        self.assertEqual(page.evaluate("location.hash"), "#team")
        page.close()

    def test_media_filters(self):
        page = self.page(1024)
        self.assertEqual(page.locator(".media-tile:visible").count(), 6)
        page.get_by_role("button", name="Digital", exact=True).click()
        self.assertEqual(page.locator(".media-tile:visible").count(), 1)
        self.assertEqual(
            page.get_by_role("button", name="Digital", exact=True).get_attribute("aria-pressed"),
            "true"
        )
        page.get_by_role("button", name="Todos").click()
        self.assertEqual(page.locator(".media-tile:visible").count(), 6)
        page.close()

    def test_local_logos_and_demo_form(self):
        page = self.page(390)
        img = page.locator(".brand img")
        self.assertEqual(img.get_attribute("src"), "assets/logo-rc-team-negro.webp")
        self.assertTrue(img.evaluate("(el) => el.complete && el.naturalWidth > 0"))
        self.assertEqual(page.locator("#contact-form").get_attribute("action"), "#")
        self.assertEqual(page.locator("#contact-form").get_attribute("method"), "post")
        self.assertTrue(page.get_by_text("Vista previa:", exact=False).count() > 0)
        page.close()


    def test_original_content_preserved(self):
        page = self.page(1024)
        for heading in (
            "Planificación de Medios", "Desarrollo de Estrategia",
            "Desarrollo de Proyectos", "Innovación", "Investigación"
        ):
            self.assertGreater(page.get_by_role("heading", name=heading, exact=True).count(), 0)
        self.assertEqual(page.get_by_role("heading", name="Rodrigo Cornejo S.M.").count(), 1)
        self.assertEqual(page.locator(".media-history-logos img").count(), 9)
        self.assertTrue(page.locator('a[href="https://www.declasseeuucl.cl"]').count() > 0)
        self.assertTrue(page.locator('a[href="tel:+56993324792"]').count() > 0)
        self.assertTrue(page.locator('a[href="tel:+56923888013"]').count() > 0)
        self.assertEqual(page.get_by_role("contentinfo").count(), 1)
        page.close()

    def test_filter_status_and_grid(self):
        page = self.page(390)
        page.get_by_role("button", name="Digital", exact=True).click()
        self.assertEqual(page.locator("#filter-status").inner_text(), "Mostrando 1 categoría de medios.")
        self.assertTrue(page.locator(".media-grid").evaluate("(el) => el.classList.contains('is-filtered')"))
        self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 392)
        page.close()

    def test_content_visible_without_javascript(self):
        page = self.browser.new_page(viewport={"width": 390, "height": 900}, java_script_enabled=False)
        page.goto(BASE, wait_until="domcontentloaded")
        self.assertEqual(
            page.locator(".strategy-heading").evaluate("(el) => getComputedStyle(el).opacity"),
            "1"
        )
        self.assertTrue(page.get_by_role("heading", name="Investigación").count() > 0)
        page.close()

if __name__ == "__main__":
    unittest.main()
