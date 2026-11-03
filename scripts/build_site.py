#!/usr/bin/env python3
"""Build the RC Team preview safely; prepare production SEO only after approval.

The source index.html remains a *non-indexable GitHub Pages preview*.
Production is a separate, manual release artifact: never auto-deployed to rcteam.cl.
No third-party packages needed.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
PREVIEW_URL = "https://andres-olguin.github.io/rcteam-web/"
PRODUCTION_URL = "https://rcteam.cl/"
LOGO_PATH = "assets/logo-rc-team-negro.webp"
ROBOTS_PREVIEW = '<meta name="robots" content="noindex,nofollow">'
ROBOTS_PROD = '<meta name="robots" content="index,follow">'
SITE_FILES = ("index.html", "styles.css", "script.js")
SITE_FOLDERS = ("assets", "images")


def replace_exact(source: str, old: str, new: str) -> str:
    count = source.count(old)
    if count != 1:
        raise ValueError(f"Se esperaba exactamente 1 coincidencia, se encontraron {count}: {old!r}")
    return source.replace(old, new, 1)


def preview_is_safe(html: str) -> bool:
    return (
        ROBOTS_PREVIEW in html
        and f'<meta property="og:url" content="{PREVIEW_URL}">' in html
        and '<link rel="canonical" href="https://rcteam.cl/">' not in html
        and f'<meta property="og:image" content="{PREVIEW_URL}{LOGO_PATH}">' in html
    )


def production_seo_html(source: str) -> str:
    """Pure transform for validation; does NOT authorize production deployment."""
    html = replace_exact(source, ROBOTS_PREVIEW, ROBOTS_PROD)
    html = replace_exact(
        html,
        f'<meta property="og:url" content="{PREVIEW_URL}">',
        f'<meta property="og:url" content="{PRODUCTION_URL}">',
    )
    for prop in ("og:image",):
        html = replace_exact(
            html,
            f'<meta property="{prop}" content="{PREVIEW_URL}{LOGO_PATH}">',
            f'<meta property="{prop}" content="{PRODUCTION_URL}{LOGO_PATH}">',
        )
    html = replace_exact(
        html,
        f'<meta name="twitter:image" content="{PREVIEW_URL}{LOGO_PATH}">',
        f'<meta name="twitter:image" content="{PRODUCTION_URL}{LOGO_PATH}">',
    )
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": PRODUCTION_URL + "#organization",
        "name": "RC Team Chile",
        "url": PRODUCTION_URL,
        "logo": PRODUCTION_URL + LOGO_PATH,
        "description": "RC Team Chile: planificación de medios, estrategia, desarrollo de proyectos, innovación e investigación.",
        "email": "contacto@rcteam.cl",
    }
    # No invented postal address, founding date, staff positions, awards or revenue.
    schema = json.dumps(org, ensure_ascii=False, indent=2).replace("</", "<\\/")
    canonical_and_schema = (
        f'  <link rel="canonical" href="{PRODUCTION_URL}">\n'
        '  <script type="application/ld+json">\n'
        + schema + '\n  </script>\n'
    )
    html = replace_exact(html, '  <title>RC Team Chile | Estrategia de medios</title>',
                         '  <title>RC Team Chile | Estrategia de medios</title>\n' + canonical_and_schema.rstrip("\n"))
    if PREVIEW_URL in html:
        raise ValueError("La versión de producción conserva una URL del ambiente de prueba")
    return html


def production_blockers(source: str, javascript: str) -> list[str]:
    """Never package the public domain while the demo is unfinished."""
    blockers = []
    if 'class="demo-warning"' in source or 'id="contact-form" action="#"' in source:
        blockers.append("El formulario es una demo sin endpoint de producción")
    if 'class="team-placeholder"' in source:
        blockers.append("Quedan perfiles de equipo pendientes de aprobación")
    if "images.unsplash.com" in source:
        blockers.append("Quedan fotografías ilustrativas externas sin validar")
    if "mailto:contacto@rcteam.cl?subject=" in javascript:
        blockers.append("El JavaScript continúa preparando borradores de correo")
    return blockers


def build(target: str, destination: Path, approved: bool = False) -> None:
    source = (ROOT / "index.html").read_text(encoding="utf-8")
    javascript = (ROOT / "script.js").read_text(encoding="utf-8")
    if not preview_is_safe(source):
        raise ValueError("El HTML fuente debe conservar los metadatos seguros de preview")
    if target == "production":
        if not approved:
            raise ValueError("Producción requiere --approved-client-release, no solo SEO")
        blockers = production_blockers(source, javascript)
        if blockers:
            raise ValueError("Publicación bloqueada:\n- " + "\n- ".join(blockers))
        html = production_seo_html(source)
    elif target == "preview":
        html = source
    else:
        raise ValueError(f"Entorno desconocido: {target}")
    destination = destination.resolve()
    if destination in (ROOT, ROOT / "images", ROOT / "assets"):
        raise ValueError("Destino no permitido: no sobrescribir el proyecto ni los activos")
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "index.html").write_text(html, encoding="utf-8")
    for name in SITE_FILES:
        if name != "index.html":
            shutil.copy2(ROOT / name, destination / name)
    for folder in SITE_FOLDERS:
        shutil.copytree(ROOT / folder, destination / folder, dirs_exist_ok=True)
    (destination / ".nojekyll").touch()
    if target == "production":
        (destination / "robots.txt").write_text(
            "User-agent: *\nAllow: /\nSitemap: https://rcteam.cl/sitemap.xml\n", encoding="utf-8"
        )
        (destination / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            '<url><loc>https://rcteam.cl/</loc></url></urlset>\n', encoding="utf-8"
        )
    print(f"OK: entorno {target}, salida {destination}")
    if target == "preview":
        print("Preview con noindex. No enviar como web oficial aprobada.")
    else:
        print("REVISIÓN MANUAL OBLIGATORIA ANTES DE DESPLEGAR A rcteam.cl")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("preview", "production"), default="preview")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--approved-client-release", action="store_true",
                        help="Necesario además de resolver los bloqueadores técnicos")
    args = parser.parse_args()
    output = args.out or ROOT / "dist" / args.target
    try:
        build(args.target, output, approved=args.approved_client_release)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
