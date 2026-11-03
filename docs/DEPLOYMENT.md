# GitHub Pages y publicación de producción

## 1. Vista de demostración (Pages)
Este sitio es estático y puede desplegarse desde `main` sin compilación.

1. Abrir **Settings > Pages** en el repositorio.
2. Seleccionar **Deploy from a branch**, rama **main**, carpeta **/(root)** y guardar.
3. Comprobar el enlace mostrado por GitHub. La URL habitual es `https://andres-olguin.github.io/rcteam-web/`, **solo cuando Pages esté realmente activo**.
4. Esperar confirmación del workflow/deploy y probar navegación, CSS, JS, imágenes y enlaces en esa URL.
5. Verificar que imágenes, CSS y JS usen rutas relativas, sin anteponer `/`, para funcionar en la subruta.

**Importante:** Pages es público; no incorporar credenciales, contenido sensible ni materiales no autorizados. La vista previa podría ofrecer un formulario real que envía a `contacto@rcteam.cl`: evitar pruebas enviadas sin coordinación.

## 2. Cambios y control de calidad
- Cada cambio se desarrolla en rama propia con PR y revisión.
- Ejecutar `python scripts/validate_site.py` y revisar la vista previa manualmente.
- Una rama no aparece automáticamente en el Pages servido desde `main`.
- Al fusionar cambios aprobados a `main`, se actualiza la vista de Pages si está configurada.

## 3. Sitio oficial rcteam.cl
**No desplegar automáticamente desde GitHub Pages ni cambiar DNS.** El hosting real y sus accesos son independientes.

Antes de subir cambios a producción:
1. Obtener aprobación expresa del cliente.
2. Guardar respaldo de archivos existentes del hosting.
3. Confirmar dominio, certificado HTTPS, rutas, favicon y formularios.
4. Subir los archivos mediante el procedimiento autorizado para el proveedor del hosting.
5. Verificar versión móvil y escritorio, accesos y funcionamiento de contacto con autorización.
6. Registrar fecha, commit y resultado de despliegue; tener plan de reversión con el respaldo.

## 4. Trabajo en otra computadora
```powershell
git clone https://github.com/andres-olguin/rcteam-web.git
cd rcteam-web
git switch main
git pull --ff-only
git switch -c feat/nueva-seccion
```
Para sincronizar una rama existente: `git fetch origin` y `git switch nombre-rama`; evitar copiar carpetas manualmente.
