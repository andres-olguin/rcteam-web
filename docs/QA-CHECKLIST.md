# Validación de entrega — RC Team

## Automático
- [ ] python scripts/validate_site.py finaliza sin errores.
- [ ] Workflow "Validate static site" en verde.
- [ ] Workflow de Pages en verde luego de habilitar el sitio.

## Visual y funcional
- [ ] Probar 320, 375, 390, 768, 1024, 1280 y 1920 px.
- [ ] Sin desbordamientos, roturas, texto cortado ni imágenes faltantes.
- [ ] Logo nuevo legible sobre fondo oscuro.
- [ ] Menú responsive, foco accesible y cierre con Escape.
- [ ] Filtros de medios funcionan.
- [ ] Navegación Team y Contacto funciona.
- [ ] Rodrigo aparece como figura identificada por el sitio anterior y se aclara que su cargo está pendiente.
- [ ] Otros perfiles pendientes no se confunden con personas reales.
- [ ] Se preservaron los cinco servicios, se retiraron de la interfaz los logos históricos por petición del cliente y se mantiene la referencia visual a Declass.
- [ ] Se siguen las correcciones de las 7 diapositivas de Rodrigo: textos exactos, orden Home→Agencia, secciones retiradas, Declass sin botón, contacto y footer.
- [ ] La afirmación sobre el encargo a Declass y los más de 23.000 documentos proviene del cliente; confirmar antes de producción.
- [ ] El footer es landmark contentinfo y el contenido sigue visible si JavaScript está desactivado.
- [ ] Los filtros actualizan el mensaje accesible con el número de categorías visibles.
- [ ] Formulario de demostración usa POST como fallback sin añadir datos personales a la URL; con JS prepara correo, sin envío automático.
- [ ] Preferencia de movimiento reducido respetada.

## Aprobación y despliegue
- [ ] Rodrigo aprueba maqueta, textos y recursos.
- [ ] Recibidos y validados nombres, fotografías y cargos reales.
- [ ] Confirmado formulario definitivo de producción.
- [ ] Realizado respaldo del hosting antes de modificar rcteam.cl.
- [ ] En producción retirar noindex; la vista previa debe permanecer sin indexar.
- [ ] Registrar fecha, commit, autorización y reversión.
