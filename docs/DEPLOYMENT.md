# Previsualización en GitHub Pages y producción

## GitHub Pages (primer uso)
1. En https://github.com/andres-olguin/rcteam-web/settings/pages ir a Build and deployment.
2. Elegir Source: **GitHub Actions**.
3. El workflow .github/workflows/pages.yml se dispara al hacer push a main o mediante Run workflow en Actions.
4. Revisar que la acción "Publish preview to GitHub Pages" finalice en verde.
5. Verificar https://andres-olguin.github.io/rcteam-web/ y probar escritorio, móvil, enlaces, menús, filtros e imágenes.

**La configuración inicial requiere acceso administrativo** al repositorio. No afirmar que Pages está activo solo porque exista el workflow. El workflow no usa credenciales de hosting ni afecta el DNS.

## Vista previa
- Se empaquetan únicamente index.html, styles.css, script.js, images/ y assets/.
- Rutas relativas para subruta /rcteam-web/.
- Etiqueta noindex para que buscadores no traten la vista de revisión como web oficial.
- El formulario no envía por backend: abre un borrador de correo con los datos que introduce la persona.

## Producción: rcteam.cl
No se publicará automáticamente desde este repo.
1. Obtener aprobación final de Rodrigo.
2. Sustituir perfiles pendientes y material ilustrativo según indicación.
3. Definir formulario de producción (sin confiar en el borrador de preview).
4. Crear respaldo de los archivos existentes del hosting.
5. Comprobar seguridad, HTTPS, correo, DNS, links y favicon.
6. Publicar mediante el acceso autorizado al hosting.
7. Quitar noindex solo en la versión de producción y validar el formulario.
8. Registrar fecha, commit, evidencia y procedimiento de rollback.

## Trabajo entre computadores
Para un nuevo dispositivo usar git clone. Para sincronizar main: git switch main y git pull --ff-only origin main.
Para cambios, abrir ramas con git switch -c feat/descripcion, correr python scripts/validate_site.py, push y PR.

## Checklist
Consultar docs/QA-CHECKLIST.md. La validación automática no demuestra que todos los navegadores y tamaños sean correctos.
