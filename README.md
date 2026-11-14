# RC Team Chile — Sitio web editorial 2026

![Logotipo RC Team](assets/logo-rc-team-blanco.webp)

Sitio web corporativo de RC Team Chile. La base original procede de un trabajo freelance anterior; el rediseño editorial de 2026 se gestiona técnicamente en el marco de MasterTech SpA. Este repositorio contiene una **maqueta editorial responsive** para revisión con Rodrigo Cornejo y conserva la versión original importada en el historial Git.

**Estado:** rediseño implementado como propuesta; requiere revisión visual y aprobación del cliente. No está desplegado automáticamente en rcteam.cl.

## Estado de entrega y decisiones pendientes

**Corte de revisión: 13 de noviembre de 2026.** La maqueta de GitHub Pages está publicada. Las correcciones de Rodrigo v2 se integran mediante un PR y requieren nuevas pruebas antes de fusionarse. **No equivale a la aprobación del cliente ni a la publicación oficial**.

| Entregable | Estado | Evidencia / siguiente paso |
| --- | --- | --- |
| Demo editorial y responsive | Implementada para revisión | [GitHub Pages](https://andres-olguin.github.io/rcteam-web/) |
| Validación estática, SEO y navegador | Automatizada | [GitHub Actions](https://github.com/andres-olguin/rcteam-web/actions) |
| Integrantes, cargos, contenido y permisos de medios | Pendiente cliente | [Issue #5](https://github.com/andres-olguin/rcteam-web/issues/5) |
| Formulario de producción y privacidad | Pendiente decisión/implementación | [Issue #6](https://github.com/andres-olguin/rcteam-web/issues/6) |
| Fotografía, rendimiento, SEO final y migración | Pendiente antes de producción | [Issue #7](https://github.com/andres-olguin/rcteam-web/issues/7) |
| Reglas obligatorias para proteger `main` | Pendiente configuración administrativa | [Issue #8](https://github.com/andres-olguin/rcteam-web/issues/8) |
| Aprobación de Rodrigo | No confirmada | Registrar aprobación y alcance antes del lanzamiento |
| Publicación oficial en `rcteam.cl` | **No autorizada ni ejecutada** | Requiere revisión y respaldo del hosting |

**Versionado previsto:** `v0.1.0-preview` cuando se publique formalmente una versión identificable de revisión; `v1.0.0-production` solo tras aprobación y despliegue real. No hay releases publicadas a la fecha del corte. No inventar fechas límite ni aceptar tácitamente el contenido del cliente.

Los detalles técnicos están en `docs/`; evitar crear documentos nuevos cuando corresponda actualizar uno existente.

## Enlaces
- Código: https://github.com/andres-olguin/rcteam-web
- Vista pública (GitHub Pages, vista previa): https://andres-olguin.github.io/rcteam-web/. Publicación verificada por GitHub Actions el 3 de noviembre de 2026.
- Web oficial existente: https://rcteam.cl
- Diseño de referencia: imagen proporcionada directamente por Rodrigo (no es una orden de copia pixel a pixel).

## Contenido de la propuesta
- Portada de gran formato con nuevo logo y estética azul oscuro/cian.
- Etapas operativas de la referencia: planificación, negociación, implementación y verificación; **servicios del sitio original** preservados: Planificación de Medios, Desarrollo de Estrategia, Desarrollo de Proyectos, Innovación e Investigación.
- Mosaico de medios con filtros: exterior, tradicionales y digital.
- Sección Agencia inmediatamente después del Home, seguida de servicios, medios, proyecto destacado Declass, Team y contacto. Los logos históricos de medios siguen archivados en el repositorio, pero Rodrigo ordenó retirarlos de la interfaz.
- Rodrigo Cornejo S.M. figura con la fotografía original en Team. Los cargos y demás integrantes siguen **pendientes de validación**.
- Formulario **de demostración**: prepara un borrador en el cliente de correo y conserva una copia visible para pegar en otro servicio si `mailto:` no abre una aplicación. Sin JavaScript muestra alternativas de contacto; no envía mensajes por backend.
- Recursos externos de Unsplash son **ilustrativos** y no son campañas de RC Team.

## Estrategia de contenido y UX

El sitio sigue una narrativa de **atención (Hero) → credibilidad (Agencia) → oferta (servicios y medios) → evidencia (Declass) → personas (Team) → contacto** según las correcciones v2 de Rodrigo. El objetivo propuesto es facilitar que un visitante conozca la oferta antes de escribir, no afirmar conversiones medidas.

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


## Correcciones v2 de Rodrigo — 13 de noviembre de 2026
Rodrigo entregó el archivo privado **CORRECCIÓN WEB RC TEAM v2.pptx** por WhatsApp. El archivo original no se incorpora al repositorio público. Las indicaciones se ejecutan únicamente sobre la vista previa: 
- Titular y texto principal del hero sustituidos; se elimina la línea de cobertura de medios.
- Agencia colocada inmediatamente después del home; se reemplaza el párrafo corporativo según el texto del cliente y se mantiene el titular no marcado.
- Se modifica el titular de servicios y el copy completo de las cuatro etapas.
- Se elimina la sección independiente «Cómo trabajamos».
- Se cambia el titular del mosaico de Medios; se retiran las referencias históricas de logos de la **interfaz**, pero los archivos permanecen en el historial y carpeta de respaldo.
- El proyecto Declass conserva su imagen, cambia titular y texto por el material enviado por Rodrigo, y elimina el botón externo.
- Se suprimen los bloques Eficiencia, Territorios y Filosofía.
- El cierre invita a conversar/café y al WhatsApp; se conserva el formulario de demostración, sin backend real.
- Se corrigió la proporción del logo del footer mediante la mejora visual previamente validada.

Las afirmaciones sobre Declass, la Embajada de Estados Unidos y los más de 23.000 documentos se transcriben **a solicitud de Rodrigo**. No se han verificado de forma independiente; el cliente es responsable de confirmar la exactitud y autorización comercial antes de producción.

**Pendiente:** fotos y cargos del resto del equipo; sustitución posterior de algunas imágenes de fondo; validación final en dispositivos y aprobación antes de reemplazar rcteam.cl.

**No presentar la demo como sitio oficial finalizado hasta obtener la aprobación de RC Team.** El código original no debe atribuirse retrospectivamente como un trabajo contratado por la sociedad sin respaldo contractual.
