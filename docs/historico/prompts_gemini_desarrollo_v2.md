# Prompts base para Gemini durante el desarrollo

## Cómo usar este archivo

Usa estos prompts para pedir a Gemini que genere código de forma controlada, módulo por módulo. Evita pedir toda la aplicación de una sola vez.

## Prompt base de contexto

```text
Estoy desarrollando una API en FastAPI para el proyecto:

"Sistema inteligente de apoyo clínico para la clasificación de severidad en neumonía pediátrica mediante modelos de Machine Learning y Deep Learning".

La aplicación usa:
- FastAPI
- SQL Server
- SQLAlchemy
- JWT
- passlib con bcrypt
- Pydantic
- Arquitectura modular

La app permitirá:
- Registro y login de usuarios.
- Gestión de roles.
- Gestión de pacientes pediátricos.
- Captura de evaluaciones clínicas.
- Predicción con modelo tabular de Machine Learning.
- Carga opcional de radiografía.
- Predicción con modelo de Deep Learning de imágenes.
- Integración de resultados para clasificar severidad.
- Recomendaciones clínicas auxiliares.
- Historial, dashboard y reportes.

Importante:
- La app es de apoyo clínico.
- No sustituye el criterio médico.
- No da diagnóstico definitivo.
- No prescribe medicamentos automáticamente.
- Las recomendaciones son orientativas.

Respeta mi estructura de carpetas y genera código limpio, modular y mantenible.
```

## Prompt para inspeccionar tabla con MCP SQL Server

```text
Usa el MCP de SQL Server para inspeccionar la tabla dbo.NOMBRE_TABLA.

Necesito:
1. Columnas.
2. Tipos de datos.
3. Primary key.
4. Foreign keys.
5. Relaciones.
6. Si tiene campos de auditoría.
7. Si hay campos nullable.

Después genera el modelo SQLAlchemy respetando exactamente los nombres reales.
```

## Prompt para generar un módulo nuevo

```text
Genera el módulo NOMBRE_MODULO para mi API FastAPI.

Estructura esperada:

app/modules/NOMBRE_MODULO/
  models.py
  schema.py
  service.py
  router.py

Requisitos:
- Usar SQLAlchemy para modelos.
- Usar Pydantic para schemas.
- Usar service.py para lógica de negocio.
- Usar router.py solo para endpoints.
- Usar Depends(get_db).
- Usar require_roles cuando el endpoint deba estar protegido.
- No mezclar lógica de negocio dentro del router.
- Entregar código archivo por archivo.
```

## Prompt para generar router

```text
Genera únicamente router.py para el módulo NOMBRE_MODULO.

Reglas:
- Usar APIRouter.
- Usar Depends(get_db).
- Usar Depends(require_roles([...])) según permisos.
- No colocar lógica pesada en el router.
- Llamar funciones del service.py.
- Manejar errores HTTP correctamente.
- Entregar solo el código de router.py.
```

## Prompt para generar service

```text
Genera únicamente service.py para el módulo NOMBRE_MODULO.

Reglas:
- Contener lógica de negocio.
- Recibir db: Session cuando necesite base de datos.
- Usar modelos SQLAlchemy.
- No usar objetos Request o Response.
- No mezclar lógica HTTP.
- Retornar objetos o datos claros para el router.
- Manejar validaciones de negocio.
```

## Prompt para generar schema

```text
Genera únicamente schema.py para el módulo NOMBRE_MODULO.

Reglas:
- Usar Pydantic.
- Separar schemas de entrada y salida.
- No exponer campos sensibles.
- Usar EmailStr, Field, Optional cuando aplique.
- Usar from_attributes=True.
- Agregar validaciones mínimas necesarias.
```

## Prompt para revisar código

```text
Revisa este código y dime:
1. Si tiene errores.
2. Si respeta Clean Code.
3. Si respeta separación router/service/schema/model.
4. Si hay riesgos de seguridad.
5. Si hay problemas con SQLAlchemy o FastAPI.
6. Qué cambiarías antes de probarlo.

No reescribas todo si no es necesario. Primero señala los problemas concretos.
```

## Prompt para integrar modelo tabular

```text
Necesito integrar mi modelo tabular de Machine Learning al backend FastAPI.

El modelo recibe variables clínicas del paciente y devuelve:
- Clase de severidad: baja, media o alta.
- Probabilidades por clase.

Genera una estructura limpia para:
app/modules/predictions/
  schema.py
  service.py
  router.py

Reglas:
- No cargar el modelo en cada request si se puede evitar.
- Validar variables de entrada.
- Retornar probabilidades.
- Guardar resultado asociado a una evaluación.
- No mezclar lógica del modelo en el router.
```

## Prompt para integrar modelo de imagen

```text
Necesito integrar mi modelo de Deep Learning para radiografías de tórax.

El sistema debe:
- Recibir una imagen.
- Validar formato.
- Preprocesar la imagen.
- Ejecutar el modelo.
- Devolver clasificación y probabilidades.
- Asociar resultado al paciente/evaluación.

Genera una estructura limpia usando FastAPI.
No mezcles procesamiento de imagen dentro del router.
```

## Prompt para recomendaciones clínicas

```text
Genera el módulo de recomendaciones clínicas auxiliares.

Las recomendaciones deben depender de la severidad:
- Baja
- Media
- Alta

Reglas:
- No redactar como diagnóstico definitivo.
- No redactar como prescripción automática.
- Usar lenguaje auxiliar.
- Incluir advertencia de que debe validarse con criterio médico.
- Separar las reglas en service.py.
```

## Prompt para dashboard

```text
Genera el módulo de dashboard para estadísticas generales.

Indicadores:
- Total de pacientes.
- Total de evaluaciones.
- Distribución por severidad.
- Casos con radiografía.
- Resultados por modelo.
- Evaluaciones por fecha.

Reglas:
- Solo usuarios Administrador y Consulta/Lectura pueden consultar estadísticas.
- Usar queries eficientes.
- No traer todos los registros si solo se necesitan agregados.
```
