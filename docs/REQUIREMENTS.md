# Requerimientos y decisiones — RC Team

## Origen
Conversación con Rodrigo Cornejo en octubre de 2026 y tres imágenes de referencia aportadas al proyecto en noviembre de 2026. El diseño es una **propuesta basada en referencias**, no una aprobación final del cliente.

## Acordado
- Rediseño editorial azul, negro y blanco, con bloques de scroll.
- Navegación Team (aprox. 4–5 personas con foto y cargo) y Contacto (sección inferior).
- Nuevo logotipo entregado en dos variantes: fondo negro y fondo blanco.
- Mantener calidad responsive para escritorio y teléfonos.
- Avances mediante una maqueta antes de alterar la web oficial.

## Implementado en la maqueta
- Nuevo logo en assets/.
- Hero, presentación de Agencia inmediatamente posterior, cuatro etapas de estrategia, cinco servicios originales, mosaico de Medios sin logos históricos, Declass con texto proporcionado por Rodrigo, Team y contacto.
- Eliminados expresamente por Rodrigo: metodología independiente, eficiencia, territorios y filosofía; botones de Declass y fila pública de logos históricos.
- Navegación responsive y filtros de tipos de medios.
- Formulario de demostración que abre borrador de correo, sin envío de producción.

## Pendiente
- Team: Rodrigo envió por WhatsApp la foto grupal (20-11-2026) y los retratos con nombre y cargo de cada integrante (23-11-2026). La maqueta los incorpora tal como figuran en los nombres de archivo enviados; ver sección «Team y Tres Mentes».
- Validar en GitHub Pages la maquetación de las correcciones v2 y las fotografías de fondo. Rodrigo indicó que enviará imágenes del equipo y posteriormente reemplazará algunas imágenes de fondo.
- Decidir si el formulario de producción conserva FormSubmit o usa otra solución.
- GitHub Pages quedó configurado el 3 de noviembre de 2026; revisar y aprobar visualmente la web y planificar despliegue posterior en rcteam.cl.
- Se retiraron de la página los logos históricos por instrucción directa. Conservar los archivos solo como respaldo. El texto sobre el proyecto Declass fue suministrado por Rodrigo y requiere su confirmación final antes de producción.
- Ver docs/CONTENT.md y docs/MIGRATION.md para distinguir contenido original de propuestas nuevas.

## Acuerdo comercial
Rodrigo y el desarrollador acordaron CLP 30.000 por el rediseño. No hay constancia de cobro o pago en este repositorio. Una futura web de importaciones fue mencionada como posibilidad aparte, no un proyecto contratado.

## Separación de ambientes
- main: fuente para preview mediante workflow de GitHub Pages.
- feat/* y otras ramas: trabajo y revisión con PR.
- rcteam.cl: producción independiente, solo con autorización.

## Fuera de alcance, salvo nuevo acuerdo
E-commerce, dashboard, CMS, backend, analítica sofisticada y nuevas campañas no especificadas.


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

**Pendiente:** sustitución posterior de algunas imágenes de fondo; validación final en dispositivos y aprobación antes de reemplazar rcteam.cl.

## Team y Tres Mentes — 25 de noviembre de 2026
Material recibido de Rodrigo por WhatsApp (los archivos originales no se suben al repositorio público, salvo los derivados web indicados en ASSETS.md):
- 20-11-2026: foto grupal del equipo («Te envío las fotos del equipo para ir avanzando»).
- 23-11-2026: retratos con nombre y cargo («Te envío foto y cargo de los integrantes del Team»):
  - Rodrigo Cornejo S.M. — Director General.
  - Ignacio Szalay B. — Desarrollo de Negocios y Medios.
  - Bárbara León G. — Ejecutiva de Medios.
  - Paz Palacios V. — Coordinadora de Administración.
  - Alejandra Fernández A. — Coordinadora de Finanzas.
- 24-11-2026: pidió incluir el logo de Tres Mentes en el pie, junto al de RC Team («RC Team / Tres Mentes»), y adjuntó el logo en JPEG y PNG transparente.

Decisiones de maqueta sin confirmación expresa del cliente: orden de las tarjetas (Director General primero), ubicación de la foto grupal sobre las tarjetas y versión clara del logo de Tres Mentes para el pie oscuro. El logo de Tres Mentes no enlaza a ningún sitio porque no se entregó URL.

Rodrigo también informó que reenvió por correo los accesos al hosting. Esos accesos no se registran en el repositorio y no autorizan por sí solos el despliegue en rcteam.cl.


## Ajuste hero laptop y Team — 25 de noviembre de 2026
Dirección revisó la preview en Opera (pantalla 1366×768, área útil ~1324×608) tras el PR #21: el CSS del PR #19 sí se aplicaba, pero el hero quedaba pequeño (titular 48 px) con una franja vacía bajo el CTA, y la foto grupal ocupaba casi toda la pantalla.
- Hero en laptops: ocupa el alto visible y el titular escala con la altura (65 px en ~1324×608). 1920×1080 y móvil sin cambios.
- Foto grupal junto al titular de Team, sin recorte.
- Footer: «Desarrollo web por MasterTech» (marca comercial, sin la forma jurídica).

## Correcciones de Rodrigo — 25 de noviembre de 2026 (12:29–12:32)
- «Qué hacemos» en el menú bajaba a la línea de etapas y no al inicio de la sección. El ancla `#servicios` pasa a la sección completa; todos los enlaces del menú dejan la etiqueta de sección a la misma distancia del header.
- Logo de Tres Mentes en el footer enlazado a https://tr3smentes.cl/ (URL enviada por Rodrigo), en pestaña nueva.

## Aprobaciones de Rodrigo — 25 de noviembre de 2026 (13:30–13:35, WhatsApp)
- «Todos los textos están aprobados.» Pidió eliminar tres párrafos laterales: «No se trata solo de aparecer…» (Qué hacemos), «Estas cinco áreas formaban parte…» (Servicios) y «Soluciones para llegar donde están tus audiencias.» (Medios). Eliminados.
- «El texto de Declass está confirmado.» Confirmación del cliente; MasterTech no lo ha verificado de forma independiente.
- Formulario: «está bien que llegue al correo (contacto@rcteam.cl), si también llega al WhatsApp +56993324792 genial». La preview ofrece ahora dos botones: borrador de correo a contacto@rcteam.cl y mensaje prellenado de WhatsApp (wa.me/56993324792). Ambos los envía el visitante. **Pendiente:** elegir el mecanismo de envío automático al correo para producción (servicio externo o script en el hosting); el bloqueador de producción del formulario se mantiene hasta entonces.
- 13:44–13:45: Rodrigo envió la imagen para reemplazar «la imagen grande». Se aplica al hero: collage y fondo, en lugar de la foto ilustrativa de Unsplash (calle con letreros). El mosaico de Medios conserva sus imágenes ilustrativas.
