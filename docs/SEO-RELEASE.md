# SEO por ambiente — GitHub Pages vs producción

## Regla crítica
El archivo fuente \`index.html\` es una **maqueta pública** con:
- \`<meta name="robots" content="noindex,nofollow">\`
- \`og:url\` y \`og:image\` apuntando a GitHub Pages
- rutas de recursos **relativas**
- formulario de demostración y perfiles sin completar

Esto **no es un error** del ambiente de vista previa; evita que se indexe como un reemplazo de la página oficial. Una URL de preview no equivale a una web oficial.

## Script de compilación segura
Para la vista previa:

    python scripts/build_site.py --target preview --out dist/preview

La GitHub Action \`.github/workflows/pages.yml\` ejecuta ese mismo constructor para \`_site\` y **no** habilita SEO de producción.

Para una versión oficial, después de aprobación explícita y de completar las dependencias:

    python scripts/build_site.py --target production --approved-client-release --out dist/production

**El comando falla intencionalmente hoy:** la web aún contiene formulario demo, perfiles pendientes e imágenes ilustrativas externas. El parámetro de aprobación no ignora estos bloqueadores. NO se publica nada en \`rcteam.cl\` automáticamente.

Cuando se resuelvan, la exportación para producción:
- Sustituye \`noindex,nofollow\` por \`index,follow\`.
- Cambia \`og:url\`, \`og:image\` y \`twitter:image\` a \`https://rcteam.cl/\`.
- Inserta \`<link rel="canonical" href="https://rcteam.cl/">\`.
- Añade JSON-LD \`Organization\` para RC Team Chile con nombre, dominio, logotipo y correo público. No inventa dirección ni cargo societario.
- Crea \`robots.txt\` y \`sitemap.xml\` para la raíz de producción.

## Comprobación
Ejecutar:

    python -m unittest discover -s tests -p "test_seo.py" -v
    python scripts/validate_site.py

La validación de SEO prueba la transformación en memoria y garantiza que la preview conserva el bloqueo de indexación. No demuestra que Google haya indexado nada.

## Open Graph y redes sociales
La maqueta usa un logotipo WebP existente como miniatura. Funciona en la conversación de WhatsApp observada, pero una pieza de 1200×630 px aprobada por Rodrigo en PNG o JPEG sería una mejora futura para compartir en distintas plataformas. **No inventar un recurso ni señalar dimensiones que el archivo actual no tiene.**

## SEO y datos estructurados
- Elegir \`Organization\` mientras no exista una dirección física confirmada que justifique implementar \`LocalBusiness\`.
- No añadir dirección, número de empleados, fundador/cargo, reseñas ni resultados medibles sin fuente.
- Metadatos y schema no garantizan rankings; comprobar el dominio con herramientas del proveedor y Search Console al publicar.
- La comprobación de URLs indexadas y redirecciones requiere inventario real de producción.

## Portabilidad de rutas
Desde el \`index.html\` de la raíz se utiliza:

    <img src="assets/logo-rc-team-negro.webp" alt="RC Team">
    <a href="docs/presentacion.pdf">Descargar presentación</a>

La segunda ruta es válida **solo si** existe el archivo \`docs/presentacion.pdf\` en el mismo árbol publicado. En este proyecto no hay tal PDF; es un ejemplo, no un enlace real.

Si se mueve el HTML a \`vistas/index.html\` y \`assets/\` permanece en la raíz del proyecto, la ruta correcta pasa a ser:

    <img src="../assets/logo-rc-team-negro.webp" alt="RC Team">

El uso de rutas relativas es portable entre hosts **siempre que se conserve la estructura de directorios y la ubicación del HTML**. Mover \`index.html\` fuera de la raíz también afectaría el punto de entrada de GitHub Pages.

## Riesgos conocidos para el lanzamiento
Form endpoint real, protección anti-spam, información de privacidad y consentimiento; imágenes de terceros; logos de medios; fotografía grande de Rodrigo; contenido de Team; enlaces externos; OG social image especializada; revisión móvil de navegación y rendimiento.

Ver [MIGRATION.md](MIGRATION.md), [QA-CHECKLIST.md](QA-CHECKLIST.md) e Issue #7.
