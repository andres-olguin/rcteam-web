# Validación de entrega — RC Team

## Integración final en claude — 14 de noviembre de 2026

- Rama `fix/rc-team-integracion-final-20261114` creada desde `origin/main` (`78af801`), con árbol limpio y sin otra integración activa ni locks pendientes. Trabajo exclusivo en `claude`; no se cambiaron los otros worktrees.
- Se combinaron por squash los cambios de PR #16 (`cfc93cd`) y #17 (`6d01de9`). La aplicación de tres vías fue limpia; se conservan las mejoras técnicas y visuales y se elimina solo una regla CSS duplicada.
- Se inicializa la clase `js` en el head antes de cargar CSS para evitar el parpadeo del menú móvil. Sin JS sigue visible la navegación y se oculta el formulario inoperante; el aviso `<noscript>` ofrece alternativas reales de contacto.
- El borrador queda disponible en un campo de solo lectura para copiar destinatario, asunto y mensaje, más un enlace de reintento de `mailto:`. No se afirma que el correo se haya enviado. README y riesgos SEO actualizados; POST no se documenta como respaldo funcional.
- Python portátil 3.11.9, Playwright 1.65.2, Chromium 159 y axe-core 4.10.3 instalados dentro de `artifacts/tools/`, ignorado por Git. Se usó `artifacts/tools/runtime/python.exe` en lugar del alias de Windows. Variables locales: `PLAYWRIGHT_BROWSERS_PATH=artifacts/tools/browsers` y `AXE_CORE_PATH=artifacts/tools/axe.min.js` (rutas absolutas al ejecutar).
- `python scripts/validate_site.py`: **correcto, 39 referencias**. `python scripts/build_site.py --target preview`, `node --check script.js` y `git diff --check`: **correctos**.
- `python -m unittest discover -s tests -p "test_*.py" -v`: **32 pruebas aprobadas, sin omisiones**, salida 0 (239,995 s). Incluye las ocho pruebas SEO, responsive, teclado, foco, reduced-motion, menú, filtros, imágenes y anclas, formulario y respaldo copiable. Registro: `artifacts/integration-tests.txt`. El intento previo se detuvo por Chromium aún no instalado; se repitió completa tras instalarlo.
- Axe WCAG 2 A/AA y 2.1 A/AA: **cero infracciones** a 390 y 1280 px (`artifacts/axe-390.json`, `artifacts/axe-1280.json`).
- Responsive automatizado y capturas con fuentes e imágenes cargadas a 320, 375, 390, 570, 768, 850, 1024, 1280 y 1920 px. Inspección visual de 320, 375, 768, 1024, 1280 y 1920 px: sin desbordamiento horizontal. Capturas: `artifacts/rc-team-<ancho>.png`.
- Hero: sin intersecciones móviles a 320, 375 y 570 px; separación de al menos 16 px entre leyenda y ambas tarjetas a 850, 851, 900, 1024, 1100, 1140 y 1280 px.
- Preview compilada bajo `/dist/preview/`: imágenes decodificadas, noindex preservado, contenido visible con animación normal, sin desbordamiento a 375 px y cero errores JavaScript. Comprobación local: `artifacts/check_preview.py`.
- Diff y archivos revisados sin secretos detectados ni materiales ajenos al alcance. Branding y originales conservados. No se enviaron mensajes ni se activó backend.
- Límites: no Safari/Firefox, dispositivos físicos, lector de pantalla humano, Lighthouse ni apertura/envío real desde una aplicación de correo. Las verificaciones locales no acreditan aprobación comercial; siguen pendientes los Issues #5–#7. No se fusiona `main`, no se despliega producción ni se cambia DNS/hosting.

## Auditoría técnica local — 14 de noviembre de 2026

Revisión de `AGENTS.md`, HTML/CSS/JS, constructor, validación, pruebas, recursos, documentación y workflows. Base: `78af801`. Trabajo en la rama existente de Codex `ai/codex/rc-team-final-20261113`, con árbol inicialmente limpio. No se modificaron `main`, hosting, DNS ni configuración remota.

### Hallazgos corregidos

| Hallazgo | Corrección y evidencia |
| --- | --- |
| Desbordamiento de 17 px a 320 px cuando no cargan las fuentes externas | Tarjetas de estrategia con `min-width:0` y ajuste de palabras; regresión bloqueando Google Fonts. |
| Leyenda del collage tapada por la tarjeta de audio en móvil | Reubicación dentro de la imagen; prueba de intersecciones en 320, 375 y 570 px. |
| Menú móvil inaccesible sin JavaScript | Navegación visible como alternativa sin JS; prueba de visibilidad del enlace Team. |
| Campos obligatorios aceptaban solo espacios y fallaban sin explicación | Validación nativa personalizada, corregible al escribir; prueba de rechazo y posterior borrador válido. |
| Foto de Rodrigo y Declass móvil demasiado pesadas | Variantes WebP derivadas, sin cambiar contenido ni eliminar originales; detalle en ASSETS.md. |
| Constructor permitía escribir dentro de carpetas fuente o sobre un ancestro | Rechazo previo a escritura de destinos protegidos; regresión automatizada. |
| Preview podía reutilizar robots/sitemap de una exportación oficial anterior | Rechazo de destino con esos archivos; prueba que verifica que no se escribe HTML. |
| Validador omitía rutas de `source srcset` | Inspección de candidatos de imágenes; regresión y 37 referencias revisadas. |
| QA de formulario no comprobaba comportamiento; axe ignoraba infracciones graves | Prueba del `mailto:` y su codificación, campos inválidos, teclado, cambio de ancho y bloqueo CI ante infracciones graves. |
| Capturas completas no cargaban imágenes diferidas | Espera explícita de fuentes e imágenes antes de capturar cada ancho. |

### Ejecución y evidencias

- Python portátil 3.11.9, Playwright 1.65.2 y Chromium 159, instalados solo en `artifacts/tools/` (ignorado por Git). El alias `python` del equipo no es ejecutable; los comandos se ejecutaron mediante `artifacts/tools/python/python.exe`.
- `python scripts/validate_site.py`: correcto, 37 referencias; `node --check script.js` y `git diff --check`: correctos.
- `python scripts/build_site.py --target preview`: correcto, salida local `dist/preview/`, conserva `noindex,nofollow`.
- `python -m unittest discover -s tests -p "test_*.py" -v`: **29 pruebas aprobadas**, código de salida 0; incluye SEO, bloqueadores, responsive, imágenes, navegación, filtros, formulario, geometría, reduced-motion y foco. Registro: `artifacts/audit-final-tests.txt`. Tras el último ajuste del collage se repitió la prueba de geometría móvil: **1 prueba aprobada**, incluyendo intersecciones a 320, 375 y 570 px.
- Anchos automatizados: 320, 375, 390, 570, 768, 850, 1024, 1280 y 1920 px. Capturas con imágenes decodificadas: `artifacts/rc-team-<ancho>.png`.
- Axe WCAG 2 A/AA y 2.1 A/AA a 390 y 1280 px: **cero infracciones reportadas**; informes en `artifacts/axe-390.json` y `artifacts/axe-1280.json`.
- Preview compilada probada bajo `/dist/preview/`: recursos relativos y variantes WebP con HTTP 200, noindex preservado, animación normal visible al hacer scroll y cero errores JavaScript capturados. Recortes finales del collage en `artifacts/hero-final-320.png`, `hero-final-375.png` y `hero-final-570.png`.
- Inspección visual de las capturas de 320, 375, 768, 1024, 1280 y 1920 px; la matriz automatizada no detectó desbordamiento horizontal antes ni después de cargar fuentes e imágenes.
- Se inspeccionaron cambios y archivos añadidos para evitar secretos y material ajeno. Los originales gráficos y el branding se conservan. Los enlaces internos e imágenes se comprobaron; no se enviaron correos ni formularios reales.

### Límites y pendientes

- No se ejecutaron Safari, Firefox, dispositivos físicos, lector de pantalla humano, Lighthouse/Core Web Vitals, ni una comprobación remota de CI/Pages o producción. Axe no acredita por sí solo conformidad completa.
- La prueba del formulario comprueba la solicitud `mailto:`, no la apertura de una aplicación de correo instalada ni el envío. Sin JS el formulario se oculta y un aviso ofrece correo y WhatsApp. Con JS el borrador queda visible para copiarlo y se ofrece un enlace para reintentar; no se activa un backend.
- Los recursos de Google Fonts y Unsplash siguen siendo dependencias externas. Los originales archivados siguen incluidos por el constructor, aunque las dos imágenes pesadas ya no se descargan al navegar.
- Pendientes del cliente: material y cargos de Team, aprobación final del rediseño y fotografías, validación de las afirmaciones de Declass, y decisión de contacto definitivo. Ya constan en REQUIREMENTS.md; no se consideran completados ni se asignan fechas.
- La ejecución inicial de Codex no pudo crear una rama por restricciones de escritura en los metadatos Git compartidos. Esta limitación histórica fue levantada para la integración en `claude`; ver el registro de integración siguiente. No se ha fusionado `main` ni desplegado producción.

La lista siguiente sigue siendo el control de entrega y aprobación general; esta auditoría local no marca como aprobadas las tareas comerciales ni los despliegues.

## Automático
- [ ] python scripts/validate_site.py finaliza sin errores.
- [ ] Workflow "Validate static site" en verde.
- [ ] Workflow de Pages en verde luego de habilitar el sitio.

## Visual y funcional
- [ ] Probar 320, 375, 390, 768, 1024, 1280 y 1920 px.
- [ ] Sin desbordamientos, roturas, texto cortado ni imágenes faltantes.
- [ ] Logo nuevo legible sobre fondo oscuro y sin rectángulo negro en header y footer.
- [ ] Favicon nuevo con isotipo RC visible en una pestaña limpia (sin caché del anterior).
- [ ] Menú responsive, foco accesible y cierre con Escape.
- [ ] Filtros de medios funcionan y las seis tarjetas del mosaico no dejan columnas/filas vacías en escritorio, tablet o móvil.
- [ ] Navegación Team y Contacto funciona.
- [ ] Rodrigo aparece como figura identificada por el sitio anterior y se aclara que su cargo está pendiente.
- [ ] Otros perfiles pendientes no se confunden con personas reales.
- [ ] Se preservaron los cinco servicios, se retiraron de la interfaz los logos históricos por petición del cliente y se mantiene la referencia visual a Declass.
- [ ] Se siguen las correcciones de las 7 diapositivas de Rodrigo: textos exactos, orden Home→Agencia, secciones retiradas, Declass sin botón, contacto y footer.
- [ ] La afirmación sobre el encargo a Declass y los más de 23.000 documentos proviene del cliente; confirmar antes de producción.
- [ ] El footer es landmark contentinfo y el contenido sigue visible si JavaScript está desactivado.
- [ ] Los filtros actualizan el mensaje accesible con el número de categorías visibles.
- [ ] Formulario sin JS muestra alternativas de contacto; con JS prepara correo y conserva un borrador copiable si no hay cliente de correo, sin envío automático ni backend.
- [ ] Preferencia de movimiento reducido respetada.

## Aprobación y despliegue
- [ ] Rodrigo aprueba maqueta, textos y recursos.
- [ ] Recibidos y validados nombres, fotografías y cargos reales.
- [ ] Confirmado formulario definitivo de producción.
- [ ] Realizado respaldo del hosting antes de modificar rcteam.cl.
- [ ] En producción retirar noindex; la vista previa debe permanecer sin indexar.
- [ ] Registrar fecha, commit, autorización y reversión.
