# RC Team — Instrucciones permanentes para Codex, Antigravity y colaboradores

## Objetivo
Evolucionar un sitio estático profesional siguiendo la referencia editorial azul/negro de Rodrigo, sin inventar contenidos ni modificar rcteam.cl sin aprobación.

## Reglas de repositorio
1. Siempre crear rama (feat/, fix/, chore/ o docs/) y Pull Request. No hacer commits de desarrollo directamente a main.
2. main contiene la propuesta más reciente validada y la fuente de GitHub Pages (cuando Pages esté habilitado).
3. Nunca subir contraseñas, tokens, .env, accesos de hosting, datos privados o materiales sin permiso.
4. No cambiar DNS, dominio, hosting ni desplegar rcteam.cl sin instrucción expresa y respaldo previo.
5. Mantener HTML, CSS y JavaScript nativos, salvo justificación técnica documentada y aprobación.
6. Mantener rutas de recursos internas relativas (GitHub Pages usa /rcteam-web/).
7. Conservar el branding RC Team: variantes WebP derivadas de los archivos facilitados; no sustituir ni alterar logotipo por IA.
8. Usar solo datos de equipo confirmados. No generar ni simular fotos, roles o identidades. Los 5 perfiles presentes son marcadores explícitos.
9. Fotografías Unsplash son recursos ilustrativos, no campañas realizadas por RC Team. Deben revisarse con Rodrigo antes de publicar producción.
10. El formulario de preview solo abre borrador de correo: no activar FormSubmit ni otro backend sin autorización.
11. Evitar implementar métricas, clientes, testimonios, premios o cifras no verificadas.
12. Mantener rastreo de cambios con commits descriptivos y documentación actualizada.

## Arquitectura
index.html = estructura y contenido.
styles.css = diseño, tokens, layout, motion y responsive.
script.js = menú, filtros y formulario demo.
assets/ = logos entregados.
images/ = respaldo de imágenes originales.
docs/ = requisitos, diseño, operación y QA.
scripts/validate_site.py = validación local.
.github/workflows/ = CI y publicación de preview.

## Antes de enviar PR
- Ejecutar python scripts/validate_site.py.
- Inspeccionar cambios por secretos y archivos no autorizados.
- Revisar 320, 375, 768, 1024, 1280 y 1920 px; sin horizontal overflow.
- Probar navegación por teclado, foco visible, preferencia reduced-motion, menú, filtros, links y carga de imágenes.
- Señalar explícitamente qué pruebas no se ejecutaron.
- No atribuir aprobación al cliente sin evidencia.

## Coordinación de agentes
Codex: implementación, pruebas y diffs pequeños.
Antigravity: revisión UI, responsive, interacciones y QA visual.
Trabajar en ramas distintas o en secuencia para evitar conflictos. No ejecutar merges o despliegues simultáneos sin revisión. Un responsable integra los PR.

## Pendientes comerciales
Confirmados: nuevo estilo editorial, menú Team/Contacto, navegación vertical. Pendientes: material de 4–5 integrantes, aprobación del rediseño y decisión del contacto final. Ver docs/REQUIREMENTS.md.
