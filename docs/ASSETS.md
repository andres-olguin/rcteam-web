# Registro de recursos gráficos

## Logotipos
- assets/logo-rc-team-negro.webp: derivado del archivo enviado "Nuevo logo RC Team fondo negro.png".
- assets/logo-rc-team-blanco.webp: derivado del archivo enviado "Nuevo logo RC Team fondo blanco.png".
- Uso exclusivamente para la web de RC Team; no implica permiso para utilizar su marca en otros productos.

## Imágenes de demostración
Se sirven desde images.unsplash.com bajo https://unsplash.com/license. Su uso aquí es editorial e ilustrativo: no son campañas ni clientes atribuidos a RC Team.

Fotografías empleadas por ID:
- 1771076402741-c4220c3c4748: ciudad / publicidad exterior.
- 1590602847861-f357a9332bbc: radio.
- 1516321318423-f06f85e504b3: digital.
- 1642789665204-80f5131ae4db: prensa.
- 1497366811353-6870744d04b2: oficina.
- 1519501025264-65ba15a82390: ciudad.
- 1477959858617-67f85cf4f1df: skyline.

Antes de publicación oficial, revisar con Rodrigo y reemplazar elementos de demostración según su material aprobado. No publicar imágenes privadas sin consentimiento.


## Recursos procedentes de la web original
- `images/PERFIL.png`: foto mostrada junto al nombre de Rodrigo Cornejo S.M.; requiere optimización antes de producción (aprox. 7.4 MB en el repositorio).
- `images/declass.jpg` y `images/declassmobile.png`: material visual del proyecto Declass de la versión original.
- Logotipos de medios en `images/`: Pauta, Mega, TXS, Infinita, El Mostrador, The Clinic, Tele13, Cooperativa, Emol y otro archivo sin identificar `diario.png`.

Su presencia en el sitio anterior no confirma relación contractual, patrocinios ni licencias de reproducción. Validar con Rodrigo antes del lanzamiento oficial.


## Correcciones editoriales v2
Por instrucción del cliente se retiró de la página la franja de logos históricos. Los archivos originales continúan en `images/` como respaldo, pero ya no se muestran en GitHub Pages. Rodrigo anunció el envío de fotos del equipo y la futura sustitución de algunas imágenes de fondo; el material aún está pendiente.

## Integración de la marca y favicon — revisión 13-11-2026
- El logotipo original de Rodrigo conserva un rectángulo negro en el archivo. La vista previa aplica un filtro SVG `#rc-black-to-alpha` a header y footer, que convierte el negro de fondo en transparencia **sin redibujar la marca**. El archivo original sigue disponible como respaldo.
- `assets/favicon-rc-team.svg` contiene el isotipo RC extraído del archivo facilitado por el cliente, incorporado como imagen PNG transparente dentro del SVG para uso de navegador. Sustituye en la maqueta el favicon antiguo de `images/favicon.ico`, que permanece archivado.
- Verificar el favicon sin caché y la apariencia del logotipo sobre los distintos tonos del encabezado antes de producción; el filtro fue validado visualmente en Chromium con el archivo fuente original.
- El mosaico de seis medios cambió su grilla para ocupar completamente las dos filas de escritorio y evitar huecos blancos.
