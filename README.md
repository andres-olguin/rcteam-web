# RC Team Chile — Sitio web editorial 2026

![Logotipo RC Team](assets/logo-rc-team-blanco.webp)

Sitio web corporativo de RC Team Chile. La base original procede de un trabajo freelance anterior; el rediseño editorial de 2026 se gestiona técnicamente en el marco de MasterTech SpA. Este repositorio contiene una **maqueta editorial responsive** para revisión con Rodrigo Cornejo y conserva la versión original importada en el historial Git.

**Estado:** rediseño implementado como propuesta; requiere revisión visual y aprobación del cliente. No está desplegado automáticamente en rcteam.cl.

## Enlaces
- Código: https://github.com/andres-olguin/rcteam-web
- Vista pública (GitHub Pages, vista previa): https://andres-olguin.github.io/rcteam-web/. Publicación verificada por GitHub Actions el 3 de noviembre de 2026.
- Web oficial existente: https://rcteam.cl
- Diseño de referencia: imagen proporcionada directamente por Rodrigo (no es una orden de copia pixel a pixel).

## Contenido de la propuesta
- Portada de gran formato con nuevo logo y estética azul oscuro/cian.
- Etapas operativas de la referencia: planificación, negociación, implementación y verificación; **servicios del sitio original** preservados: Planificación de Medios, Desarrollo de Estrategia, Desarrollo de Proyectos, Innovación e Investigación.
- Cómo trabajamos: entender, conectar, activar y mejorar.
- Mosaico de medios con filtros: exterior, tradicionales y digital.
- Sección Agencia con presentación anterior de RC Team, logos de medios del sitio original, referencia Declass, inversión, territorios, filosofía, Team y contacto.
- Rodrigo Cornejo S.M. figura con la fotografía original en Team. Los cargos y demás integrantes siguen **pendientes de validación**.
- Formulario **de demostración**: abre un borrador en el cliente de correo; no envía mensajes por backend.
- Recursos externos de Unsplash son **ilustrativos** y no son campañas de RC Team.

## Estrategia de contenido y UX

El sitio sigue una narrativa de **atención (Hero) → credibilidad (Agencia y Rodrigo) → oferta (servicios y medios) → evidencia (Declass) → personas (Team) → contacto**. El objetivo propuesto es facilitar que un visitante conozca la oferta antes de escribir, no afirmar conversiones medidas.

Las **cinco líneas de servicio del sitio original** se distinguen de las **cuatro etapas de trabajo de la referencia**. Así se explica qué hace RC Team y cómo propone abordar el trabajo, sin inventar cifras, casos de éxito o testimonios.

Ver [Estrategia de contenido y UX](docs/CONTENT-STRATEGY.md), incluyendo hipótesis de audiencia y decisiones por aprobar.

## SEO y ambientes

- **Vista previa Pages:** `noindex,nofollow` permanece en el HTML fuente.
- **Producción:** exportación manual con metadatos del dominio oficial (canonical, Open Graph, Twitter, JSON-LD `Organization`, robots y sitemap) únicamente después de aprobación y de resolver bloqueadores.
- `python scripts/build_site.py --target preview` genera la demo; `--target production --approved-client-release` está bloqueado mientras existan formulario demo, perfiles incompletos y fotos ilustrativas.
- No se modifica el DNS ni el alojamiento de `rcteam.cl`.

Ver [SEO y publicación](docs/SEO-RELEASE.md) y [Plan de migración](docs/MIGRATION.md).

## Tecnologías
HTML5, CSS3, JavaScript nativo y assets WebP. Sin Node ni dependencias de producción. Un constructor opcional en Python separa la vista previa de una exportación oficial y bloquea el lanzamiento incompleto. La previsualización utiliza GitHub Pages.

## Estructura
- index.html — contenido y semántica.
- styles.css — sistema visual y breakpoints.
- script.js — menú, filtros, animación y correo.
- assets/ — variantes optimizadas del nuevo logo.
- images/ — recursos originales conservados.
- docs/ — alcance, diseño, assets, operación y QA.
- scripts/validate_site.py — verificación estática.
- scripts/build_site.py — constructor y bloqueadores de producción.
- tests/test_seo.py — comprobación de SEO y aislamiento por ambientes.
- .github/workflows/validate.yml — validación de PR y main.
- .github/workflows/pages.yml — publicación de preview desde main.

## Desarrollar en Windows o en la universidad
Requisitos: Git, VS Code (u otro editor), navegador y Python 3 opcional para validación.

Comandos:

    git clone https://github.com/andres-olguin/rcteam-web.git
    cd rcteam-web
    python -m http.server 8000

Abrir http://localhost:8000.

Antes de empezar cualquier cambio:

    git switch main
    git pull --ff-only origin main
    git switch -c feat/nueva-mejora

Verificar con:

    python scripts/validate_site.py

Luego subir rama y abrir PR para revisión. No escribir directo a main en trabajos nuevos. Para actualizar una máquina después de una fusión:

    git switch main
    git pull --ff-only origin main

## Publicación
Leer docs/DEPLOYMENT.md. GitHub Pages utiliza el workflow de GitHub Actions. La habilitación inicial se realizó el 3 de noviembre de 2026; verificar siempre el resultado de la última ejecución. La acción de despliegue no modifica rcteam.cl ni el DNS.

## Requisitos y control de calidad
- docs/REQUIREMENTS.md — decisiones y pendientes con Rodrigo.
- docs/DESIGN-SYSTEM.md — dirección visual, responsividad y accesibilidad.
- docs/QA-CHECKLIST.md — verificación manual y aprobación.
- docs/ASSETS.md — procedencia de logos e imágenes ilustrativas.
- docs/CONTENT.md — qué contenido procede del sitio original y qué afirmaciones necesitan confirmación.
- docs/MIGRATION.md — inventario y plan para migrar a rcteam.cl sin modificar DNS.
- docs/SEO-RELEASE.md — SEO y publicación por ambiente.
- docs/CONTENT-STRATEGY.md — estrategia comercial, UX y validaciones.
- NOTICE.md — propiedad de marca y materiales de terceros.

## Seguridad y permisos
Repositorio **público**: no subir credenciales, accesos al hosting, capturas privadas ni fotografías del equipo sin permiso de publicación. Se excluyen archivos .env en .gitignore. La marca y contenido del cliente no se relicencian por el hecho de mantener este repositorio.

**No presentar la demo como sitio oficial finalizado hasta obtener la aprobación de RC Team.** El código original no debe atribuirse retrospectivamente como un trabajo contratado por la sociedad sin respaldo contractual.
