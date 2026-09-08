# Arquitectura y Clean Code del backend

## Objetivo

Definir reglas de arquitectura, organización y limpieza de código para el backend de la aplicación.

## Stack principal

- Python.
- FastAPI.
- SQLAlchemy.
- SQL Server.
- JWT.
- Pydantic.
- Modelos ML/DL serializados.
- Uvicorn para desarrollo.

## Principios generales

### Separación de responsabilidades

Cada archivo debe tener una responsabilidad clara:

- `models.py`: modelos SQLAlchemy.
- `schema.py`: schemas Pydantic.
- `service.py`: lógica de negocio.
- `router.py`: endpoints HTTP.
- `dependencies.py`: dependencias reutilizables.
- `security.py`: funciones de seguridad.
- `database.py`: conexión a base de datos.
- `config.py`: configuración y variables de entorno.

El router no debe contener lógica pesada de negocio.

### Estructura modular

Cada módulo funcional debe tener su propia carpeta:

```text
app/
  core/
    config.py
    database.py
    security.py
    dependencies.py
  modules/
    auth/
      models.py
      schema.py
      service.py
      router.py
    patients/
      models.py
      schema.py
      service.py
      router.py
    evaluations/
      models.py
      schema.py
      service.py
      router.py
    predictions/
      service.py
      router.py
    images/
      models.py
      schema.py
      service.py
      router.py
```

## Reglas para routers

Los routers deben:

- Declarar endpoints.
- Recibir datos de entrada.
- Validar permisos con `Depends`.
- Llamar funciones del servicio.
- Retornar respuestas.
- Manejar códigos HTTP.

Los routers no deben:

- Hacer queries directos complejos.
- Hashear contraseñas.
- Procesar modelos ML directamente.
- Tener lógica clínica compleja.
- Contener reglas extensas de negocio.

## Reglas para servicios

Los servicios deben:

- Contener la lógica de negocio.
- Coordinar modelos, repositorios y validaciones.
- Ejecutar reglas clínicas o de integración.
- Preparar respuestas para routers.

Los servicios no deben:

- Depender directamente de detalles HTTP.
- Levantar demasiadas excepciones HTTP salvo que el diseño lo permita.
- Mezclar responsabilidades de otros módulos.

## Reglas para modelos

Los modelos SQLAlchemy deben:

- Representar fielmente las tablas.
- Usar nombres reales de columnas.
- Definir relaciones claras.
- Evitar lógica de negocio.

Ejemplo:

```python
class User(Base):
    __tablename__ = "Users"
    __table_args__ = {"schema": "dbo"}

    user_id = Column(String(40), primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
```

## Reglas para schemas

Los schemas Pydantic deben:

- Validar datos de entrada.
- Evitar exponer campos sensibles.
- Separar schemas de request y response.
- No devolver contraseñas.
- Usar `EmailStr`, `Field`, `Optional` cuando aplique.

Ejemplo:

```python
class LoginRequest(BaseModel):
    email: EmailStr
    user_password: str = Field(..., min_length=8, max_length=72)
```

## Seguridad

### Contraseñas

- Nunca guardar contraseñas en texto plano.
- Usar bcrypt mediante passlib.
- Limitar contraseña a 72 caracteres por compatibilidad con bcrypt.
- Guardar solo el hash.

### JWT

El token debe incluir:

- `sub`: identificador del usuario.
- `email`: correo.
- `role_id`: rol del usuario.
- `exp`: expiración.

### Rutas protegidas

Usar:

- `get_current_user`
- `require_roles`

Ejemplo:

```python
@router.post("/patients")
def create_patient(current_user=Depends(require_roles([1, 2]))):
    ...
```

## Manejo de errores

Usar códigos HTTP adecuados:

- `400`: datos inválidos o reglas de negocio incumplidas.
- `401`: usuario no autenticado o token inválido.
- `403`: usuario autenticado sin permisos.
- `404`: recurso no encontrado.
- `409`: conflicto, por ejemplo email duplicado.
- `500`: error interno inesperado.

## Nombres recomendados

### Funciones

Usar nombres claros:

- `get_user_by_email`
- `create_patient`
- `predict_tabular_severity`
- `upload_xray_image`
- `generate_recommendations`

### Variables

Evitar nombres ambiguos como:

- `data`
- `x`
- `obj`
- `temp`

Preferir:

- `patient_data`
- `evaluation_data`
- `current_user`
- `prediction_result`

## Comentarios

Usar comentarios solo cuando agreguen valor. No comentar lo obvio.

Bueno:

```python
# No permitir creación pública de administradores
if user_data.role_id == 1:
    ...
```

Malo:

```python
# Suma uno
x = x + 1
```

## Buenas prácticas

- Mantener funciones pequeñas.
- Evitar duplicación.
- Validar datos desde schemas.
- Centralizar reglas reutilizables.
- No mezclar SQL directo con ORM salvo necesidad.
- Usar variables de entorno.
- No subir `.env` al repositorio.
- No exponer información sensible en errores.
- Mantener consistencia en idioma de nombres. Preferentemente inglés en código y español en mensajes si la app será para usuarios hispanohablantes.

## Reglas para modelos de Machine Learning

Los modelos deben estar aislados en servicios dedicados.

Ejemplo:

```text
app/modules/predictions/
  tabular_model.py
  image_model.py
  service.py
```

El endpoint no debe cargar el modelo cada vez. Los modelos deben cargarse una vez al iniciar o mediante un servicio reutilizable.

## Reglas para recomendaciones clínicas

- Las recomendaciones deben ser auxiliares.
- No usar lenguaje de prescripción obligatoria.
- Incluir advertencia clínica.
- Permitir actualizar recomendaciones sin tocar el modelo ML.
- Separar reglas de recomendación de la lógica del router.

## Checklist antes de cerrar cada módulo

- ¿Tiene router, schema, service y model si aplica?
- ¿Tiene validación de entrada?
- ¿Tiene permisos por rol?
- ¿No expone datos sensibles?
- ¿Maneja errores comunes?
- ¿Está incluido en `main.py`?
- ¿Se probó en Swagger/Postman?
