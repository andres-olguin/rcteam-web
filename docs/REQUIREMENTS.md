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
- El sitio original identifica a Rodrigo Cornejo S.M. y su foto, ahora recuperados en Team. Su cargo y los demás nombres, fotografías y cargos continúan por confirmar.
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

**Pendiente:** fotos y cargos del resto del equipo; sustitución posterior de algunas imágenes de fondo; validación final en dispositivos y aprobación antes de reemplazar rcteam.cl.
