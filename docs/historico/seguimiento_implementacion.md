# Seguimiento de implementación

## Corte de estado del backend

Fecha: 2026-08-11.

### Resumen ejecutivo

El backend cuenta con un flujo funcional de extremo a extremo para:

```text
autenticación
  -> paciente
  -> evaluación clínica y predicción ML
  -> radiografía y predicción DL
  -> fusión de resultados
  -> decisión auxiliar explicable
```

La aplicación utiliza FastAPI, SQLAlchemy, SQL Server, JWT, un modelo tabular
persistido en formato PKL y un modelo radiográfico Keras configurable.

### Módulos desarrollados

| Módulo | Estado | Funcionalidad disponible |
|---|---|---|
| Autenticación | Funcional | Registro controlado, login JSON/OAuth2, JWT y usuario actual |
| Roles y permisos | Funcional | Escritura para administrador/especialista y lectura autenticada |
| Pacientes | Funcional | Alta, lista, búsqueda, detalle, edición y desactivación lógica |
| Evaluaciones | Funcional | Alta, listado, detalle, historial por paciente y predicción tabular |
| Radiografías | Funcional | Validación, almacenamiento, inferencia CNN, persistencia y consulta |
| Fusión | Funcional | Combinación versionada de severidad clínica y evidencia radiográfica |
| Decisión auxiliar | Implementada, pendiente de validación clínica | Combina ML, DL y datos originales; genera explicación y recomendación |
| Configuración y errores | Funcional | Perfiles de entorno, CORS, logging y respuestas de error uniformes |
| Migraciones | Funcional | Alembic, revisión base, roles iniciales y flujo documentado |

### Contratos HTTP disponibles

- `GET /` y `GET /health/db`.
- `POST /auth/register`, `POST /auth/login`, `POST /auth/token` y
  `GET /auth/me`.
- `POST /patients/`, `GET /patients/`, `GET /patients/search`,
  `GET /patients/{patient_id}`, `PATCH /patients/{patient_id}` y
  `DELETE /patients/{patient_id}`.
- `POST /evaluations`, `GET /evaluations`,
  `GET /evaluations/{evaluation_id}` y
  `GET /patients/{patient_id}/evaluations`.
- `POST /evaluations/{evaluation_id}/radiograph` y
  `GET /evaluations/{evaluation_id}/radiograph`.
- `POST /decision/auxiliary`.

Los esquemas detallados se mantienen además en OpenAPI cuando
`ENABLE_DOCS=true`, mediante `/docs` y `/openapi.json`.

### Datos y reglas consolidados

- La edad está estandarizada en meses y limitada a `0..72` en pacientes,
  evaluaciones, contratos de decisión y SQL Server.
- La evaluación conserva los datos clínicos originales, la severidad tabular y
  las probabilidades `Bajo`, `Medio` y `Alto`.
- La radiografía conserva clase, confianza, cuatro probabilidades y versión del
  modelo.
- La fusión conserva severidad final, concordancia, fundamento, explicación,
  código de recomendación y versión.
- La radiografía es evidencia auxiliar y no sustituye la valoración clínica.

### Calidad y base de datos

- Suite automatizada: `68 passed` al 2026-08-11.
- Cobertura incluida: configuración, seguridad, esquemas, contratos HTTP,
  control de roles, integración SQL Server, modelo tabular, radiografías,
  fusión, decisión auxiliar, errores y migraciones.
- Las pruebas de integración escriben dentro de transacciones con rollback.
- Alembic está en la revisión `20260811_0001 (head)`.
- La migración base fue probada con `upgrade` y `downgrade` en una base temporal
  limpia, eliminada al terminar.
- Los datos existentes permanecieron en 4 usuarios, 3 pacientes,
  2 evaluaciones y 2 radiografías después de las pruebas del punto 4.

### Bloqueos y pendientes vigentes

- Validar con la especialista la matriz de reglas clínicas, sus umbrales,
  recomendaciones y campos faltantes.
- Ejecutar la Fase 6 del backlog después de esa validación.
- Validar operativamente el CNN definitivo con el archivo y entorno de
  producción previstos.
- Implementar administración de usuarios y cambio/restablecimiento de
  contraseña.
- Implementar dashboard, reportes, filtros avanzados y paginación.
- Definir requisitos de auditoría, privacidad, almacenamiento de imágenes y
  despliegue seguro.
- Publicar un contrato versionado para el frontend móvil; mientras tanto los
  contratos clínicos y de decisión deben considerarse provisionales.

## Capa auxiliar de decisión

Fecha: 2026-07-13

### Implementado

- Se creó `app/services/auxiliary_decision.py`.
- Se agregó la función principal `generate_auxiliary_decision`.
- Se implementaron reglas auxiliares que combinan:
  - resultado clínico del modelo ML tabular,
  - resultado radiográfico del modelo DL,
  - datos originales del formulario clínico.
- La severidad clínica tiene prioridad sobre la radiografía.
- La radiografía se usa solo como evidencia auxiliar.
- Se agregaron signos de alarma para elevar la recomendación a valoración urgente:
  - `spo2 < 90`,
  - cianosis,
  - apnea,
  - convulsiones,
  - Glasgow menor a 14,
  - frecuencia respiratoria elevada junto con tiraje.
- Se agregó identificación de hallazgos clínicos relevantes en español.
- Se incluyeron todos los campos del formulario clínico actual.

### Endpoint auxiliar independiente

- Se creó `app/modules/decision/schema.py`.
- Se creó `app/modules/decision/router.py`.
- Se registró el router en `app/main.py`.
- Endpoint disponible:

```http
POST /decision/auxiliary
```

Este endpoint recibe manualmente:

- `clinical_result`,
- `xray_result`,
- `patient_data`.

### Integración con flujo real

- Se actualizó `app/modules/radiographs/service.py`.
- Al subir una radiografía en:

```http
POST /evaluations/{evaluation_id}/radiograph
```

el backend ahora:

- ejecuta el modelo radiográfico DL,
- usa el resultado clínico ML ya guardado en la evaluación,
- usa los datos clínicos originales de la evaluación,
- genera `auxiliary_decision`,
- devuelve la recomendación auxiliar en la misma respuesta.

### Respuesta nueva esperada

La respuesta de subida de radiografía ahora incluye:

```json
{
  "radiograph": {},
  "integrated_result": {},
  "auxiliary_decision": {
    "clasificacion_auxiliar": "",
    "prediccion_severidad": "",
    "probabilidades_severidad": {},
    "hallazgos_clinicos_relevantes": [],
    "resultado_radiografico_auxiliar": "",
    "prediccion_radiografica": "",
    "probabilidades_radiograficas": {},
    "recomendacion": "",
    "nota_seguridad": ""
  }
}
```

### Mapeos agregados

El modelo clínico devuelve etiquetas en español:

- `Bajo`
- `Medio`
- `Alto`

La capa auxiliar las normaliza a:

- `Low`
- `Moderate`
- `High`

El modelo radiográfico devuelve etiquetas internas:

- `covid_19`
- `normal`
- `pneumonia_bacterial`
- `pneumonia_viral`

La capa auxiliar las normaliza a:

- `COVID-19`
- `Normal`
- `Bacterial pneumonia`
- `Viral pneumonia`

### Validaciones realizadas

- Compilación con `py_compile` de los archivos modificados.
- Prueba directa de `generate_auxiliary_decision` con el ejemplo clínico/radiográfico.
- Prueba simulada del adaptador entre `Evaluation`, `Radiograph` y la capa auxiliar.

### Validación manual e integración

- Se crearon evaluaciones clínicas y se confirmó la persistencia de la
  predicción tabular.
- Se cargaron dos radiografías y se confirmó su análisis y persistencia.
- La integración y el contrato de `auxiliary_decision` están cubiertos por
  pruebas automatizadas.
- Queda pendiente validar clínicamente las reglas y revisar que el frontend
  consuma y muestre:
  - clasificación auxiliar,
  - hallazgos clínicos relevantes,
  - resultado radiográfico auxiliar,
  - recomendación,
  - nota de seguridad.

### Nota técnica

Se mantiene `integrated_result` para no romper el contrato anterior del endpoint. La nueva salida explicable está en `auxiliary_decision`.
