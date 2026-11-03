"""SEO environment isolation, HTML metadata and deployment gate."""
import json
import re
import unittest
from pathlib import Path

from scripts.build_site import (
    PREVIEW_URL, PRODUCTION_URL, ROBOTS_PREVIEW, ROBOTS_PROD,
    preview_is_safe, production_seo_html, production_blockers, ROOT
)

HTML = (ROOT / "index.html").read_text(encoding="utf-8")
JS = (ROOT / "script.js").read_text(encoding="utf-8")


class SEO(unittest.TestCase):
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
        self.assertTrue(any("formulario" in issue.lower() for issue in blockers))
        self.assertTrue(any("equipo" in issue.lower() for issue in blockers))
        self.assertTrue(any("fotografías" in issue.lower() for issue in blockers))

    def test_relative_assets_survive_a_subdirectory(self):
        self.assertIn('src="assets/logo-rc-team-negro.webp"', HTML)
        self.assertIn('href="styles.css"', HTML)
        self.assertIn('src="script.js"', HTML)
        self.assertNotIn('src="/assets/', HTML)


if __name__ == "__main__":
    unittest.main()
