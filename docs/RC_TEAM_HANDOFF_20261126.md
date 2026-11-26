# RC Team Chile — Contexto integral de desarrollo y traspaso

**Fecha del corte:** 26 de noviembre de 2026. **Repositorio:** andres-olguin/rcteam-web. **Este documento describe el historial y una fotografía del estado verificado en la fecha del corte; no sustituye el historial Git ni la confirmación comercial del cliente.**

## 1. Empresa, cliente y entornos

- Desarrolladora: MasterTech SpA (marca pública MasterTech Technology).
- Cliente y contraparte: Rodrigo Cornejo, RC Team Chile.
- Dominio oficial: https://rcteam.cl/ — **no se modifica ni se despliega automáticamente**.
- Repositorio: https://github.com/andres-olguin/rcteam-web
- Vista previa: https://andres-olguin.github.io/rcteam-web/
- Correo de RC Team: contacto@rcteam.cl
- La versión en GitHub Pages es una **preview no indexable**, no el lanzamiento oficial.

## 2. Objetivo y línea visual

Rediseño editorial, corporativo y responsive para RC Team Chile: azul oscuro, azul eléctrico, cian, blanco; titulares contundentes, fotografías ligadas a medios y publicidad, collage del hero, navegación adaptable, foco en claridad comercial y accesibilidad. Preservar logo, fotografías y contenido originados o aprobados por Rodrigo; no inventar testimonios, clientes, cargos ni cifras.

La arquitectura del relato comercial está organizada como: **Hero → Agencia → Qué hacemos → Medios → Declass → Team → Contacto**. El diseño debe funcionar tanto en pantallas de laptop con área útil reducida como en monitores grandes y móviles. No tomar los tests automáticos por sustituto de inspección visual real.

## 3. Contenido pedido por Rodrigo y correcciones v2

La presentación original de correcciones denominada «CORRECCIÓN WEB RC TEAM v2.pptx» dio lugar al PR #14.

- **Hero:** “Conocemos los medios. Vamos más allá de la pauta.” Descripción: “Planificamos, negociamos y desarrollamos estrategias de medios que conectan marcas con oportunidades, optimizando cada inversión.” CTA de contacto y exploración de servicios.
- **Agencia:** inmediatamente después del hero; “La experiencia no se promete. Se demuestra en cada proyecto.”
- **Qué hacemos:** cuatro etapas, planificación, negociación, implementación y verificación; conservar servicios históricos diferenciados.
- **Medios:** collage/mosaico de seis medios con filtros; retirar de la interfaz la franja de logos históricos de terceros.
- **Declass:** proyecto destacado; eliminar botón externo; las afirmaciones sobre instituciones y documentación requieren verificación documental por el cliente antes de producción.
- **Team:** se inició como contenido por confirmar. **Actualización al 25-11:** PR #21 incorporó fotografías/nombres del equipo; consultar el HTML y la aprobación vigente antes de declarar pendientes.
- **Contacto:** invitación a conversar; correo contacto@rcteam.cl; mensajería por WhatsApp. **Actualización al 25-11:** PR #25 añadió una ruta de WhatsApp desde el formulario y textos aportados por Rodrigo; no equivale a backend de envío automatizado.

Eliminar/evitar reintroducir secciones que Rodrigo había quitado: sección autónoma «Cómo trabajamos», franja histórica de logotipos, y contenidos «Eficiencia», «Territorios», «Filosofía».

## 4. Tecnología y estructura

HTML5, CSS3, JavaScript nativo y optimización WebP, con Python 3 para build y validación. Fuentes principales: index.html, styles.css, script.js. Constructor: scripts/build_site.py. Validación: scripts/validate_site.py. Pruebas: tests/test_browser.py, tests/test_seo.py. Documentación: README.md, docs/REQUIREMENTS.md, CONTENT.md, DESIGN-SYSTEM.md, ASSETS.md, SEO-RELEASE.md, QA-CHECKLIST.md. Publicación de preview mediante .github/workflows/pages.yml.

GitHub Pages debe conservar meta robots noindex,nofollow. Producción requiere autorización y verificación de bloqueadores de build. Nunca confundir GitHub Pages con rcteam.cl.

## 5. Flujo multiagente

Se utilizaron Codex, Claude y Antigravity con ramas independientes en un solo repositorio y worktrees hermanos: main, codex, claude, antigravity. El estándar operativo referido es MTS-ENG-001, documentado en el repositorio corporativo de gobernanza (verificar su vigencia con Dirección).

- Codex: implementación técnica, QA, accesibilidad, scripts y pruebas.
- Claude: auditoría, revisión de arquitectura y hallazgos técnicos.
- Antigravity: revisión visual, capturas, responsive y pruebas de geometría.
- Git y CI: PR, verificaciones, revisión humana, después integración a main.
- No escribir en worktrees ajenos, no fusionar sin autorización, no desplegar producción por accidente.
- Limitación histórica: un sandbox restringido impedía escribir en metadatos Git compartidos bajo main/.git. Se resolvió para una integración con permisos mayores, que no deben ser la configuración por defecto.

## 6. Hitos históricos de pull requests

- **#12:** pulido visual/responsive de la base.
- **#14:** incorporación de las correcciones editoriales v2 de Rodrigo.
- **#15:** integración visual del logo y favicon y distribución de Medios.
- **#16:** auditoría técnica de Codex, commit cfc93cd; correcciones de overflow, navegación sin JS, formulario demo, optimización WebP de Rodrigo/Declass, validación de recursos y pruebas. Cerrado como reemplazado por #18.
- **Auditoría Claude sobre #16:** detectó menú móvil que podía parpadear antes de ejecutar script diferido; supuesto POST de respaldo sin endpoint real; documentación que afirmaba que no existían commits/PR. Recomendó inline JS temprano, noscript, corregir el formulario/documentación.
- **#17:** revisión Antigravity, commit 6d01de9; resolvió superposición entre Radio/Audio y «01 / Conectar» a 1024 px, mejoró microetiquetas, balanceó filtros. Cerrado como reemplazado por #18.
- **#18:** integración de #16 y #17 más correcciones, commit de rama c4fc601, squash a main 458fae593c9d8014922286a8ec983b027af4a390. Tests locales reportados 32/32, CI pasó, axe sin infracciones detectadas en viewports comprobados. Agregó aviso noscript y borrador copiable.
- **#19:** compactación hero para laptops, commit de rama a85f3db, squash a main 837f05bc27046d1852880261dc15718e36c8ab15; viewport de laptop recibió ajustes de tipografía, paddings y collage. CI pasó.
- **#20:** invalidación de caché CSS/JS en build mediante huella del contenido, para evitar CSS antiguo en navegadores. Consultar estado actual antes de actuar.
- **#21:** equipo confirmado y logo Tres Mentes en footer.
- **#22:** hero de pantalla completa en laptops, foto grupal compacta y crédito MasterTech; por tanto **las reglas del PR #19 fueron revisadas posteriormente**.
- **#23:** anclas de servicios/“Qué hacemos” y enlace logo Tres Mentes.
- **#24:** «Volver arriba» y logos vuelven al principio.
- **#25:** textos recibidos/aprobados por Rodrigo y opción WhatsApp del formulario.
- **#26:** imagen de hero enviada por Rodrigo.
- **#27:** collage del hero con fotografía de pantalla en carretera.
- **#28:** collage más nítido sin velo oscuro.
- **#29:** etiquetas de etapas de trabajo en una sola línea en celular y tablet.

Los PR #21–#29 son posteriores al contexto histórico del 14-11. No revertirlos siguiendo instrucciones antiguas sin revisar primero el código actual y los comentarios/aprobaciones del cliente.

## 7. Historia del problema responsive del hero

Dirección observó en una laptop con Opera que el título del hero se veía excesivamente grande y el CTA quedaba fuera de la primera pantalla. Las capturas iniciales mostraban una altura útil limitada por barras del navegador y Windows. Antigravity agregó reglas combinadas de ancho y alto en #19 y reportó cambios de 882 a 560 px de alto en un viewport simulado 1366×610, sin reducir la versión de 1920×1080. Dirección indicó que en su navegador real aún se veía igual.

Se consideró posible caché: el HTML referenciaba styles.css sin versión. En DevTools se probó manualmente añadir una query ?v=837f05bc. La captura de la consola de esa prueba estaba en **modo responsive 761×522**; esa simulación cae en el breakpoint móvil/tablet, por lo que **no prueba** cómo se ve realmente la laptop a ancho CSS mayor de 850 px. Se pidió comprobar window.innerWidth/innerHeight, zoom, computed styles y media queries en la ventana real. No se recibió esa medición en aquel momento.

La investigación original quedó superada en parte por PR #20 y las mejoras visuales posteriores #22–#29. Si reaparece un problema, inspeccionar el sitio **actual**, CSS efectivamente servido, escala, zoom y viewport reales antes de modificar estilos.

## 8. Estado verificado en GitHub (26-11-2026)

- **main HEAD:** 40e441263fe6d106437fc56bcfe5442136fffcf5 (PR #29).
- En main ya existen fotografías del equipo, nuevos activos locales del hero, ajustes de laptop posteriores al PR #19, imagen aportada por Rodrigo, textos actualizados y opción WhatsApp de contacto.
- Los archivos antiguos del ZIP se conservan en backups/rc-team-original-20261126/ como respaldo byte a byte; no reemplazan la web actual.
- El README y algunos Issues antiguos conservan un corte previo, por lo que pueden contener frases desactualizadas sobre Team, fotos o formulario. Distinguir documentación histórica y estado vivo del HTML/commits.
- Verificar el estado presente de CI, Pages y cualquier PR antes de tomar decisiones: el estado mostrado es un corte, no una autorización permanente de despliegue.

## 9. Estado del formulario

- En la preview, la opción de correo prepara un mailto con asunto/cuerpo; dispone de contenido copiable como respaldo.
- La opción WhatsApp crea un enlace wa.me con mensaje prellenado y pide al usuario completar el envío.
- No se ha demostrado un servicio backend enviando y almacenando solicitudes.
- Enlaces de WhatsApp y número deben verificarse con la confirmación de Rodrigo y su configuración actual.
- El formulario oficial deberá someterse a revisión de privacidad, antispam, consentimiento y prueba funcional antes de activarse en rcteam.cl.

## 10. Trabajo pendiente y controles

Los issues públicos originales #5, #6 y #7 siguen abiertos según consulta de corte, pero algunos puntos sobre equipo y fotografías se han resuelto en PR más recientes. Actualizar checklist/Issues con evidencias, sin cerrar asuntos parcialmente resueltos ni asumir autorizaciones.

Antes de despliegue oficial: aprobación explícita de Rodrigo de la versión final y contenido; licencias de imágenes y logos; respaldo completo del sitio vigente en rcteam.cl; confirmación de accesos, hosting y document root; formulario real/privacidad; SEO de producción y redirecciones; QA responsive y accesibilidad en el dominio oficial; plan de reversión. Nunca actualizar DNS/hosting por una mera corrección CSS.

## 11. Evidencia y prioridades

Históricamente se ejecutaron validate_site.py, pruebas Selenium/Playwright Chromium y axe-core; se generaron capturas 320–1920 px, se comprobó teclado, Escape, reduced-motion, menú, filtros, imágenes, enlaces y geometría. No confundir «sin infracciones automatizadas» con certificación WCAG completa, ni «CI verde» con aprobación comercial.

Prioridad al continuar: inspeccionar el estado actual de main y la experiencia visual real de Rodrigo/Dirección; regularizar documentación e Issues desactualizados; obtener aprobación expresa de publicación y revisar el plan para rcteam.cl.

## 12. Notas de comunicación

Mantener comunicación en español claro, concreta y no robótica. Documentar quién aprobó qué, evitando prometer fechas sin evidencia. Para mensajes de WhatsApp al cliente, escribir breve, natural y sin listas artificiosas. No introducir contenido o testimonios que Rodrigo no haya aprobado.

## 13. Enlaces de referencia

- Repositorio: https://github.com/andres-olguin/rcteam-web
- Vista previa: https://andres-olguin.github.io/rcteam-web/
- Producción: https://rcteam.cl/
- Historial de PR: https://github.com/andres-olguin/rcteam-web/pulls
- Validaciones CI: https://github.com/andres-olguin/rcteam-web/actions
- Respaldo histórico íntegro: backups/rc-team-original-20261126/README.md

**Nota de procedencia:** este documento consolida el contexto de gestión trabajado en conversación y verifica los hechos de GitHub de la fecha de corte. No es transcripción textual del chat completo; no incluye datos privados ajenos al proyecto ni contraseñas.
