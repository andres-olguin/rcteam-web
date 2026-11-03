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
- Hero, estrategia, presentación de agencia, servicios originales, metodología, medios, logos de medios originales, Declass, eficiencia, territorios, filosofía, Team y contacto.
- Navegación responsive y filtros de tipos de medios.
- Formulario de demostración que abre borrador de correo, sin envío de producción.

## Pendiente
- El sitio original identifica a Rodrigo Cornejo S.M. y su foto, ahora recuperados en Team. Su cargo y los demás nombres, fotografías y cargos continúan por confirmar.
- Aprobar imágenes ilustrativas, textos y composición definitiva.
- Decidir si el formulario de producción conserva FormSubmit o usa otra solución.
- GitHub Pages quedó configurado el 3 de noviembre de 2026; revisar y aprobar visualmente la web y planificar despliegue posterior en rcteam.cl.
- Confirmar qué logos de medios pueden mostrarse públicamente y el vínculo exacto con Declass.
- Ver docs/CONTENT.md y docs/MIGRATION.md para distinguir contenido original de propuestas nuevas.

## Acuerdo comercial
Rodrigo y el desarrollador acordaron CLP 30.000 por el rediseño. No hay constancia de cobro o pago en este repositorio. Una futura web de importaciones fue mencionada como posibilidad aparte, no un proyecto contratado.

## Separación de ambientes
- main: fuente para preview mediante workflow de GitHub Pages.
- feat/* y otras ramas: trabajo y revisión con PR.
- rcteam.cl: producción independiente, solo con autorización.

## Fuera de alcance, salvo nuevo acuerdo
E-commerce, dashboard, CMS, backend, analítica sofisticada y nuevas campañas no especificadas.
