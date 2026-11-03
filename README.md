# RC Team Chile — Sitio web

Repositorio de desarrollo y mantenimiento del sitio de **RC Team Chile**, gestionado técnicamente por **MasterTech SpA**.

> **Estado:** versión original importada el 3 de noviembre de 2026. El rediseño editorial solicitado por Rodrigo Cornejo está **pendiente**, no publicado ni aprobado. No confundir este repositorio con evidencia de que la nueva versión esté terminada.

## Enlaces

- Sitio oficial: https://rcteam.cl
- Código: https://github.com/andres-olguin/rcteam-web
- Vista de GitHub Pages (solo cuando esté habilitada): https://andres-olguin.github.io/rcteam-web/

## Tecnología

Sitio estático: HTML5, CSS3 y JavaScript sin framework ni compilación. Fuentes Poppins (Google Fonts), iconos Font Awesome desde CDN y formulario de contacto mediante FormSubmit (servicio externo).

## Estructura

```text
/
├── index.html               # Página principal
├── styles.css               # Diseño y responsive
├── script.js                # Interacciones y animaciones
├── images/                  # Recursos gráficos
├── docs/                    # Requisitos y operaciones
├── scripts/                 # Validaciones sin dependencias
└── .github/workflows/       # Integración continua
```

## Trabajar desde Windows o la universidad

Requisitos: Git, navegador y un editor como VS Code; Python 3 es opcional para validación.

```powershell
git clone https://github.com/andres-olguin/rcteam-web.git
cd rcteam-web
python -m http.server 8000
```

Visitar http://localhost:8000 y detener con Ctrl+C. Como alternativa, abrir `index.html` directamente; el servidor local reproduce mejor las rutas del sitio.

Para comenzar una modificación: `git switch main`, `git pull --ff-only`, `git switch -c feat/nombre-cambio`. Al terminar: `python scripts/validate_site.py`, `git add .`, `git commit -m "feat: descripcion"`, `git push -u origin feat/nombre-cambio` y abrir un pull request contra `main`. **No cambiar directamente main.**

## Validación

```powershell
python scripts/validate_site.py
```

Comprueba estructura básica, recursos relativos y destinos internos del HTML. **No reemplaza** pruebas visuales, de accesibilidad, de enlaces externos ni pruebas reales del formulario.

## Publicación y revisión

La configuración de GitHub Pages se describe en [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). La vista de Pages debe tratarse como un entorno público de revisión, no como la producción de `rcteam.cl`. Antes de demostrar el sitio al cliente, verificar visualmente escritorio y móvil.

## Alcance del rediseño

Consultar [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md). Referencia editorial azul/negro, navegación Team y Contacto, equipo de 4–5 integrantes por confirmar y nuevo logo pendiente de integrar. **Los contenidos nuevos requieren material y validación del cliente.**

## Seguridad y contenido

No introducir accesos de hosting, credenciales, tokens, respaldos privados ni información personal no autorizada. El repositorio es público. **No realizar envíos de prueba del formulario de contacto** sin coordinación con el destinatario.

## Responsabilidades

RC Team Chile es el sitio del cliente. MasterTech SpA presta servicios de desarrollo y mantenimiento; la autoría técnica no implica propiedad de la marca, imágenes ni contenidos de RC Team. Las entregas deben aprobarse antes de publicar en el dominio oficial.
