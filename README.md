# RC Team Chile — Sitio web editorial 2026

![Logotipo RC Team](assets/logo-rc-team-blanco.webp)

Sitio web corporativo de RC Team Chile, desarrollado por MasterTech SpA. Este repositorio contiene una **maqueta editorial responsive** para revisión con Rodrigo Cornejo y conserva la versión original importada en el historial Git.

**Estado:** rediseño implementado como propuesta; requiere revisión visual y aprobación del cliente. No está desplegado automáticamente en rcteam.cl.

## Enlaces
- Código: https://github.com/andres-olguin/rcteam-web
- Vista pública prevista: https://andres-olguin.github.io/rcteam-web/ (funcionará después de habilitar Pages y completar el workflow).
- Web oficial existente: https://rcteam.cl
- Diseño de referencia: imagen proporcionada directamente por Rodrigo (no es una orden de copia pixel a pixel).

## Contenido de la propuesta
- Portada de gran formato con nuevo logo y estética azul oscuro/cian.
- Estrategia y servicios: planificación, negociación, implementación y verificación.
- Cómo trabajamos: entender, conectar, activar y mejorar.
- Mosaico de medios con filtros: exterior, tradicionales y digital.
- Inversión, territorios, filosofía, Team y contacto.
- Team reservado para 4–5 fotografías/cargos reales, todavía **pendientes**.
- Formulario **de demostración**: abre un borrador en el cliente de correo; no envía mensajes por backend.
- Recursos externos de Unsplash son **ilustrativos** y no son campañas de RC Team.

## Tecnologías
HTML5, CSS3, JavaScript nativo y assets WebP. Sin Node, dependencias de producción ni proceso de compilación. La previsualización utiliza GitHub Pages.

## Estructura
- index.html — contenido y semántica.
- styles.css — sistema visual y breakpoints.
- script.js — menú, filtros, animación y correo.
- assets/ — variantes optimizadas del nuevo logo.
- images/ — recursos originales conservados.
- docs/ — alcance, diseño, assets, operación y QA.
- scripts/validate_site.py — verificación estática.
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
Leer docs/DEPLOYMENT.md. GitHub Pages se habilita inicialmente en Settings > Pages > Source > GitHub Actions, por el propietario del repositorio. La acción de despliegue no modifica rcteam.cl ni el DNS.

## Requisitos y control de calidad
- docs/REQUIREMENTS.md — decisiones y pendientes con Rodrigo.
- docs/DESIGN-SYSTEM.md — dirección visual, responsividad y accesibilidad.
- docs/QA-CHECKLIST.md — verificación manual y aprobación.
- docs/ASSETS.md — procedencia de logos e imágenes ilustrativas.

## Seguridad y permisos
Repositorio **público**: no subir credenciales, accesos al hosting, capturas privadas ni fotografías del equipo sin permiso de publicación. Se excluyen archivos .env en .gitignore. La marca y contenido del cliente no se relicencian por el hecho de mantener este repositorio.

**No presentar la demo como sitio oficial finalizado hasta obtener la aprobación de RC Team.**
