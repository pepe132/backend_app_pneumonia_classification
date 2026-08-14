# Pendientes del backend v1

Este documento resume lo que falta por implementar en el backend de la aplicacion de apoyo clinico para clasificacion de severidad en neumonia pediatrica.

El objetivo general de la aplicacion es permitir que personal medico autorizado registre pacientes pediatricos, capture datos clinicos, cargue radiografias de torax cuando aplique, obtenga una clasificacion auxiliar de severidad mediante modelos de Machine Learning y Deep Learning, consulte recomendaciones orientativas, historial, estadisticas y reportes. La aplicacion no sustituye el criterio medico profesional.

## Estado actual del backend

Ya existe una base funcional del backend con FastAPI, SQLAlchemy y SQL Server.

Implementado actualmente:

- Modulo de autenticacion con registro, login, JWT y endpoint de usuario actual.
- Bloqueo de registro publico de usuarios administradores.
- Roles basicos: administrador, especialista/medico y consulta/lectura.
- Modulo de pacientes con creacion, listado, busqueda, consulta, actualizacion y desactivacion logica.
- Modulo de evaluaciones clinicas con formulario tabular, validaciones y relacion con paciente.
- Prediccion tabular conectada al modelo `modelo_neumonia_app.pkl`.
- Persistencia de severidad tabular y probabilidades baja, media y alta.
- Historial de evaluaciones por paciente.
- Modulo de radiografias con carga JPG/PNG, validacion de archivo, almacenamiento local y consulta.
- Predictor de imagen preparado para cargar un modelo CNN desde `CNN_MODEL_PATH`.
- Persistencia de resultado radiografico, confianza y probabilidades por clase.
- Logica de fusion v1 entre resultado tabular y radiografia.
- Capa auxiliar que combina ML, DL y datos clinicos originales.
- Manejo comun de errores, configuracion por entorno, CORS y logging.
- Migraciones formales con Alembic para el esquema completo.
- Suite automatizada con 68 pruebas aprobadas al 2026-08-11.
- Documentacion tecnica inicial en `docs/`.

## Pendientes principales

### 1. Recomendaciones clinicas auxiliares

Estado: implementada tecnicamente; pendiente de validacion clinica.

Implementado:

- Servicio `app/services/auxiliary_decision.py`.
- Endpoint `POST /decision/auxiliary`.
- Integracion automática al analizar una radiografia.
- Combinacion del resultado ML, resultado DL y datos clinicos originales.
- Hallazgos relevantes, clasificacion auxiliar, recomendacion y nota de seguridad.
- Persistencia de codigo y version de fusion en la evaluacion.
- Pruebas unitarias, de contrato e integracion.

Pendiente:

- Validar y complementar `docs/matriz_reglas_clinicas_v1.md` con la especialista.
- Ejecutar los escenarios DE-01 a DE-10 de la Fase 6.
- Definir si el texto final se conserva como snapshot historico.
- Decidir si se requiere un endpoint de consulta independiente por evaluacion.

### 2. Permisos y control de acceso por rol

Estado: implementado en rutas actuales y cubierto por pruebas automatizadas;
pendiente cerrar la regla de visibilidad de datos.

Ya existe `require_roles` y las rutas clinicas principales ya distinguen entre usuarios de escritura y usuarios de lectura.

Por implementar:

- Revisar si el usuario debe ver todos los pacientes o solo los creados por el mismo, segun la regla de negocio final.

Implementado:

- Creacion, edicion y eliminacion logica de pacientes restringidas a administrador y especialista.
- Creacion de evaluaciones restringida a administrador y especialista.
- Carga de radiografias restringida a administrador y especialista.
- Rol consulta/lectura puede consultar pacientes, evaluaciones y radiografias, pero no modificarlos.

### 3. Administracion de usuarios

Estado: pendiente.

Actualmente existe registro publico controlado y login, pero no hay modulo administrativo completo.

Por implementar:

- Listar usuarios.
- Consultar usuario por ID.
- Crear usuarios desde rol administrador.
- Editar usuario, rol y estado activo/inactivo.
- Desactivar usuarios.
- Evitar eliminacion fisica de usuarios con informacion clinica asociada.
- Definir flujo para cambio o restablecimiento de contrasena.

### 4. Recuperacion o cambio de contrasena

Estado: pendiente.

Por implementar:

- Endpoint para cambio de contrasena del usuario autenticado.
- Endpoint administrativo para restablecer contrasena.
- Opcional para version futura: recuperacion por correo/token temporal.
- Validaciones de longitud, seguridad y expiracion si se usan tokens.

### 5. Verificacion operativa del modelo CNN

Estado: preparado en codigo, pendiente de validacion real.

El predictor de radiografias ya intenta cargar TensorFlow y el archivo configurado en `CNN_MODEL_PATH`, pero falta comprobar la integracion en el entorno real.

Por implementar/verificar:

- Confirmar ubicacion final del archivo `.keras`.
- Confirmar que TensorFlow funciona en el entorno del backend.
- Probar inferencia con imagenes JPG/PNG reales.
- Validar que la salida del modelo contenga las cuatro clases esperadas.
- Documentar variables `.env` relacionadas con radiografias.
- Definir comportamiento si el modelo no esta disponible en produccion.

### 6. Dashboard y estadisticas

Estado: pendiente.

Por implementar:

- Total de pacientes activos.
- Total de evaluaciones.
- Evaluaciones por severidad final.
- Evaluaciones por severidad tabular.
- Conteo de radiografias analizadas.
- Distribucion de clases radiograficas.
- Tendencias por fecha.
- Estadisticas por paciente o por periodo.
- Endpoints protegidos para dashboard.
- Definir si el dashboard sera visible para administrador, especialista y consulta/lectura.

### 7. Reportes

Estado: pendiente.

Por implementar:

- Endpoint de reporte individual por evaluacion.
- Incluir datos del paciente, datos clinicos, resultado tabular, resultado radiografico si existe, fusion y recomendaciones.
- Vista/estructura lista para impresion desde frontend.
- Opcional: generacion de PDF.
- Reportes generales o estadisticos para administracion.
- Control de acceso por rol.

### 8. Busqueda y filtros avanzados

Estado: parcialmente implementado.

Actualmente hay busqueda simple de pacientes por nombre.

Por implementar:

- Buscar pacientes por expediente o identificador si se agrega ese campo.
- Filtros por edad, sexo, fecha de registro o estado.
- Filtros de evaluaciones por paciente, severidad, fecha y usuario creador.
- Paginacion consistente en listados.
- Ordenamiento configurable.

### 9. Validacion de base de datos y migraciones

Estado: implementado.

Implementado:

- Alembic configurado para SQL Server y limitado a las tablas de la aplicacion.
- Revision base `20260811_0001` con las cinco tablas y sus restricciones.
- Carga inicial de los roles administrador, especialista y lectura.
- Base de pruebas existente marcada en `head` sin alterar sus datos.
- Creacion y reversion verificadas en una base temporal limpia.
- Flujo operativo documentado en `docs/migraciones.md`.
- Los scripts SQL `001` a `004` se conservan como historial previo a Alembic.

### 10. Configuracion de entorno

Estado: implementada; pendiente definir dominios reales del frontend para CORS.

El archivo `.env.example` documenta desarrollo, pruebas, produccion, SQL
Server, JWT, CORS, logging, documentacion, radiografias y CNN.

Implementado:

- Variables requeridas y valores de ejemplo seguros.
- Perfiles `development`, `testing` y `production`.
- Validacion reforzada de secretos, CORS y debug en produccion.
- Logging, documentacion OpenAPI condicional y limites operativos.

Pendiente:

- Definir los dominios reales del frontend en `CORS_ORIGINS`.

### 11. Manejo de errores y respuestas API

Estado: implementado y cubierto por pruebas automatizadas.

Implementado:

- Formato comun `{ "error": { "code", "message", "details" } }`.
- Manejo de errores HTTP, validacion, SQLAlchemy y fallos inesperados.
- Codigos diferenciados para autenticacion, permisos, ausencia, conflicto,
  validacion y servicio no disponible.
- Pruebas automatizadas del contrato de errores.

Pendiente:

- Corregir textos antiguos con problemas de codificacion de caracteres.
- Mantener el contrato sincronizado con el frontend movil.

### 12. Pruebas automatizadas

Estado: implementadas y en crecimiento.

Resultado actual: 68 pruebas aprobadas al 2026-08-11.

Cobertura funcional:

- Autenticacion, JWT y permisos por rol.
- Esquemas y validaciones clinicas.
- Pacientes y evaluaciones con SQL Server y rollback.
- Prediccion tabular, radiografias y predictor simulado/real controlado.
- Fusion y decision auxiliar.
- Configuracion, errores y contratos HTTP.
- Revision activa de Alembic.

Pendiente:

- Agregar los casos clinicos DE-01 a DE-10 cuando las reglas sean aprobadas.
- Incorporar pruebas de los modulos futuros de usuarios, dashboard y reportes.

## Pendientes secundarios

- Revisar nombres y consistencia de severidades: `Bajo`, `Medio`, `Alto` frente a codigos internos.
- Revisar acentos/caracteres en textos de respuesta, ya que algunos archivos muestran caracteres mal codificados.
- Estandarizado: `age_months` representa la edad del paciente en meses (0 a 72), que corresponde al rango de entrenamiento confirmado del modelo tabular.
- Agregar campo de expediente o identificador clinico si sera necesario para busqueda real.
- Revisar relaciones ORM entre paciente y evaluaciones.
- Revisar si se necesita auditoria de cambios clinicos.
- Revisar si se requiere borrado logico tambien para evaluaciones.
- Revisar limite y estrategia de almacenamiento de radiografias.

## Orden recomendado de implementacion

1. Validar y versionar la matriz de reglas con la especialista.
2. Ejecutar la Fase 6 de pruebas clínicas controladas.
3. Documentar los contratos actuales para el frontend móvil.
4. Validar el modelo CNN definitivo en el entorno objetivo.
5. Agregar administracion de usuarios y cambio de contrasena.
6. Implementar dashboard basico y reportes.
7. Agregar filtros avanzados y paginacion.
8. Completar decisiones de auditoria, privacidad y despliegue.

## Relacion con el frontend movil

Los pendientes del cliente React Native/Expo se encuentran en
`docs/pendientes_frontend_mobile_v1.md`.

El frontend puede comenzar con autenticacion, pacientes, evaluaciones,
radiografias y visualizacion de la fusion. Las recomendaciones y reglas de
alarma deben mostrarse como provisionales hasta concluir la validacion clinica.
