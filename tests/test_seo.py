"""SEO environment isolation, HTML metadata and deployment gate."""
import json
import re
import unittest
import tempfile
from pathlib import Path

from scripts.build_site import (
    PREVIEW_URL, PRODUCTION_URL, ROBOTS_PREVIEW, ROBOTS_PROD,
    preview_is_safe, production_seo_html, production_blockers, build, ROOT
)
from scripts.validate_site import SiteParser

HTML = (ROOT / "index.html").read_text(encoding="utf-8")
JS = (ROOT / "script.js").read_text(encoding="utf-8")


class SEO(unittest.TestCase):
    def test_picture_sources_are_validated(self):
        parser = SiteParser()
        parser.feed('<picture><source srcset="images/small.webp 1x, images/large.webp 2x"></picture>')
        self.assertEqual(parser.links, [
            ("source", "srcset", "images/small.webp"),
            ("source", "srcset", "images/large.webp"),
        ])

    def test_build_rejects_source_directories_and_ancestors(self):
        for destination in (ROOT, ROOT.parent, ROOT / "assets" / "preview", ROOT / "docs" / "preview"):
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                build("preview", destination)

    def test_preview_rejects_stale_production_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            (destination / "robots.txt").write_text("User-agent: *\nAllow: /", encoding="utf-8")
            with self.assertRaises(ValueError):
                build("preview", destination)
            self.assertFalse((destination / "index.html").exists())

    def test_preview_is_not_indexable(self):
        self.assertTrue(preview_is_safe(HTML))
        self.assertIn(ROBOTS_PREVIEW, HTML)
        self.assertNotIn(ROBOTS_PROD, HTML)
        self.assertNotIn('rel="canonical" href="https://rcteam.cl/"', HTML)

    def test_production_seo_is_separate_and_not_deployed(self):
        output = production_seo_html(HTML)
        self.assertIn(ROBOTS_PROD, output)
        self.assertNotIn(ROBOTS_PREVIEW, output)
        self.assertIn('<link rel="canonical" href="https://rcteam.cl/">', output)
        self.assertIn(f'<meta property="og:url" content="{PRODUCTION_URL}">', output)
        self.assertIn(f'<meta property="og:image" content="{PRODUCTION_URL}assets/logo-rc-team-negro.webp">', output)
        self.assertIn(f'<meta name="twitter:image" content="{PRODUCTION_URL}assets/logo-rc-team-negro.webp">', output)
        self.assertNotIn(PREVIEW_URL, output)

    def test_structured_data_has_no_unverified_address(self):
        output = production_seo_html(HTML)
        match = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', output, re.S)
        self.assertIsNotNone(match)
        schema = json.loads(match.group(1))
        self.assertEqual(schema["@type"], "Organization")
        self.assertEqual(schema["url"], PRODUCTION_URL)
        self.assertNotIn("address", schema)
        self.assertNotIn("foundingDate", schema)
        self.assertNotIn("numberOfEmployees", schema)

    def test_production_is_blocked_until_ready(self):
        blockers = production_blockers(HTML, JS)
        # El formulario ya tiene endpoint (enviar.php) y las fotos Unsplash están aprobadas (26-11-2026).
        self.assertFalse(any("formulario" in issue.lower() for issue in blockers))
        self.assertFalse(any("fotografías" in issue.lower() for issue in blockers))
        self.assertIn('action="enviar.php"', HTML)

    def test_team_blocker_fires_only_with_pending_profiles(self):
        pending = HTML.replace("</main>", '<div class="team-placeholder"></div></main>', 1)
        self.assertTrue(any("equipo" in issue.lower() for issue in production_blockers(pending, JS)))
        # Team confirmado por Rodrigo el 23-11-2026: ya no quedan perfiles pendientes.
        self.assertFalse(any("equipo" in issue.lower() for issue in production_blockers(HTML, JS)))

    def test_relative_assets_survive_a_subdirectory(self):
        self.assertIn('src="assets/logo-rc-team-negro.webp"', HTML)
        self.assertIn('href="styles.css"', HTML)
        self.assertIn('src="script.js"', HTML)
        self.assertNotIn('src="/assets/', HTML)


if __name__ == "__main__":
    unittest.main()
