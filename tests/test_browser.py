"""Headless viewport and interaction smoke tests for RC Team preview."""
from pathlib import Path
import os
import json
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
                page.evaluate("""async () => {
                    await document.fonts.ready;
                    await Promise.all([...document.images].map(img => {
                        img.loading = 'eager';
                        return img.decode();
                    }));
                }""")
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), width + 2)
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

    def test_menu_keyboard_and_resize(self):
        page = self.page(375)
        toggle = page.locator(".menu-toggle")
        toggle.focus()
        page.keyboard.press("Enter")
        page.keyboard.press("Shift+Tab")
        self.assertEqual(page.evaluate("document.activeElement.getAttribute('href')"), "#contacto")
        page.keyboard.press("Tab")
        self.assertTrue(toggle.evaluate("el => el === document.activeElement"))
        page.keyboard.press("Escape")
        self.assertEqual(toggle.get_attribute("aria-expanded"), "false")
        self.assertTrue(toggle.evaluate("el => el === document.activeElement"))
        toggle.click()
        page.set_viewport_size({"width": 1024, "height": 900})
        page.wait_for_function("!document.body.classList.contains('menu-open')")
        page.close()

    def test_layout_without_external_fonts(self):
        page = self.browser.new_page(viewport={"width": 320, "height": 900}, reduced_motion="reduce")
        page.route("**/fonts.googleapis.com/**", lambda route: route.abort())
        page.goto(BASE, wait_until="domcontentloaded")
        self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 322)
        page.close()

    def test_reduced_motion_and_visible_keyboard_focus(self):
        page = self.page(375)
        page.keyboard.press("Tab")
        self.assertTrue(page.locator('.skip-link').evaluate("el => el === document.activeElement"))
        self.assertNotEqual(page.locator('.skip-link').evaluate("el => getComputedStyle(el).outlineStyle"), "none")
        self.assertEqual(page.evaluate("getComputedStyle(document.documentElement).scrollBehavior"), "auto")
        self.assertLessEqual(float(page.locator('.wave i').first.evaluate(
            "el => parseFloat(getComputedStyle(el).animationDuration)"
        )), .001)
        self.assertEqual(page.locator('.hero-copy').evaluate("el => getComputedStyle(el).opacity"), "1")
        page.close()

    def test_form_validation_and_mail_draft(self):
        from urllib.parse import urlsplit, parse_qs
        page = self.page(375)
        navigations = []
        session = page.context.new_cdp_session(page)
        session.send("Page.enable")
        session.on("Page.frameRequestedNavigation", lambda event: navigations.append(event["url"]))
        page.locator('[name="nombre"]').fill("   ")
        page.locator('[name="email"]').fill("qa@example.org")
        page.locator('[name="mensaje"]').fill("Consulta de prueba & medios")
        page.locator('#contact-form button[value="correo"]').click()
        self.assertFalse(page.locator('[name="nombre"]').evaluate("el => el.checkValidity()"))
        self.assertFalse(navigations)
        page.locator('[name="nombre"]').fill("Prueba QA")
        page.locator('#contact-form button[value="correo"]').click()
        page.wait_for_function("document.querySelector('#form-feedback').textContent.length > 0")
        page.wait_for_timeout(200)
        drafts = [url for url in navigations if url.startswith("mailto:")]
        self.assertEqual(len(drafts), 1)
        query = parse_qs(urlsplit(drafts[0]).query)
        self.assertEqual(query["subject"], ["Consulta web RC Team - Prueba QA"])
        self.assertIn("Consulta de prueba & medios", query["body"][0])
        self.assertTrue(page.locator('#mail-fallback').is_visible())
        self.assertEqual(page.locator('#mail-draft-link').get_attribute('href'), drafts[0])
        self.assertIn("Consulta de prueba & medios", page.locator('#mail-draft-copy').input_value())
        self.assertIn("qa@example.org", page.locator('#mail-draft-copy').input_value())
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

    def test_images_load_and_internal_links_resolve(self):
        page = self.page(1280)
        for image in page.locator("img").all():
            image.scroll_into_view_if_needed()
            image.evaluate("el => el.loading = 'eager'")
            image.evaluate("el => el.decode()")
            self.assertGreater(image.evaluate("el => el.naturalWidth"), 0)
        self.assertEqual(page.locator('a[href^="#"]').evaluate_all("""links =>
            links.filter(link => !document.getElementById(link.hash.slice(1))).map(link => link.hash)
        """), [])
        page.close()


    def test_original_content_preserved(self):
        page = self.page(1024)
        for heading in (
            "Planificación de Medios", "Desarrollo de Estrategia",
            "Desarrollo de Proyectos", "Innovación", "Investigación"
        ):
            self.assertGreater(page.get_by_role("heading", name=heading, exact=True).count(), 0)
        self.assertEqual(page.get_by_role("heading", name="Rodrigo Cornejo S.M.").count(), 1)
        self.assertEqual(page.locator(".media-history").count(), 0)
        self.assertEqual(page.locator('a[href="https://www.declasseeuucl.cl"]').count(), 0)
        self.assertGreater(page.get_by_text("23.000 documentos", exact=False).count(), 0)
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
        self.assertTrue(page.locator('#main-nav a[href="#team"]').is_visible())
        self.assertFalse(page.locator('#contact-form').is_visible())
        self.assertTrue(page.locator('noscript a[href="mailto:contacto@rcteam.cl"]').is_visible())
        page.close()

    def test_mobile_menu_closed_before_deferred_script(self):
        page = self.browser.new_page(viewport={"width": 375, "height": 900})
        page.route("**/script.js", lambda route: route.abort())
        page.goto(BASE, wait_until="domcontentloaded")
        self.assertFalse(page.locator('#main-nav').is_visible())
        self.assertTrue(page.locator('.menu-toggle').is_visible())
        self.assertEqual(page.locator('html').get_attribute('class'), 'js')
        page.close()


    def test_automated_accessibility_critical_violations(self):
        """WCAG automated smoke check; not a substitute for human screen-reader QA."""
        from pathlib import Path
        axe_path = Path(os.environ.get("AXE_CORE_PATH", ROOT / "node_modules" / "axe-core" / "axe.min.js"))
        if not axe_path.exists():
            self.skipTest("axe-core is installed by browser-qa CI; locally run npm install --no-save axe-core@4")
        for width in (390, 1280):
            with self.subTest(width=width):
                page = self.page(width)
                page.add_script_tag(path=str(axe_path))
                violations = page.evaluate("""async () => {
                  const results = await window.axe.run(document, {
                    runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']}
                  });
                  return results.violations.map(v => ({
                    id: v.id, impact: v.impact, description: v.description,
                    nodes: v.nodes.slice(0, 3).map(n => n.target.join(' '))
                  }));
                }""")
                critical = [v for v in violations if v["impact"] == "critical"]
                serious = [v for v in violations if v["impact"] == "serious"]
                (ARTIFACTS / f"axe-{width}.json").write_text(
                    json.dumps(violations, ensure_ascii=False, indent=2), encoding="utf-8"
                )
                self.assertFalse(critical, f"Critical axe violations at {width}px: {critical}")
                self.assertFalse(serious, f"Serious axe violations at {width}px: {serious}")
                page.close()



    def test_visual_footer_hero_geometry(self):
        page = self.page(1280)
        footer_logo = page.locator(".footer-brand img")
        footer_logo.scroll_into_view_if_needed()
        page.wait_for_function("document.querySelector('.footer-brand img').naturalWidth > 0")
        dimensions = footer_logo.evaluate("""(el) => {
          const r = el.getBoundingClientRect();
          return {rendered: r.width / r.height, intrinsic: el.naturalWidth / el.naturalHeight};
        }""")
        self.assertAlmostEqual(dimensions["rendered"], dimensions["intrinsic"], delta=0.08)
        rects = page.evaluate("""() => {
          const a = document.querySelector('.hero-art-caption').getBoundingClientRect();
          const b = document.querySelector('.hero-art-card-b').getBoundingClientRect();
          return {overlap: a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top};
        }""")
        self.assertFalse(rects["overlap"], "Hero caption overlaps the lower collage card")
        page.close()

    def test_mobile_contact_and_media_geometry(self):
        for width in (320, 375, 570):
            page = self.page(width)
            overlaps = page.evaluate("""() => {
                const caption = document.querySelector('.hero-art-caption').getBoundingClientRect();
                return [...document.querySelectorAll('.hero-art-card')].some(el => {
                    const card = el.getBoundingClientRect();
                    return caption.left < card.right && caption.right > card.left &&
                        caption.top < card.bottom && caption.bottom > card.top;
                });
            }""")
            self.assertFalse(overlaps, f"Hero caption overlaps a card at {width}px")
            page.close()
        page = self.page(320)
        positions = page.evaluate("""() => {
          const heading = document.querySelector('.contact-heading h2').getBoundingClientRect();
          const orb = document.querySelector('.contact-orb').getBoundingClientRect();
          return {orbRight:orb.right, orbTop:orb.top, headingBottom:heading.bottom};
        }""")
        self.assertLessEqual(positions["orbRight"], 321)
        self.assertGreaterEqual(positions["orbTop"], positions["headingBottom"] - 1)
        page.close()

        page = self.page(390)
        dimensions = page.evaluate("""() => ({
            grid: document.querySelector('.media-grid').getBoundingClientRect().width,
            last: document.querySelector('.media-tile:nth-child(6)').getBoundingClientRect().width
        })""")
        self.assertAlmostEqual(dimensions["grid"], dimensions["last"], delta=2)
        page.close()

        page = self.page(1280)
        page.get_by_role("button", name="Digital", exact=True).click()
        selected = page.locator(".media-tile:visible")
        self.assertEqual(selected.count(), 1)
        self.assertLessEqual(selected.first.bounding_box()["width"], 461)
        page.close()

    def test_team_last_row_is_centered(self):
        for width in (390, 768):
            with self.subTest(width=width):
                page = self.page(width)
                positions = page.evaluate("""() => {
                  const container = document.querySelector('.team-grid').getBoundingClientRect();
                  const children = Array.from(document.querySelectorAll('.team-grid > .team-placeholder'));
                  const items = children.slice(window.innerWidth < 571 ? -1 : -2);
                  const left = Math.min(...items.map(el => el.getBoundingClientRect().left));
                  const right = Math.max(...items.map(el => el.getBoundingClientRect().right));
                  return {itemsMid:(left+right)/2, containerMid:container.left+container.width/2};
                }""")
                self.assertAlmostEqual(positions["itemsMid"], positions["containerMid"], delta=5)
                page.close()

    def test_mobile_menu_backdrop_and_scroll_lock(self):
        page = self.page(390)
        toggle = page.locator(".menu-toggle")
        toggle.click()
        self.assertTrue(page.locator("body").evaluate("(el) => el.classList.contains('menu-open')"))
        self.assertTrue(page.locator(".menu-backdrop").is_visible())
        page.mouse.click(8, 880)
        self.assertEqual(toggle.get_attribute("aria-expanded"), "false")
        self.assertFalse(page.locator("body").evaluate("(el) => el.classList.contains('menu-open')"))
        page.close()



    def test_rodrigo_v2_content_and_section_order(self):
        page = self.page(1280)
        normalized = lambda locator: " ".join(locator.inner_text().split())
        self.assertIn("Vamos más allá de la pauta.", normalized(page.locator("#hero-title")))
        self.assertIn("Pensamos, planificamos", normalized(page.locator("#strategy-title")))
        self.assertIn("Cada desafío merece una estrategia a su medida.", normalized(page.locator(".catalog-intro h3")))
        self.assertIn("Conectamos marcas", normalized(page.locator("#media-title")))
        self.assertIn("Un proyecto de alcance internacional.", normalized(page.locator("#case-title")))
        self.assertIn("Las buenas estrategias", normalized(page.locator("#contact-title")))
        self.assertEqual(page.locator(".hero-footnote").count(), 0)
        self.assertEqual(page.locator(".media-history").count(), 0)
        self.assertEqual(page.locator("#metodo, .investment, #territorios, .values").count(), 0)
        self.assertEqual(page.locator('a[href="#metodo"]').count(), 0)
        self.assertEqual(page.locator(".case-study .button").count(), 0)
        self.assertTrue(page.locator(".agency-section").evaluate(
            "(el) => el.previousElementSibling?.classList.contains('hero')"
        ))
        self.assertTrue(page.locator(".strategy").evaluate(
            "(el) => el.previousElementSibling?.classList.contains('agency-section')"
        ))
        self.assertGreater(page.get_by_text("Vamos por un café y conversamos!", exact=True).count(), 0)
        self.assertGreater(page.get_by_text("O iniciamos una conversación por WhatsApp", exact=False).count(), 0)
        self.assertTrue(page.locator('meta[name="robots"][content="noindex,nofollow"]').count() == 1)
        page.close()

    def test_rodrigo_v2_timeline_and_declass_copy(self):
        page = self.page(1024)
        cards = page.locator(".strategy .timeline article")
        self.assertEqual(cards.count(), 4)
        expected = [
            "Cada decisión comienza con una buena estrategia.",
            "Nuestro conocimiento se transforma en valor.",
            "De las ideas a la acción.",
            "Los resultados respaldan cada decisión.",
        ]
        for i, title in enumerate(expected):
            self.assertEqual(" ".join(cards.nth(i).locator("h3").inner_text().split()), title)
        paragraph = " ".join(page.locator(".case-copy p").inner_text().split())
        self.assertIn("Embajada de los Estados Unidos", paragraph)
        self.assertIn("más de 23.000 documentos", paragraph)
        self.assertIn("FBI, la CIA, la NSA", paragraph)
        page.close()



    def test_brand_logo_and_matching_favicon(self):
        page = self.page(1280)
        for selector in (".brand img", ".footer-brand img"):
            logo = page.locator(selector)
            logo.scroll_into_view_if_needed()
            page.wait_for_function(
                "(selector) => { const el = document.querySelector(selector); return el && el.complete && el.naturalWidth > 0; }",
                arg=selector
            )
            self.assertTrue(logo.evaluate("(el) => el.complete && el.naturalWidth > 0"))
            self.assertIn("rc-black-to-alpha", logo.evaluate("(el) => getComputedStyle(el).filter"))
        self.assertTrue(page.locator("filter#rc-black-to-alpha").count() == 1)
        icon = page.locator('link[rel="icon"]')
        self.assertEqual(icon.get_attribute("href"), "assets/favicon-rc-team.svg")
        self.assertEqual(icon.get_attribute("type"), "image/svg+xml")
        icon_path = ROOT / "assets" / "favicon-rc-team.svg"
        self.assertTrue(icon_path.exists())
        import base64
        from xml.etree import ElementTree
        root = ElementTree.fromstring(icon_path.read_text(encoding="utf-8"))
        embedded = root.find("{http://www.w3.org/2000/svg}image")
        self.assertIsNotNone(embedded)
        data = embedded.attrib["href"].split(",", 1)[1]
        self.assertTrue(base64.b64decode(data).startswith(b"\x89PNG\r\n\x1a\n"))
        page.close()

    def test_media_collage_fills_grid_without_empty_cells(self):
        for width in (320, 390, 768, 1280, 1920):
            with self.subTest(width=width):
                page = self.page(width)
                measures = page.evaluate("""() => {
                    const grid = document.querySelector(".media-grid").getBoundingClientRect();
                    const tiles = [...document.querySelectorAll(".media-grid .media-tile")];
                    const covered = tiles.reduce((sum, tile) => {
                       const r = tile.getBoundingClientRect();
                       return sum + r.width * r.height;
                    }, 0);
                    const last = tiles[tiles.length - 1].getBoundingClientRect();
                    return {coverage:covered / (grid.width * grid.height),
                      gridRight:grid.right,gridBottom:grid.bottom,
                      lastRight:last.right,lastBottom:last.bottom};
                }""")
                self.assertGreater(measures["coverage"], .94,
                    f"Media collage has visible blank cells at {width}px: {measures}")
                self.assertAlmostEqual(measures["lastRight"], measures["gridRight"], delta=3)
                self.assertAlmostEqual(measures["lastBottom"], measures["gridBottom"], delta=3)
                page.close()

    def test_hero_collage_no_overlap_intermediate_widths(self):
        for width in (850, 851, 900, 1024, 1100, 1140, 1280):
            with self.subTest(width=width):
                page = self.page(width)
                rects = page.evaluate("""() => {
                    const cap = document.querySelector(".hero-art-caption").getBoundingClientRect();
                    const cardA = document.querySelector(".hero-art-card-a").getBoundingClientRect();
                    const cardB = document.querySelector(".hero-art-card-b").getBoundingClientRect();
                    const gap = (a, b) => Math.max(a.left - b.right, b.left - a.right, a.top - b.bottom, b.top - a.bottom);
                    return {gapA: gap(cap, cardA), gapB: gap(cap, cardB)};
                }""")
                self.assertGreaterEqual(rects["gapA"], 16, f"Caption too close to card A at {width}px: {rects}")
                self.assertGreaterEqual(rects["gapB"], 16, f"Caption too close to card B at {width}px: {rects}")
                page.close()

    def test_micro_labels_legible_and_filtered_media_balanced(self):
        for width in (320, 1280):
            with self.subTest(width=width):
                page = self.page(width)
                sizes = page.evaluate("""() => {
                    const selectors = [
                        ".eyebrow", ".section-label", ".media-tile-overlay small",
                        ".team-placeholder span", ".services-grid span",
                        ".hero-art-card-a > span", ".hero-art-card-b > span"
                    ];
                    return selectors.flatMap(sel =>
                        [...document.querySelectorAll(sel)].map(el => ({
                            sel, size: parseFloat(getComputedStyle(el).fontSize)
                        }))
                    );
                }""")
                for item in sizes:
                    self.assertGreaterEqual(item["size"], 11.0, f"Micro-label below 11px at {width}px: {item}")
                page.close()

        for width in (1280, 1920):
            with self.subTest(filter_width=width):
                page = self.page(width)
                page.get_by_role("button", name="Tradicionales", exact=True).click()
                ratios = page.evaluate("""() => {
                    const grid = document.querySelector(".media-grid").getBoundingClientRect();
                    const tiles = [...document.querySelectorAll(".media-tile:not([hidden])")];
                    const totalW = tiles.reduce((s, t) => s + t.getBoundingClientRect().width, 0);
                    return {totalW, gridW: grid.width, ratio: totalW / grid.width};
                }""")
                self.assertGreaterEqual(ratios["ratio"], 0.98, f"Filtered tiles leave trailing gap at {width}px: {ratios}")
                page.close()

    def test_laptop_hero_above_the_fold_and_no_overlap(self):
        viewports = [
            (1366, 610),
            (1366, 768),
            (1440, 800),
            (1536, 864),
            (1920, 1080),
            (1024, 768),
            (390, 844),
        ]
        for width, height in viewports:
            with self.subTest(viewport=f"{width}x{height}"):
                page = self.browser.new_page(
                    viewport={"width": width, "height": height},
                    reduced_motion="reduce",
                    device_scale_factor=1,
                )
                page.goto(BASE, wait_until="domcontentloaded")
                metrics = page.evaluate("""() => {
                    const vh = window.innerHeight, vw = window.innerWidth;
                    const h1 = document.querySelector(".hero h1").getBoundingClientRect();
                    const lead = document.querySelector(".hero-lead").getBoundingClientRect();
                    const cta = document.querySelector(".hero-actions .button-primary").getBoundingClientRect();
                    const cap = document.querySelector(".hero-art-caption").getBoundingClientRect();
                    const cardA = document.querySelector(".hero-art-card-a").getBoundingClientRect();
                    const cardB = document.querySelector(".hero-art-card-b").getBoundingClientRect();
                    const gap = (a, b) => Math.max(a.left - b.right, b.left - a.right, a.top - b.bottom, b.top - a.bottom);
                    return {
                        vh,
                        overflow: document.documentElement.scrollWidth - vw,
                        h1Size: parseFloat(getComputedStyle(document.querySelector(".hero h1")).fontSize),
                        h1Bottom: h1.bottom,
                        leadBottom: lead.bottom,
                        ctaBottom: cta.bottom,
                        gapCapCardA: gap(cap, cardA),
                        gapCapCardB: gap(cap, cardB),
                        gapCardACardB: gap(cardA, cardB),
                    };
                }""")
                self.assertLessEqual(metrics["overflow"], 2, f"Overflow at {width}x{height}: {metrics}")
                self.assertLessEqual(metrics["leadBottom"], height, f"Lead below fold at {width}x{height}: {metrics}")
                self.assertLessEqual(metrics["ctaBottom"], height, f"CTA below fold at {width}x{height}: {metrics}")
                min_gap = 10 if width <= 570 else 16
                self.assertGreaterEqual(metrics["gapCapCardA"], min_gap, f"Caption/CardA overlap at {width}x{height}: {metrics}")
                self.assertGreaterEqual(metrics["gapCapCardB"], min_gap, f"Caption/CardB overlap at {width}x{height}: {metrics}")
                self.assertGreaterEqual(metrics["gapCardACardB"], min_gap, f"CardA/CardB overlap at {width}x{height}: {metrics}")
                if (width, height) == (1920, 1080):
                    self.assertGreaterEqual(metrics["h1Size"], 100.0, f"1920x1080 H1 unintentionally shrunk: {metrics}")
                page.close()

    def test_team_members_confirmed_with_photos(self):
        expected = [
            ("Rodrigo Cornejo S.M.", "Director General"),
            ("Ignacio Szalay B.", "Desarrollo de Negocios y Medios"),
            ("Bárbara León G.", "Ejecutiva de Medios"),
            ("Paz Palacios V.", "Coordinadora de Administración"),
            ("Alejandra Fernández A.", "Coordinadora de Finanzas"),
        ]
        for width in (390, 1280):
            with self.subTest(width=width):
                page = self.page(width)
                page.locator("#team").scroll_into_view_if_needed()
                page.evaluate("document.querySelectorAll('#team img').forEach(i => i.loading = 'eager')")
                page.wait_for_function(
                    "[...document.querySelectorAll('#team img')].every(i => i.complete && i.naturalWidth > 0)"
                )
                cards = page.evaluate("""() => [...document.querySelectorAll('.team-grid > article')].map(a => ({
                    name: a.querySelector('h3').textContent.trim(),
                    role: a.querySelector('p').textContent.trim(),
                    alt: a.querySelector('img').alt,
                    rendered: a.querySelector('img').getBoundingClientRect().width,
                }))""")
                self.assertEqual([(c["name"], c["role"]) for c in cards], expected)
                for card in cards:
                    self.assertIn(card["name"], card["alt"])
                    self.assertGreater(card["rendered"], 100)
                self.assertEqual(page.locator("#team .avatar-silhouette").count(), 0)
                self.assertEqual(page.locator("#team").get_by_text("confirmar", exact=False).count(), 0)
                group = page.locator(".team-group img")
                self.assertEqual(group.count(), 1)
                self.assertGreater(group.evaluate("(el) => el.getBoundingClientRect().height"), 200)
                page.close()

    def test_footer_shows_rc_team_and_tres_mentes(self):
        for width in (390, 1280):
            with self.subTest(width=width):
                page = self.page(width)
                logo = page.locator(".site-footer .footer-partner-logo")
                self.assertEqual(logo.count(), 1)
                logo.scroll_into_view_if_needed()
                page.wait_for_function(
                    "(() => { const i = document.querySelector('.footer-partner-logo'); return i.complete && i.naturalWidth > 0; })()"
                )
                info = page.evaluate("""() => {
                    const tm = document.querySelector('.footer-partner-logo');
                    const rc = document.querySelector('.footer-brand img');
                    const a = tm.getBoundingClientRect(), b = rc.getBoundingClientRect();
                    return {
                        alt: tm.alt, width: a.width,
                        rendered: a.width / a.height, intrinsic: tm.naturalWidth / tm.naturalHeight,
                        centerDelta: Math.abs((a.top + a.bottom) / 2 - (b.top + b.bottom) / 2),
                        afterRc: a.left > b.right,
                        filter: getComputedStyle(tm).filter,
                        overflow: document.documentElement.scrollWidth - innerWidth,
                    };
                }""")
                self.assertIn("Tres Mentes", info["alt"])
                link = page.locator(".site-footer a.footer-partner")
                self.assertEqual(link.get_attribute("href"), "https://tr3smentes.cl/")
                self.assertEqual(link.get_attribute("target"), "_blank")
                self.assertIn("noopener", link.get_attribute("rel"))
                self.assertGreaterEqual(info["width"], 110)
                self.assertAlmostEqual(info["rendered"], info["intrinsic"], delta=0.08)
                self.assertTrue(info["afterRc"], info)
                self.assertLessEqual(info["centerDelta"], 6, info)
                self.assertEqual(info["filter"], "none")
                self.assertLessEqual(info["overflow"], 2)
                page.close()

    def test_hero_fills_real_laptop_browser_viewport(self):
        # Áreas útiles medidas en Opera maximizado sobre pantalla 1366x768 (zoom 100 % y 125 %).
        for width, height, min_h1 in ((1324, 608, 60), (1053, 488, 40)):
            with self.subTest(viewport=f"{width}x{height}"):
                page = self.browser.new_page(
                    viewport={"width": width, "height": height},
                    reduced_motion="reduce", device_scale_factor=1,
                )
                page.goto(BASE, wait_until="domcontentloaded")
                m = page.evaluate("""() => ({
                    hero: document.querySelector('.hero').getBoundingClientRect().height,
                    h1: parseFloat(getComputedStyle(document.querySelector('.hero h1')).fontSize),
                    cta: document.querySelector('.hero-actions .button-primary').getBoundingClientRect().bottom,
                })""")
                self.assertGreaterEqual(m["hero"], height - 2, f"Franja vacía bajo el hero: {m}")
                self.assertGreaterEqual(m["h1"], min_h1, f"Titular demasiado pequeño: {m}")
                self.assertLessEqual(m["cta"], height, f"CTA bajo el pliegue: {m}")
                page.close()

    def test_footer_credits_mastertech_brand(self):
        page = self.page(1280)
        credit = page.locator('.site-footer a[href="https://mastertechg.com"]')
        self.assertEqual(credit.inner_text().strip(), "MasterTech")
        page.close()

    def test_nav_links_land_at_section_start_with_same_margin(self):
        # Pedido de Rodrigo (25-11-2026): "Qué hacemos" debe quedar al inicio, como las demás pestañas.
        for width, height in ((1324, 608), (1920, 969), (390, 844)):
            with self.subTest(viewport=f"{width}x{height}"):
                page = self.browser.new_page(viewport={"width": width, "height": height},
                                             reduced_motion="reduce", device_scale_factor=1)
                page.goto(BASE, wait_until="domcontentloaded")
                offsets = {}
                for href in ("#agencia", "#servicios", "#medios", "#team", "#contacto"):
                    self.assertEqual(page.locator(f'#main-nav a[href="{href}"]').count(), 1)
                    page.evaluate("window.scrollTo(0, 0); location.hash = ''")
                    page.evaluate(f"location.hash = '{href}'")
                    page.wait_for_timeout(150)
                    offsets[href] = page.evaluate(f"""() => {{
                        const header = document.querySelector('.site-header').getBoundingClientRect().bottom;
                        const section = document.querySelector('{href}');
                        return {{tag: section.tagName, label: section.querySelector('.section-label').getBoundingClientRect().top - header}};
                    }}""")
                for href, data in offsets.items():
                    self.assertEqual(data["tag"], "SECTION", f"{href} no apunta a una sección: {offsets}")
                labels = [d["label"] for d in offsets.values()]
                self.assertLessEqual(max(labels) - min(labels), 3, f"Márgenes distintos: {offsets}")
                self.assertGreaterEqual(min(labels), 0, f"Etiqueta tapada por el header: {offsets}")
                page.close()

    def test_back_to_top_links_scroll_to_page_start(self):
        # Reportado por Dirección (25-11-2026): "Volver arriba" cambiaba a #inicio sin desplazar,
        # porque el ancla estaba en el header fijo.
        for width in (390, 1324):
            with self.subTest(width=width):
                page = self.page(width)
                self.assertEqual(page.evaluate("document.getElementById('inicio').tagName"), "SECTION")
                for selector in ('.site-footer a[href="#inicio"]:not(.footer-brand)', ".footer-brand", ".brand"):
                    page.evaluate("history.replaceState(null, '', location.pathname); window.scrollTo(0, document.documentElement.scrollHeight)")
                    page.wait_for_timeout(100)
                    self.assertGreater(page.evaluate("scrollY"), 1000)
                    page.locator(selector).first.click()
                    page.wait_for_function("scrollY < 5", timeout=3000)
                page.close()

    def test_form_whatsapp_option(self):
        from urllib.parse import urlsplit, parse_qs
        page = self.page(375)
        page.evaluate("() => { window.__opened = []; window.open = (u) => { window.__opened.push(u); return {}; }; }")
        page.locator('[name="nombre"]').fill("Prueba QA")
        page.locator('[name="email"]').fill("qa@example.org")
        page.locator('[name="mensaje"]').fill("Consulta WhatsApp & medios")
        page.locator('#contact-form button[value="whatsapp"]').click()
        page.wait_for_function("window.__opened.length === 1")
        url = page.evaluate("window.__opened[0]")
        parts = urlsplit(url)
        self.assertEqual(parts.netloc + parts.path, "wa.me/56993324792")
        text = parse_qs(parts.query)["text"][0]
        self.assertIn("Prueba QA", text)
        self.assertIn("Consulta WhatsApp & medios", text)
        self.assertIn("WhatsApp", page.locator("#form-feedback").inner_text())
        page.close()

    def test_rodrigo_removed_side_paragraphs(self):
        # Pedido de Rodrigo (25-11-2026): quitar los párrafos laterales de Qué hacemos, Servicios y Medios.
        page = self.page(1280)
        body = page.locator("body").inner_text()
        for text in ("No se trata solo de aparecer", "Estas cinco áreas formaban parte",
                     "Soluciones para llegar donde están tus audiencias"):
            self.assertNotIn(text, body)
        page.close()

    def test_hero_uses_image_supplied_by_rodrigo(self):
        page = self.page(1280)
        info = page.evaluate("""() => {
            const img = document.querySelector('.hero-art-frame img');
            return {src: img.getAttribute('src'),
                    bg: getComputedStyle(document.querySelector('.hero-photo')).backgroundImage};
        }""")
        self.assertEqual(info["src"], "images/hero-fondo-ciudad-noche.webp")
        self.assertIn("hero-fondo-ciudad-noche.webp", info["bg"])
        self.assertNotIn("unsplash", info["bg"])
        page.wait_for_function("document.querySelector('.hero-art-frame img').naturalWidth > 0")
        page.close()


if __name__ == "__main__":
    unittest.main()
