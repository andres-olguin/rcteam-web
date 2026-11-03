# Guía de trabajo para Codex y colaboradores — RC Team

## Propósito
Mantener el sitio original de RC Team y ejecutar un rediseño editorial **solo con requisitos confirmados**, preservando la versión aprobada en `main`.

## Reglas obligatorias
1. **No hacer commits directamente a `main`** para cambios nuevos: utilizar `feat/*`, `fix/*`, `docs/*` o `chore/*` y abrir PR.
2. No desplegar a `rcteam.cl` ni modificar DNS, hosting, servicios de contacto o credenciales sin autorización explícita.
3. Conservar contenido, enlaces y datos de contacto existentes salvo cambio solicitado y verificado.
4. No inventar nombres, cargos, fotos, logo, testimonios, proyectos, clientes o autorizaciones del cliente.
5. Mantener HTML/CSS/JS estáticos hasta que exista una necesidad técnica documentada para otra tecnología.
6. No incluir secretos, accesos, archivos personales ni licencias de recursos que no se puedan redistribuir. Revisar `git diff --cached` antes de subir.
7. Mantener rutas **relativas** para recursos internos; la web debe funcionar bajo la subruta `/rcteam-web/` de GitHub Pages.
8. Preservar funcionamiento de contacto y links; **no enviar formularios reales de prueba** sin coordinación.
9. Añadir documentación y evidencia de pruebas para cambios relevantes. Usar commits descriptivos.
10. Señalar como **pendiente/no verificado** cualquier requisito o comportamiento no comprobado.

## Arquitectura
- `index.html`: contenido y semántica
- `styles.css`: tokens, layout y puntos de quiebre
- `script.js`: interacción no bloqueante
- `images/`: activos aprobados y optimizados
- `docs/`: alcance y operación
- `scripts/validate_site.py`: verificación estática

## Verificación antes de cada PR
- Ejecutar `python scripts/validate_site.py`.
- Revisar manualmente a 320, 375, 768 y 1280 px; sin scroll horizontal ni contenido cortado.
- Comprobar navegación por teclado, etiquetas, contraste y `prefers-reduced-motion`.
- Comprobar carga de imágenes y enlaces locales en `http://localhost:8000` y, cuando aplique, en la subruta de Pages.
- No asegurar que Pages o el formulario funcionan sin prueba real.

## Estado del cliente
Referencia de rediseño editorial azul/negro, navegación superior Team y Contacto, 4–5 personas en Team (datos pendientes), nuevo logo pendiente. No confundir propuesta de referencia con composición exacta aprobada. Consultar `docs/REQUIREMENTS.md`.
