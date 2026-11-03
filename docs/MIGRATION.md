# Plan de migración — rcteam.cl

## Procedencia
El respaldo importado conserva el trabajo freelance original; el rediseño se gestiona actualmente dentro de MasterTech SpA. La migración no implica asumir automáticamente derechos o responsabilidades legales de la versión original.

## Ambientes
- **GitHub Pages:** vista previa pública `https://andres-olguin.github.io/rcteam-web/`, independiente del sitio oficial, con `noindex`.
- **Producción:** `https://rcteam.cl`, hosting y configuración fuera del repositorio. **No se administra DNS desde GitHub Pages.**

## Inventario del sitio original (commit 62dc447)
- Encabezado con logo anterior y navegación de contacto.
- Perfil de Rodrigo Cornejo S.M. y presentación corporativa.
- Cinco servicios, logotipos de medios y referencia Declass.
- Correo, WhatsApp, dos teléfonos y formulario FormSubmit.
- `styles.css` y `script.js` originales preservados en el historial Git.

## Inventario del rediseño
- Hero editorial, agencia, cuatro etapas de ejecución, cinco servicios originales, metodología, mosaico de medios, referencias de medios, Declass, eficiencia, territorios, filosofía, Team y contacto.
- Nuevo logo negro/blanco comprimido.
- JS de menú, filtros y preparación de consulta por correo.
- Los textos y recursos de propuesta no acreditan aprobación de Rodrigo.

## Antes de reemplazar el sitio vigente
1. Conseguir aprobación escrita del diseño y contenido.
2. Confirmar los cinco servicios, logos de medios y participación en Declass.
3. Recibir fotos, nombres y cargos con autorización para publicación.
4. Confirmar correos, WhatsApp y teléfonos.
5. Resolver el mecanismo de formulario **real** (protección anti-spam, finalidad, datos tratados y aviso de privacidad revisado).
6. Optimizar la foto del perfil y recursos pesados; sustituir imágenes externas ilustrativas por material aprobado.
7. Auditar rutas internas, enlaces, contraste, teclado y SEO de producción.
8. Preparar una build de producción: retirar `noindex`, fijar canonical en `https://rcteam.cl/`, adaptar `og:url`, `og:image`, robots/sitemap y verificar metadatos.
9. Tomar copia de seguridad de archivos de hosting y documentar cómo revertir.
10. Coordinar ventana de publicación con Rodrigo; no alterar DNS ni alojamiento sin instrucción expresa.
11. Verificar HTTPS, recursos, enlaces, formulario y mobile en producción.
12. Registrar el commit exacto, fecha, aprobación y resultados.

## URLs y redirecciones
No hay evidencia de rutas internas adicionales indexadas. Antes de publicar, rastrear URLs existentes e indexación y conservar redirecciones necesarias. No inventar rutas 301.

## Responsables
- Rodrigo / RC Team: aprobación de contenido, credenciales de canales propios y material autorizable.
- MasterTech SpA: desarrollo, QA y preparación técnica.
- Hosting/dominio: responsables y accesos deben confirmarse antes de desplegar.

## Reversión
Si falla la publicación, restaurar archivos respaldados y limpiar caché; verificar que el dominio apunte al hosting original. Cualquier cambio de DNS necesita un plan separado.
