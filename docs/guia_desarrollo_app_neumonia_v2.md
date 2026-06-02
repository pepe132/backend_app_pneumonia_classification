# Guía de desarrollo por fases

## Propósito

Este archivo sirve como guía técnica para desarrollar la aplicación por módulos, evitando mezclar responsabilidades y permitiendo avanzar de manera ordenada.

## Fase 1. Configuración base del proyecto

### Objetivo

Preparar la base de FastAPI, SQL Server, SQLAlchemy y configuración general del backend.

### Componentes

- `app/main.py`
- `app/core/config.py`
- `app/core/database.py`
- `.env`
- `requirements.txt`

### Actividades

- Configurar FastAPI.
- Configurar conexión a SQL Server.
- Configurar variables de entorno.
- Probar conexión a base de datos.
- Crear estructura modular.

## Fase 2. Autenticación

### Objetivo

Permitir registro, login y validación de usuario autenticado.

### Componentes

- `app/modules/auth/models.py`
- `app/modules/auth/schema.py`
- `app/modules/auth/service.py`
- `app/modules/auth/router.py`
- `app/core/security.py`

### Endpoints sugeridos

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Reglas

- Las contraseñas deben guardarse hasheadas.
- El login debe generar JWT.
- El usuario inactivo no debe poder iniciar sesión.
- El registro público no debe permitir crear administradores.

## Fase 3. Protección por roles

### Objetivo

Controlar el acceso a los módulos según el rol del usuario.

### Componentes

- `app/core/dependencies.py`

### Funciones

- `get_current_user`
- `require_roles`

### Roles

- `1 = Administrador`
- `2 = Especialista/Médico`
- `3 = Consulta/Lectura`

### Reglas

- Administrador puede gestionar usuarios y configuración.
- Especialista/Médico puede registrar pacientes y evaluaciones.
- Consulta/Lectura solo puede visualizar información.

## Fase 4. Módulo de pacientes

### Objetivo

Registrar y consultar pacientes pediátricos.

### Carpeta sugerida

`app/modules/patients/`

### Archivos

- `models.py`
- `schema.py`
- `service.py`
- `router.py`

### Endpoints sugeridos

- `POST /patients`
- `GET /patients`
- `GET /patients/{patient_id}`
- `PUT /patients/{patient_id}`
- `DELETE /patients/{patient_id}` o baja lógica

### Permisos

- Crear: Administrador, Especialista/Médico.
- Editar: Administrador, Especialista/Médico.
- Consultar: Administrador, Especialista/Médico, Consulta/Lectura.
- Eliminar: preferentemente solo Administrador o usar baja lógica.

## Fase 5. Evaluaciones clínicas tabulares

### Objetivo

Capturar datos clínicos del paciente y enviarlos al modelo tabular.

### Carpeta sugerida

`app/modules/evaluations/`

### Variables clínicas sugeridas

edad_meses
peso_kg
fr
fc
temperatura_c
spo2
tiraje
aleteo_nasal
quejido_espiratorio
cianosis
apnea
rechazo_comer
vomita_todo
convulsiones
glasgow
desnutricion
antecedentes_cronicos
sibilancias
dias_sintomas
dias_fiebre
dias_tos
dias_dificultad_respiratoria
crepitantes
disminucion_murmullo_vesicular
dolor_toracico

### Endpoints sugeridos

- `POST /evaluations`
- `GET /evaluations`
- `GET /evaluations/{evaluation_id}`
- `GET /patients/{patient_id}/evaluations`

# prompt
✦ Para implementar la Fase 5 (Evaluaciones Clínicas) de manera sólida y alineada con la arquitectura de "Clean Code" que
  ya tiene el proyecto, te propongo el siguiente planteamiento técnico.

  Overview de la Implementación (Fase 5)

  La Fase 5 se centrará en la captura y persistencia de los datos. Aunque la Fase 6 es la de predicción, dejaremos la
  estructura lista para que la integración sea natural.

  1. Ubicación Arquitectónica
  Crearemos un nuevo módulo en app/modules/evaluations/. Este módulo será el responsable de todo lo relacionado con los
  signos vitales y hallazgos clínicos del paciente.

  2. Diseño del Modelo de Datos (models.py)
  La tabla Evaluations (o Evaluaciones) actuará como el "expediente clínico" de un momento dado. Sugiero que contenga:
   * Metadatos: evaluation_id, patient_id (FK), created_by (FK al médico), created_at.
   * Variables Clínicas: Los 25 campos mencionados en la guía (edad_meses, fr, fc, temperatura, spo2, tiraje, etc.).
   * Campos de Predicción (Preparación para Fase 6): Añadiremos columnas para severity_tabular y las probabilidades
     (prob_low, prob_medium, prob_high). En esta fase se guardarán como NULL o valores por defecto, y en la Fase 6 el
     servicio de ML las actualizará.

  3. Validación y Tipado (schema.py)
  Utilizaremos Pydantic para asegurar que los datos que ingresan son válidos:
   * Validar rangos lógicos (ej. Temperatura entre 30°C y 45°C).
   * Validar tipos de datos (Booleanos para signos como cianosis o apnea, Flotantes/Enteros para signos vitales).

  4. Flujo de Trabajo Sugerido
   1. POST /evaluations: El especialista envía el formulario.
   2. Service: El servicio valida que el patient_id existe, guarda los datos en la DB.
   3. Respuesta: Devuelve el objeto de evaluación creado.
   4. (Nota: En la Fase 6, entre el paso 2 y 3, insertaremos la llamada al modelo de Machine Learning).

  5. Endpoints a Implementar
   * POST /evaluations: Crear registro.
   * GET /patients/{patient_id}/evaluations: Ver el historial de evaluaciones de un niño en particular.
   * GET /evaluations/{evaluation_id}: Ver el detalle de una evaluación específica.

## Fase 6. Modelo tabular

### Objetivo

Integrar el modelo de Machine Learning para predecir severidad a partir de datos clínicos.

### Carpeta sugerida

`app/modules/predictions/`

### Componentes

- Carga del modelo.
- Preprocesamiento de variables.
- Validación de rangos.
- Predicción.
- Probabilidades por clase.

### Salida esperada

- Severidad baja, media o alta.
- Probabilidades por clase.
- Versión del modelo.
- Fecha/hora de predicción.

## Fase 7. Radiografías y modelo de imagen

### Objetivo

Permitir carga de radiografías y clasificación mediante modelo de Deep Learning.

### Carpeta sugerida

`app/modules/images/`

### Endpoints sugeridos

- `POST /patients/{patient_id}/xray`
- `POST /images/{image_id}/predict`
- `GET /patients/{patient_id}/images`

### Reglas

- Validar tipo y tamaño de archivo.
- Asociar imagen a paciente y evaluación.
- Guardar ruta o referencia, no necesariamente el archivo dentro de la base de datos.
- Mantener control de acceso.

## Fase 8. Clasificación integrada

### Objetivo

Combinar resultado del modelo tabular y modelo de imagen para generar una severidad final auxiliar.

### Consideraciones

- Si no hay radiografía, la severidad puede basarse solo en el modelo tabular.
- Si hay radiografía, se integran ambas salidas.
- El sistema debe mostrar resultados individuales y resultado final.
- Debe conservar probabilidades y nivel de confianza.

### Salida sugerida

- Resultado tabular.
- Resultado imagen.
- Severidad final sugerida.
- Recomendaciones asociadas.
- Advertencias o limitaciones.

## Fase 9. Recomendaciones clínicas

### Objetivo

Mostrar recomendaciones auxiliares según la severidad.

### Reglas

- No redactar como prescripción automática.
- Usar lenguaje de apoyo clínico.
- Indicar que deben validarse con criterio médico.
- Permitir actualización futura de reglas o protocolos.

## Fase 10. Historial

### Objetivo

Consultar la evolución de un paciente a través de sus evaluaciones.

### Funciones

- Ver evaluaciones previas.
- Comparar resultados.
- Consultar radiografías asociadas.
- Revisar recomendaciones emitidas.
- Filtrar por fecha o severidad.

## Fase 11. Dashboard y estadísticas

### Objetivo

Visualizar indicadores generales.

### Indicadores sugeridos

- Total de pacientes.
- Total de evaluaciones.
- Distribución por severidad.
- Casos con radiografía.
- Resultados por modelo.
- Evolución temporal.
- Distribución por edad y sexo.

## Fase 12. Reportes

### Objetivo

Generar reportes clínicos o administrativos.

### Reportes sugeridos

- Reporte individual del paciente.
- Reporte de evaluación.
- Reporte por severidad.
- Reporte estadístico.
- Exportación PDF.
- Exportación Excel.

## Fase 13. Auditoría

### Objetivo

Registrar acciones importantes del sistema.

### Eventos sugeridos

- Login.
- Registro de usuario.
- Creación de paciente.
- Edición de paciente.
- Creación de evaluación.
- Ejecución de predicción.
- Carga de radiografía.
- Consulta de reportes.

## Orden recomendado

1. Auth.
2. Roles.
3. Pacientes.
4. Evaluaciones.
5. Modelo tabular.
6. Radiografías.
7. Modelo de imagen.
8. Integración de resultados.
9. Recomendaciones.
10. Historial.
11. Dashboard.
12. Reportes.
13. Auditoría.
