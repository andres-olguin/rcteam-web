#!/usr/bin/env python3
"""Validación estática básica de RC Team sin dependencias externas."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "index.html"
REQUIRED = ["index.html", "styles.css", "script.js"]
LOCAL_ATTRS = {"src", "href", "poster"}


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.errors = []
        self.title = False
        self.lang = False
        self.main = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html" and attrs.get("lang"):
            self.lang = True
        if tag == "title":
            self.title = True
        if tag == "main":
            self.main = True
        if attrs.get("id"):
            value = attrs["id"]
            if value in self.ids:
                self.errors.append(f"ID duplicado: {value}")
            self.ids.add(value)
        for key in LOCAL_ATTRS:
            if attrs.get(key):
                self.links.append((tag, key, attrs[key]))


def main():
    errors = [f"Falta archivo esencial: {path}" for path in REQUIRED if not (ROOT / path).is_file()]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    parser = SiteParser()
    parser.feed(ENTRY.read_text(encoding="utf-8"))
    errors.extend(parser.errors)
    if not parser.lang:
        errors.append("Falta atributo lang en html")
    if not parser.title:
        errors.append("Falta title")
    if not parser.main:
        errors.append("Falta main")
    for tag, attr, value in parser.links:
        url = urlsplit(value.strip())
        if url.scheme in {"https", "http", "mailto", "tel", "data", "javascript"} or value.startswith("//"):
            continue
        if url.scheme:
            continue
        if url.path:
            if url.path.startswith("/"):
                errors.append(f"Ruta absoluta incompatible con Pages: {value}")
                continue
            target = (ROOT / unquote(url.path)).resolve()
            if not target.is_relative_to(ROOT):
                errors.append(f"Ruta fuera del proyecto: {value}")
                continue
            if not target.exists():
                errors.append(f"Recurso inexistente ({tag} {attr}): {value}")
        if url.fragment and not url.path and unquote(url.fragment) not in parser.ids:
            errors.append(f"Ancla inexistente: #{url.fragment}")
    if errors:
        print("ERROR: validación fallida:")
        for error in errors:
            print(" - " + error)
        return 1
    print(f"OK: estructura, IDs, anclas y {len(parser.links)} enlaces/recursos inspeccionados.")
    print("Nota: URLs externas, diseño, accesibilidad y formularios no se prueban aquí.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
