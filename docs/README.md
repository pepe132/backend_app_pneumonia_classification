# Documentación del backend

Última actualización: 2026-08-31.

Este directorio separa la documentación vigente de los documentos históricos.
Ante cualquier diferencia, el código, OpenAPI y las pruebas automatizadas son la
fuente de verdad del contrato técnico.

## Documentación vigente

| Documento | Propósito |
|---|---|
| `seguimiento_backend.md` | Estado actual, bloques terminados y siguiente trabajo recomendado. |
| `pendientes_backend_v1.md` | Backlog funcional y técnico detallado. Debe leerse junto con el seguimiento actual. |
| `backlog_pruebas_backend.md` | Cobertura, escenarios y pendientes de pruebas. |
| `matriz_reglas_clinicas_v1.md` | Reglas clínicas provisionales pendientes de validación formal. |
| `migraciones.md` | Operación de Alembic y antecedentes de migración. |

## Contrato para consumidores

- La API nueva se consume bajo `/api/v1`.
- Las rutas sin versión se conservan temporalmente por compatibilidad.
- Con `ENABLE_DOCS=true`, el contrato ejecutable está disponible en
  `/openapi.json`, `/docs` y `/redoc`.
- El frontend móvil mantiene su plan vigente en
  `../mobile_app_pneumonia/docs/plan_implementacion_frontend.md`, relativo al
  directorio que contiene ambos repositorios.

## Histórico

`historico/` contiene planes, contexto, arquitectura propuesta y cortes de
seguimiento que fueron útiles durante etapas anteriores. Se conservan por
trazabilidad, pero no deben utilizarse para determinar el estado actual del
backend.

Los scripts SQL anteriores a Alembic se encuentran en `../scripts/legacy/`.
No deben ejecutarse sobre una base administrada por las migraciones actuales.

## Regla de mantenimiento

Al completar un bloque:

1. Actualizar `seguimiento_backend.md`.
2. Actualizar el backlog afectado.
3. Registrar migraciones y resultado de pruebas.
4. Mover a `historico/` cualquier documento sustituido.
5. Evitar mantener dos documentos como fuente de verdad para el mismo tema.
