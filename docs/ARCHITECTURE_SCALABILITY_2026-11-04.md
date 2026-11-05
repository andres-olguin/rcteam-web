# rcteam-web — Escalabilidad y evolución técnica

**Documento:** MTS-ENG-RCTEAM-WEB-20261104 · **Estado:** investigación y planificación, no producción certificada · **Fecha:** 2026-11-04.

## Base del repositorio

Web de cliente RC Team con README, assets, estilos, scripts y tests; falta validar composición final de equipo y materiales.

## Arquitectura objetivo

Web estática con imágenes optimizadas y componentes simples; evitar backend innecesario. Separar staging y producción, despliegue de GitHub Pages si está aprobado.

## Calidad y observabilidad

Rendimiento LCP/INP/CLS, legibilidad móvil, navegación Team/Contacto, validación de enlaces y errores del formulario.

En pruebas documentar versión, fecha, dataset, comandos, hardware, fallos, tiempo y variación. Las cifras de capacidad solo se presentan cuando están respaldadas por ejecuciones reales, distinguiendo ejemplos sintéticos.

## Puertas de seguridad y negocio

Fotos, logotipos, cargos, textos y permisos deben confirmarse con RC Team antes de publicación. No asumir aprobación cliente por merge.

## Hoja de ruta condicional

G1 auditoría móvil/accesibilidad; G2 contenido autorizado; G3 QA cross-browser; G4 publicación con rollback documentado.

Las etapas no son promesas de fecha. Pasar de una etapa a otra exige prueba verificable, control de costos, responsable y análisis de riesgo. No introducir infraestructura de alta complejidad sin métricas de saturación que la justifiquen.

## Fuentes metodológicas consultadas el 04-11-2026

- [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/): rendimiento, seguridad, operación, fiabilidad y costos.
- [OWASP ASVS 5.0.0](https://asvs.owasp.org/): verificación de controles web/API cuando aplica.
- [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final): disciplina de desarrollo seguro.
- [Google SRE](https://sre.google/workbook/implementing-slos/): objetivos medidos de fiabilidad.

**Nota de integridad:** no se ha ejecutado una auditoría integral por el mero hecho de publicar este documento y las fuentes externas no prueban eficacia del proyecto.
