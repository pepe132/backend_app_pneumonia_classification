# Backlog de pruebas del backend

Fecha de creación: 2026-08-04

## Objetivo

Validar de forma controlada las funcionalidades implementadas en el backend de
apoyo clínico para neumonía pediátrica, documentar los resultados y convertir
los fallos encontrados en tareas concretas de corrección.

## Estado verificado del entorno

- Python 3.11.0 disponible.
- Entorno virtual `env` operativo.
- FastAPI, SQLAlchemy y Pydantic se importan correctamente.
- `httpx 0.28.1` instalado en `env` para usar `TestClient`.
- La aplicación se importa correctamente y registra 23 rutas.
- SQL Server responde en `127.0.0.1:1433`.
- La conexión configurada mediante SQLAlchemy funciona (`SELECT 1`).
- Estado inicial observado en la base de datos:
  - 3 roles.
  - 2 usuarios.
  - 1 paciente.
  - 0 evaluaciones.
  - 0 radiografías.

## Reglas de seguridad para las pruebas

- No modificar ni eliminar los usuarios y el paciente que ya existen.
- Ejecutar primero todas las pruebas no destructivas.
- No usar información clínica real en los datos temporales.
- Identificar los registros temporales con el prefijo
  `PRUEBA_AUTOMATIZADA_20260804`.
- Registrar los identificadores de todos los datos creados durante las pruebas.
- No realizar eliminación física de registros clínicos.
- Si la API solo admite desactivación lógica, usar ese mecanismo al finalizar.
- Antes de probar radiografías, usar únicamente una imagen anónima destinada a
  pruebas y confirmar que el archivo del modelo CNN está disponible.
- No mostrar contraseñas, tokens JWT, secretos ni credenciales de base de datos
  en los resultados.

## Clasificación de resultados

- **Aprobada:** el comportamiento y la respuesta coinciden con lo esperado.
- **Fallida:** se ejecutó la prueba, pero el resultado fue incorrecto.
- **Bloqueada:** falta una dependencia, configuración, dato o decisión funcional.
- **Pendiente:** todavía no se ejecuta.

Prioridades para incidencias:

- **P0:** riesgo de seguridad, pérdida o exposición de datos.
- **P1:** bloquea una función principal.
- **P2:** comportamiento incorrecto con alternativa temporal.
- **P3:** mejora, consistencia o documentación.

## Fase 1. Pruebas no destructivas

| ID | Módulo | Escenario | Resultado esperado | Estado |
| --- | --- | --- | --- | --- |
| ND-01 | Aplicación | Importar `app.main` | La aplicación carga sin excepciones | Aprobada |
| ND-02 | Base de datos | Ejecutar `SELECT 1` | La conexión responde correctamente | Aprobada |
| ND-03 | General | `GET /` | HTTP 200 y mensaje de API activa | Aprobada |
| ND-04 | Salud | `GET /health/db` | HTTP 200 y estado de base conectada | Aprobada |
| ND-05 | OpenAPI | `GET /openapi.json` | HTTP 200 y contrato válido | Aprobada |
| ND-06 | Autenticación | `GET /auth/me` sin token | HTTP 401 | Aprobada |
| ND-07 | Pacientes | `GET /patients/` sin token | HTTP 401 | Aprobada |
| ND-08 | Evaluaciones | `GET /evaluations` sin token | HTTP 401 | Aprobada |
| ND-09 | Radiografías | Consultar sin token | HTTP 401, sin revelar datos | Aprobada |
| ND-10 | Decisión | Enviar solicitud válida a `/decision/auxiliary` | HTTP 200 y respuesta explicable | Aprobada |
| ND-11 | Decisión | Enviar datos inválidos o incompletos | HTTP 422 o error controlado | Aprobada |

### Resultado de la Fase 1

Ejecución: 2026-08-09.

- 11 de 11 pruebas aprobadas.
- `ND-01`: `app.main` se importó correctamente.
- `ND-02`: SQLAlchemy ejecutó correctamente `SELECT 1`.
- `ND-03`, `ND-04` y `ND-05`: HTTP 200.
- `ND-06`, `ND-07`, `ND-08` y `ND-09`: HTTP 401 sin autenticación.
- `ND-10`: HTTP 200 y los nueve campos esperados de decisión auxiliar.
- `ND-11`: HTTP 422 con detalle de los tres campos requeridos ausentes.
- Conteos antes y después: 2 usuarios, 1 paciente, 0 evaluaciones y 0
  radiografías.
- La base de datos permaneció sin cambios.

## Fase 2. Autenticación y roles

| ID | Escenario | Resultado esperado | Estado |
| --- | --- | --- | --- |
| AU-01 | Registrar usuario temporal válido | Usuario creado sin exponer contraseña | Aprobada |
| AU-02 | Registrar correo duplicado | Error controlado y código HTTP apropiado | Aprobada |
| AU-03 | Intentar registro público como administrador | Operación rechazada | Aprobada |
| AU-04 | Iniciar sesión con credenciales válidas | JWT y datos básicos del usuario | Aprobada |
| AU-05 | Iniciar sesión con contraseña incorrecta | HTTP 401, sin información sensible | Aprobada |
| AU-06 | Consultar `/auth/me` con JWT válido | Datos del usuario autenticado | Aprobada |
| AU-07 | Usar token inválido o vencido | HTTP 401 | Aprobada |
| AU-08 | Rol de lectura consulta recursos | Acceso permitido | Aprobada |
| AU-09 | Rol de lectura intenta crear o modificar | HTTP 403 | Aprobada |
| AU-10 | Administrador o especialista escribe | Acceso permitido | Aprobada |

### Resultado de la Fase 2

Ejecución: 2026-08-09.

- 10 de 10 pruebas aprobadas con datos temporales válidos.
- Registro de especialista: HTTP 200 y contraseña ausente de la respuesta.
- Correo duplicado: HTTP 400.
- Intento de registro de administrador: HTTP 403.
- Login válido y `/auth/me`: HTTP 200 con identidad y rol correctos.
- Contraseña incorrecta y token inválido: HTTP 401.
- El rol lectura pudo listar pacientes, pero recibió HTTP 403 al intentar crear.
- El especialista creó un paciente con HTTP 201 y `created_by` correcto.
- Se conservaron todos los IDs de usuarios y pacientes existentes.
- Se agregaron exactamente dos usuarios y un paciente, todos temporales.

## Fase 3. Pacientes

| ID | Escenario | Resultado esperado | Estado |
| --- | --- | --- | --- |
| PA-01 | Crear paciente temporal válido | HTTP 201 y datos persistidos | Aprobada |
| PA-02 | Crear paciente con datos inválidos | HTTP 422 o error de negocio controlado | Aprobada |
| PA-03 | Listar pacientes | Respuesta paginada o limitada | Aprobada |
| PA-04 | Consultar paciente temporal por ID | Datos correctos | Aprobada |
| PA-05 | Consultar ID inexistente | HTTP 404 | Aprobada |
| PA-06 | Buscar por nombre temporal | Se encuentra el registro creado | Aprobada |
| PA-07 | Actualizar paciente temporal | Cambios persistidos | Aprobada |
| PA-08 | Desactivar paciente temporal | Desactivación lógica, sin borrado físico | Aprobada |
| PA-09 | Verificar permisos de lectura/escritura | Se respeta la matriz de roles | Aprobada |

### Resultado de la Fase 3

Ejecución: 2026-08-09.

- 9 de 9 pruebas funcionales aprobadas.
- Se creó un segundo paciente temporal con HTTP 201.
- Una solicitud con campos obligatorios ausentes devolvió HTTP 422.
- Listado, consulta por ID y búsqueda devolvieron el paciente esperado.
- Un ID inexistente devolvió HTTP 404.
- Nombre y peso se actualizaron y persistieron correctamente.
- El rol lectura pudo consultar, pero recibió HTTP 403 al intentar modificar.
- La desactivación devolvió HTTP 204, conservó físicamente la fila con
  `active=false` y la excluyó del listado y la búsqueda.
- Todos los pacientes anteriores conservaron sus IDs y los registros no
  temporales permanecieron sin cambios.
- La validación de edad, peso, talla y sexo fue corregida después de la primera
  ejecución. Las regresiones de alta y actualización inválidas devuelven HTTP
  422 sin modificar la base de datos.
- La edad del paciente se estandarizó posteriormente como `age_months`. El
  rango final confirmado del modelo es 0 a 72 meses y se aplica en pacientes,
  evaluaciones, decisión auxiliar y SQL Server. Los valores existentes se
  conservaron.

## Fase 4. Evaluaciones y modelo tabular

| ID | Escenario | Resultado esperado | Estado |
| --- | --- | --- | --- |
| EV-01 | Crear evaluación clínica válida | HTTP 201 y relación con paciente | Aprobada |
| EV-02 | Evaluar paciente inexistente | HTTP 404 | Aprobada |
| EV-03 | Enviar valores fuera de rango | HTTP 422 o error controlado | Aprobada |
| EV-04 | Ejecutar predicción tabular | Severidad `Bajo`, `Medio` o `Alto` | Aprobada |
| EV-05 | Validar probabilidades | Valores entre 0 y 1 con suma razonable | Aprobada |
| EV-06 | Confirmar persistencia de predicción | Resultado recuperable por ID | Aprobada |
| EV-07 | Listar evaluaciones | Registro temporal incluido | Aprobada |
| EV-08 | Consultar historial del paciente | Evaluación temporal incluida | Aprobada |
| EV-09 | Crear evaluación con rol de lectura | HTTP 403 | Aprobada |

### Resultado de la Fase 4

Ejecución: 2026-08-09.

- 9 de 9 pruebas aprobadas.
- Paciente inexistente e inactivo: HTTP 404 sin crear evaluaciones.
- Saturación y Glasgow fuera de rango: HTTP 422.
- Rol lectura al intentar crear: HTTP 403.
- Evaluación válida: HTTP 201 y relación correcta con paciente y especialista.
- Predicción tabular: `Medio`.
- Probabilidades: baja 0.0126, media 0.7981 y alta 0.1893; suma 1.0.
- Severidad final inicial: `Medio`, basada únicamente en datos tabulares.
- Consulta por ID, listado general e historial del paciente: HTTP 200 con la
  evaluación creada.
- Los pacientes permanecieron sin cambios y se agregó exactamente una
  evaluación.
- Antes de persistir se detectó que SQL Server no tenía seis columnas del ORM.
  Se sincronizó la tabla vacía mediante
  `003_sync_evaluations_clinical_fields.sql`.

## Fase 5. Radiografías, CNN y fusión

Esta fase queda condicionada a confirmar `CNN_MODEL_PATH`, disponibilidad de
TensorFlow, archivo `.keras` e imagen anónima de prueba.

| ID | Escenario | Resultado esperado | Estado |
| --- | --- | --- | --- |
| RX-01 | Confirmar disponibilidad del modelo CNN | Modelo cargable y cuatro clases configuradas | Aprobada |
| RX-02 | Subir JPG válido | Análisis persistido y HTTP exitoso | Aprobada |
| RX-03 | Subir PNG válido | Análisis persistido y HTTP exitoso | Aprobada |
| RX-04 | Subir tipo de archivo no permitido | Operación rechazada | Aprobada |
| RX-05 | Subir archivo mayor al límite | Operación rechazada | Aprobada |
| RX-06 | Subir segunda radiografía a la misma evaluación | Conflicto controlado | Aprobada |
| RX-07 | Consultar radiografía por evaluación | Resultado correcto | Aprobada |
| RX-08 | Validar probabilidades CNN | Cuatro probabilidades válidas | Aprobada |
| RX-09 | Validar fusión | Severidad clínica no se reduce automáticamente | Aprobada |
| RX-10 | Validar concordancia y soporte | Valores coherentes con la clase radiográfica | Aprobada |
| RX-11 | Modelo CNN no disponible | Error controlado, sin HTTP 500 genérico | Aprobada |

### Resultado de la Fase 5

Ejecución: 2026-08-09.

- 11 de 11 pruebas aprobadas y una comprobación adicional de permisos.
- Modelo `densenet121_clahe_finetuned_model.keras` cargado correctamente con
  TensorFlow en CPU.
- La imagen JPG y su conversión PNG devolvieron `pneumonia_viral` con confianza
  0.527403.
- Probabilidades: COVID-19 0.008012, normal 0.020928, bacteriana 0.443658 y
  viral 0.527403; suma 1.000001 por redondeo a seis decimales.
- JPG y PNG se almacenaron, persistieron y pueden consultarse con rol lectura.
- Formato no permitido y archivo mayor a 10 MB: HTTP 422.
- Intento de segunda radiografía en una evaluación: HTTP 409.
- Rol lectura al intentar cargar: HTTP 403.
- Como la confianza 0.527403 es menor al umbral 0.60, soporte y concordancia
  quedaron `indeterminate`.
- La severidad final permaneció `Medio`; la radiografía no la redujo.
- La respuesta incluyó decisión auxiliar, hallazgos clínicos y nota de
  seguridad.
- La simulación de modelo no disponible devolvió HTTP 503 y no alteró la base.
- Se agregó una segunda evaluación ficticia para validar la carga PNG y se
  crearon exactamente dos radiografías; los pacientes no cambiaron.

## Fase 6. Decisión auxiliar y recomendaciones

Estado general: pendiente de validación clínica externa.

La matriz preliminar está disponible en
`docs/matriz_reglas_clinicas_v1.md`. No se modificarán ni aprobarán como reglas
clínicas definitivas hasta recibir la revisión de una médica pediatra.

| ID | Escenario | Resultado esperado | Estado |
| --- | --- | --- | --- |
| DE-01 | Severidad baja sin alarmas | Recomendación auxiliar coherente | Pendiente |
| DE-02 | Severidad media | Recomendación de valoración apropiada | Pendiente |
| DE-03 | Severidad alta | Recomendación urgente | Pendiente |
| DE-04 | `spo2 < 90` | Se eleva la recomendación a urgente | Pendiente |
| DE-05 | Cianosis, apnea o convulsiones | Se identifica el signo de alarma | Pendiente |
| DE-06 | Glasgow menor a 14 | Se identifica el signo de alarma | Pendiente |
| DE-07 | Frecuencia respiratoria alta con tiraje | Se eleva la recomendación | Pendiente |
| DE-08 | Radiografía normal con clínica relevante | No reduce automáticamente la severidad | Pendiente |
| DE-09 | Validar nota de seguridad | Indica que no sustituye el criterio médico | Pendiente |
| DE-10 | Integración al cargar radiografía | Respuesta contiene `auxiliary_decision` | Pendiente |

## Fase 7. Calidad técnica

| ID | Escenario | Resultado esperado | Estado |
| --- | --- | --- | --- |
| QT-01 | Compilar módulos Python | Sin errores de sintaxis | Aprobada |
| QT-02 | Revisar códigos HTTP | Consistentes por tipo de resultado | Aprobada |
| QT-03 | Revisar errores de base de datos | No se exponen detalles internos | Aprobada |
| QT-04 | Revisar errores de predictores | Respuestas controladas | Aprobada |
| QT-05 | Revisar codificación de textos | Español y acentos correctos | Parcial: errores normalizados |
| QT-06 | Revisar `.env.example` | Sin secretos y con variables completas | Aprobada |
| QT-07 | Ejecutar suite automatizada | Todas las pruebas reproducibles | Aprobada: 50 pruebas |

### Primera suite automatizada

Ejecución: 2026-08-11.

- Se agregó configuración de `pytest` y dependencias en
  `requirements-dev.txt`.
- Se crearon 46 pruebas unitarias y HTTP sin escritura, más 4 pruebas de
  integración transaccionales contra SQL Server.
- Resultado final: 50 aprobadas, 0 fallidas y 0 advertencias.
- Cobertura global final: 87%.
- Cobertura de seguridad, schemas y fusión: 100%.
- Se probaron reglas auxiliares, signos de alarma actuales, umbrales de FR,
  límites de edad, validaciones demográficas, JWT y contratos HTTP básicos.
- Se actualizó la configuración de schemas a `ConfigDict` para compatibilidad
  con Pydantic 2 y eliminar advertencias de deprecación.
- Autenticación, roles, CRUD de pacientes, evaluaciones con modelo tabular y
  radiografías con predictor simulado se prueban con persistencia real.
- Cada prueba de integración usa una transacción externa y termina con
  `ROLLBACK`; se confirmó que los conteos de usuarios, pacientes, evaluaciones
  y radiografías permanecen idénticos antes y después.
- El predictor CNN real se mantiene fuera de la suite rápida; su inferencia fue
  validada manualmente en la Fase 5.
- La suite se ejecuta con:

```powershell
.\env\Scripts\python.exe -m pytest --cov=app --cov-report=term-missing
```

### Manejo global de errores

Ejecución: 2026-08-11.

- Se agregó un contrato uniforme bajo `error.code`, `error.message` y, cuando
  aplica, `error.details`.
- Se implementaron manejadores globales para errores HTTP, validación de
  Pydantic, SQLAlchemy y excepciones inesperadas.
- Los detalles de validación no devuelven el valor recibido, evitando reflejar
  contraseñas u otros inputs sensibles.
- Los errores SQL devuelven HTTP 503 sin consultas, parámetros, credenciales ni
  mensajes del driver.
- Los errores inesperados devuelven HTTP 500 con texto genérico.
- Se conservan encabezados de seguridad como `WWW-Authenticate`.
- Las sesiones ejecutan `rollback()` automáticamente cuando una solicitud
  termina con excepción.
- El mensaje automático `Not authenticated` fue normalizado al español.
- Regresión final: 54 pruebas aprobadas, cobertura global 88% y conteos de SQL
  Server sin cambios.

### Configuración por entornos

Ejecución: 2026-08-11.

- Se centralizó la configuración en un objeto `Settings` validado con Pydantic.
- Se definieron los entornos `development`, `testing` y `production` mediante
  `APP_ENV`.
- Producción rechaza `DEBUG=true`, secretos menores de 32 caracteres, secretos
  de ejemplo y CORS con comodín.
- Se agregaron `ENABLE_DOCS`, `LOG_LEVEL` y `CORS_ORIGINS`.
- Swagger, ReDoc y OpenAPI pueden desactivarse por entorno.
- CORS solo se habilita si existen orígenes explícitos y limita métodos y
  encabezados permitidos.
- Se configuró logging de consola con nivel configurable sin imprimir secretos.
- Se validan expiración JWT, tamaño máximo de radiografías y umbral CNN.
- `.env.example` quedó completo y sin credenciales reales.
- Las dependencias de pruebas permanecen separadas en
  `requirements-dev.txt`.
- Regresión final: 67 pruebas aprobadas, cobertura global 88%, configuración
  98% y conteos SQL Server sin cambios.
- Pendiente operativo: reemplazar los orígenes locales de ejemplo por los
  dominios reales del frontend antes de producción.

## Datos temporales creados

Completar durante la ejecución:

| Tipo | Identificador | Nombre o referencia | Estado final |
| --- | --- | --- | --- |
| Usuario | `fc1d526f-3dca-4af3-bfb9-2fab68663063` | `QA_20260809_ESP` (especialista) | Activo, conservar para las siguientes fases |
| Usuario | `95dfff3a-0c2f-44f7-8cee-0c03d8513978` | `QA_20260809_LECT` (lectura) | Activo, conservar para pruebas de permisos |
| Paciente | `8be39383-1aae-4d7b-9a5a-6e652fac03cc` | `PRUEBA_AUTOMATIZADA_20260809_PACIENTE` | Activo, conservar para Fases 3 a 5 |
| Paciente | `af77c1df-df94-456f-8df1-04ccb7fd5827` | `PRUEBA_AUTOMATIZADA_20260809_PACIENTE_F3_ACTUALIZADO` | Inactivo después de completar Fase 3 |
| Evaluación | `ca9a242c-930d-4ff4-a3cf-27e79e8b5600` | Caso ficticio con severidad tabular `Medio` | Activa, con radiografía analizada |
| Evaluación | `381046ee-6e8b-4cc7-9e0f-19e6451482cb` | Copia del caso ficticio para prueba PNG | Activa, con radiografía analizada |
| Radiografía | `ea271b76-996d-42eb-a10d-cb576bd96315` | JPG, `pneumonia_viral`, confianza 0.527403 | Persistida y asociada a la primera evaluación |
| Radiografía | `c5503423-a0ee-4b5f-b089-79a1493374a4` | PNG, `pneumonia_viral`, confianza 0.527403 | Persistida y asociada a la segunda evaluación |

## Registro de incidencias

| ID | Prueba relacionada | Prioridad | Descripción | Estado |
| --- | --- | --- | --- | --- |
| INC-001 | Infraestructura de pruebas | P3 | `httpx` estaba ausente; se instaló la versión 0.28.1 en `env` | Resuelta |
| INC-002 | ND-10 | P2 | `/decision/auxiliary` es público; definir si debe exigir autenticación por tratar datos clínicos | Abierta |
| INC-003 | ND-06 a ND-09 | P3 | El mensaje automático `Not authenticated` se normalizó a `No se proporcionaron credenciales de autenticación` | Resuelta |
| INC-004 | Infraestructura de pruebas | P3 | `httpx` y las herramientas de prueba quedaron declaradas en `requirements-dev.txt`, separadas de producción | Resuelta |
| INC-005 | AU-01 | P2 | `RegisterRequest.user_name` no limitaba 40 caracteres; se agregó `max_length=40` y la regresión devuelve HTTP 422 para 41 caracteres sin alterar la base de datos | Resuelta |
| INC-006 | PA-02 | P1 | Se agregaron reglas para alta y actualización: edad >= 0, peso > 0 y <= 150 kg, talla > 0 y <= 250 cm, y sexo `M/F`. Las regresiones inválidas devuelven HTTP 422 | Resuelta |
| INC-007 | PA-08 | P2 | La consulta normal por ID ahora oculta pacientes inactivos con HTTP 404. El servicio permite recuperación interna únicamente con `include_inactive=True` para historial o administración | Resuelta |
| INC-008 | PA-01 | P2 | La unidad ambigua de `Patients.age` se resolvió renombrando el campo a `age_months`; el rango final 0–72 coincide con el entrenamiento confirmado del modelo y preservó los valores existentes | Resuelta |
| INC-009 | EV-01 | P1 | La tabla `Evaluations` no tenía seis campos requeridos por el ORM. Se agregaron mediante `003_sync_evaluations_clinical_fields.sql`; la inferencia y persistencia posteriores fueron correctas | Resuelta |
| INC-010 | QT-07 | P2 | Se autorizó usar la base actual para testing. Las pruebas CRUD usan transacciones reales con rollback y no dejan registros persistentes | Resuelta |
| INC-011 | AU-01 | P2 | `UserBase.email` no limitaba los 50 caracteres de SQL Server. Se agregó `max_length=50` y una prueba de frontera | Resuelta |

## Formato para evidencias

Para cada prueba ejecutada registrar:

```text
ID:
Fecha y hora:
Endpoint o función:
Datos usados (sin secretos):
Resultado esperado:
Código HTTP obtenido:
Resultado obtenido:
Estado:
Incidencia relacionada:
```

## Criterio de cierre

El ciclo se considera completado cuando:

- Se ejecuten todas las pruebas aplicables.
- Cada prueba quede marcada como aprobada, fallida o bloqueada.
- Los registros temporales queden identificados y desactivados cuando aplique.
- Cada fallo tenga prioridad y una acción propuesta.
- No existan incidencias P0 abiertas.
- Se genere un resumen final por módulo.

## Instrucción para continuar

En la siguiente sesión solicitar:

> Continúa con las pruebas usando `docs/backlog_pruebas_backend.md`, comenzando
> por la Fase 4 y usando únicamente el paciente temporal activo.

## Punto de control de la sesión 2026-08-09

- Fase 1 terminada: 11 de 11 pruebas aprobadas.
- Fase 2 terminada: 10 de 10 pruebas aprobadas.
- Fase 3 terminada: 9 de 9 pruebas funcionales aprobadas.
- Fase 4 terminada: 9 de 9 pruebas aprobadas.
- Fase 5 terminada: 11 de 11 pruebas aprobadas.
- Total ejecutado: 50 pruebas aprobadas, más una comprobación adicional de
  permisos de radiografías.
- Existen dos evaluaciones temporales con severidad tabular `Medio` y dos
  radiografías temporales analizadas.
- Se conservan activos un especialista, un usuario de lectura y un paciente de
  prueba para continuar.
- El segundo paciente de prueba permanece inactivo después de validar la
  desactivación lógica.
- Se corrigió el límite de 40 caracteres de `user_name`.
- Se agregaron validaciones de edad, peso, talla y sexo para pacientes.
- Los pacientes inactivos ya no son visibles mediante la consulta normal por
  ID.
- La edad quedó estandarizada entre 0 y 72 meses en pacientes, evaluaciones,
  decisión auxiliar y SQL Server.
- Se ejecutó la migración `002_standardize_patient_age_months.sql` y se comprobó
  que es idempotente.
- Se ejecutó `004_limit_age_to_72_months.sql`; los límites 72/73 se probaron en
  los tres contratos sin modificar registros.
- Próximo paso: ejecutar la Fase 6 de decisión auxiliar y recomendaciones con
  escenarios controlados bajo, medio, alto y signos de alarma.
- Se creó `docs/matriz_reglas_clinicas_v1.md` como borrador trazable basado en
  CENETEC y OMS. Antes de modificar las reglas o cerrar la Fase 6 requiere
  revisión y aprobación de un profesional clínico.

## Punto de control para validación clínica

Fecha: 2026-08-09.

Revisora propuesta: médica adscrita de pediatría, pendiente de registrar nombre
y conformidad.

Material para revisión:

- `docs/matriz_reglas_clinicas_v1.md`.
- Caso ficticio de 36 meses con severidad tabular `Medio`.
- Resultado radiográfico `pneumonia_viral` con confianza 0.527403 e
  interpretación `indeterminate`.

Decisiones solicitadas a la especialista:

- [ ] Confirmar umbrales de frecuencia respiratoria para 0–1, 2–11, 12–59 y
  60–72 meses.
- [ ] Confirmar manejo y nivel de precaución para menores de 2 meses.
- [ ] Confirmar el umbral o interpretación de Glasgow.
- [ ] Diferenciar rechazo parcial al alimento de incapacidad para beber o
  alimentarse.
- [ ] Confirmar qué signos aislados o combinaciones requieren valoración
  prioritaria o urgente.
- [ ] Revisar tiraje, retracción xifoidea, quejido y aleteo nasal.
- [ ] Confirmar textos de las recomendaciones y nota de seguridad.
- [ ] Identificar campos clínicos faltantes en el formulario.
- [ ] Confirmar el manejo de discordancia entre clínica y radiografía.
- [ ] Registrar reglas aprobadas, rechazadas o modificadas y, cuando sea
  posible, su fuente clínica.

Condición para reanudar la Fase 6:

- Recibir observaciones de la especialista.
- Actualizar y versionar la matriz.
- Registrar quién revisó, fecha y alcance de la revisión.
- Implementar únicamente las reglas aprobadas.
- Ejecutar DE-01 a DE-10 con casos controlados.

## Punto de control de arquitectura - punto 4

Fecha: 2026-08-11.

- [x] Se instaló y configuró Alembic 1.16.5.
- [x] Se creó la revisión base `20260811_0001` para SQL Server.
- [x] La detección se limitó a `Roles`, `Users`, `Patients`, `Evaluations` y
  `Radiographs`, sin incluir tablas ajenas presentes en la misma base.
- [x] La base de pruebas existente se marcó en `head`; no se ejecutaron cambios
  sobre los registros clínicos existentes.
- [x] Una base temporal vacía pasó `upgrade head`: se generaron las cinco
  tablas, los tres roles iniciales y la versión esperada.
- [x] Se comprobó `downgrade base` y después se eliminó la base temporal.
- [x] La prueba inicial descubrió y permitió corregir el uso requerido de
  `IDENTITY_INSERT` para los IDs fijos de `Roles`.
- [x] Se añadió una prueba automatizada que compara la revisión activa con la
  cabeza de Alembic.
- [x] El procedimiento quedó documentado en `docs/migraciones.md`.
