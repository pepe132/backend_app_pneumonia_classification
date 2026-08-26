# Seguimiento del backend

Documento principal para controlar el avance del backend de neumonia pediatrica.

Ultima actualizacion: 2026-08-23.

## Punto de reanudacion de la sesion

Ultimo punto validado: 2026-08-23.

Estado confirmado al cerrar:

- Bloque 1 de seguridad, usuarios y flujo clinico: terminado.
- Bloque 2 de consultas para frontend: terminado.
- Bloque 3 de estabilizacion y seguridad de datos: terminado.
- Migracion `20260819_0002` aplicada correctamente en SQL Server.
- Ultima ejecucion de pruebas: `71 passed in 10.43s`.
- No hay una migracion pendiente creada por el bloque 2.
- El backend puede continuar desde el bloque de estabilizacion y seguridad de
  datos descrito al final de este documento.

Antes de comenzar la siguiente sesion:

```powershell
alembic current
python -m pytest -q
```

Resultado esperado:

```text
20260819_0002 (head)
71 passed
```

Mensaje sugerido para reanudar el trabajo:

> Continua el backend usando `docs/seguimiento_backend.md`. Retoma desde el
> siguiente bloque recomendado, informa cada paso antes de implementarlo y no
> declares cerrado el bloque hasta que las migraciones y pytest sean validados.

Si aparecen cambios nuevos antes de reanudar, revisar primero el estado del
repositorio y ejecutar nuevamente la suite para establecer una nueva linea base.

## Estado general

El backend dispone del flujo autenticacion, pacientes, evaluacion clinica,
prediccion tabular, radiografia, CNN, fusion, decision auxiliar, reporte y
dashboard.

- Suite automatizada: **71 pruebas aprobadas**.
- Revision de Alembic: **20260819_0002 (head)**.

## Bloques terminados

### Base funcional inicial

- JWT, login, registro controlado y roles.
- CRUD de pacientes con desactivacion logica.
- Evaluaciones y prediccion tabular.
- Radiografias JPG/PNG y prediccion CNN.
- Fusion y decision auxiliar explicable.
- Errores uniformes, CORS, logging y Alembic.

### Bloque 1: seguridad, usuarios y flujo clinico

Cerrado el 2026-08-19 con `69 passed`.

- `POST /decision/auxiliary` requiere administrador o especialista.
- Administracion de usuarios exclusiva para administrador.
- Cambio propio y restablecimiento administrativo de contrasena.
- Un administrador no puede desactivarse ni retirar su propio rol.
- Los usuarios desactivados dejan de ser aceptados por tokens existentes.
- Entrega autenticada de la imagen radiografica.
- Snapshot historico de la decision auxiliar.
- Consulta de decision auxiliar por evaluacion.
- Migracion `20260819_0002` aplicada.

Endpoints agregados:

```http
GET    /auth/users
POST   /auth/users
GET    /auth/users/{user_id}
PATCH  /auth/users/{user_id}
DELETE /auth/users/{user_id}
POST   /auth/change-password
POST   /auth/users/{user_id}/reset-password
GET    /evaluations/{evaluation_id}/radiograph/image
GET    /evaluations/{evaluation_id}/auxiliary-decision
```

La migracion agrego `dbo.Evaluations.auxiliary_decision_json`.

### Bloque 2: consultas para frontend

Cerrado el 2026-08-19 con `69 passed`. No requirio migracion.

- Paginacion de pacientes y evaluaciones.
- Filtros por datos demograficos, estado, severidad, creador y fechas.
- Filtro de evaluaciones con o sin radiografia.
- Ordenamiento validado.
- Rutas anteriores conservadas por compatibilidad.
- Reporte individual consolidado.
- Dashboard con totales, distribuciones y tendencia diaria.

Endpoints agregados:

```http
GET /patients/page
GET /evaluations/page
GET /reports/evaluations/{evaluation_id}
GET /dashboard/summary
```

## Contratos para el frontend

Los listados paginados devuelven:

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 20,
  "pages": 0
}
```

El reporte incluye paciente, evaluacion, resultado integrado, radiografia y
decision auxiliar cuando estan disponibles.

El dashboard incluye pacientes activos, evaluaciones, radiografias,
distribuciones por severidad, clases radiograficas y tendencia diaria. Admite
los filtros opcionales `date_from` y `date_to`.

## Pendientes vigentes

### Prioridad alta

- Politica definida el 2026-08-23: administrador, especialista y lectura pueden
  consultar todos los pacientes y evaluaciones. Solo administrador y
  especialista pueden crear o modificar informacion clinica.
- Politica definida el 2026-08-23: el registro publico puede habilitarse en
  desarrollo/pruebas y debe estar deshabilitado en produccion; alli las cuentas
  son creadas por un administrador.
- API versionada bajo `/api/v1` el 2026-08-23; las rutas sin prefijo se
  conservan temporalmente como contratos heredados.
- Corregir textos antiguos con problemas de codificacion y normalizar acentos.
- Publicar el contrato definitivo para el frontend.

### Funcionalidad

- Agregar expediente clinico si se confirma como requisito.
- Evaluar exportacion de reportes a PDF.
- Evaluar recuperacion de contrasena por correo/token temporal.
- Definir auditoria de modificaciones clinicas.
- Definir estado o borrado logico para evaluaciones.
- Definir retencion, respaldo y eliminacion de radiografias.

### Validacion clinica

- Obtener revision formal de `docs/matriz_reglas_clinicas_v1.md`.
- Confirmar umbrales y textos de recomendaciones.
- Ejecutar DE-01 a DE-10.
- Identificar campos clinicos faltantes o ambiguos.
- Mantener las recomendaciones como provisionales hasta cerrar la validacion.

### Produccion

- Definir dominios reales en `CORS_ORIGINS`.
- Validar SQL Server, JWT, almacenamiento y CNN en el entorno objetivo.
- Definir monitoreo, respaldos y despliegue.
- Ejecutar una revision final de seguridad y privacidad.

## Siguiente bloque recomendado

**Estabilizacion y seguridad de datos:**

1. Visibilidad global autenticada definida; pendiente validacion final del bloque.
2. Resolver la politica de registro publico.
3. Normalizar textos y codificacion.
4. Versionar contratos sin romper las rutas existentes.
5. Ampliar pruebas de seguridad y actualizar OpenAPI.

## Bloque 3: estabilizacion y seguridad de datos

Cerrado y validado el 2026-08-23 con `71 passed in 10.43s`.

- Lectura clinica global para administrador, especialista y lectura.
- Escritura clinica limitada a administrador y especialista.
- Registro publico configurable en desarrollo/pruebas y prohibido en produccion.
- Mensajes HTTP visibles normalizados en espanol.
- Contratos disponibles bajo `/api/v1`.
- Rutas heredadas conservadas temporalmente para compatibilidad.
- Pruebas ampliadas para politica de registro, visibilidad y OpenAPI versionado.
- No requiere migracion de base de datos.

## Siguiente bloque recomendado despues del bloque 3

**Trazabilidad y ciclo de vida clinico:**

1. Definir e implementar identificador de expediente clinico.
2. Agregar auditoria de cambios sobre pacientes y evaluaciones.
3. Definir estado y desactivacion logica de evaluaciones.
4. Definir politica tecnica de retencion de radiografias.
5. Agregar migraciones, pruebas y documentacion del bloque.

## Comandos de control

```powershell
alembic current
alembic upgrade head
python -m pytest -q
python -m pytest --cov=app --cov-report=term-missing
```

## Regla de actualizacion

Al cerrar cada bloque se debe registrar aqui:

1. Fecha de cierre.
2. Funcionalidad implementada.
3. Endpoints agregados o modificados.
4. Migraciones aplicadas.
5. Resultado de pytest.
6. Pendientes descubiertos.
7. Siguiente bloque recomendado.

Documentos complementarios:

- `docs/pendientes_backend_v1.md`: backlog funcional detallado.
- `docs/backlog_pruebas_backend.md`: plan y evidencia de pruebas.
- `docs/seguimiento_implementacion.md`: historial tecnico anterior.
- `docs/matriz_reglas_clinicas_v1.md`: reglas clinicas provisionales.
- `docs/pendientes_frontend_mobile_v1.md`: backlog del cliente movil.
