# Herramientas, stack y configuración del proyecto

## Backend

### Lenguaje

- Python 3.11 o superior.

### Framework

- FastAPI.

### Servidor ASGI

- Uvicorn.

Comando de desarrollo:

```bash
uvicorn app.main:app --reload
```

## Base de datos

### Motor

- SQL Server.

### ORM

- SQLAlchemy.

### Driver recomendado

Dependiendo de la configuración:

- `pyodbc`
- SQL Server ODBC Driver 17 o 18.

Ejemplo de paquetes:

```bash
pip install sqlalchemy pyodbc
```

## Autenticación y seguridad

### JWT

Paquete:

```bash
pip install "python-jose[cryptography]"
```

### Hash de contraseñas

Paquetes recomendados:

```bash
pip install passlib==1.7.4 bcrypt==4.0.1
```

Nota: evitar `bcrypt 5.0.0` con `passlib 1.7.4`, porque puede generar errores de compatibilidad.

### Validación de email

```bash
pip install email-validator
```

## Variables de entorno

Usar archivo `.env`.

Ejemplo:

```env
DATABASE_URL=mssql+pyodbc://usuario:password@servidor/base?driver=ODBC+Driver+17+for+SQL+Server
SECRET_KEY=CAMBIAR_POR_CLAVE_SEGURA
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Generar clave segura:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

## Archivo `config.py`

Debe leer configuración desde `.env`.

Ejemplo:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
```

Instalar dotenv:

```bash
pip install python-dotenv
```

## Archivo `database.py`

Debe contener:

- `engine`
- `SessionLocal`
- `Base`
- `get_db`

Ejemplo conceptual:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Dependencias principales

Archivo `requirements.txt` sugerido:

```text
fastapi
uvicorn
sqlalchemy
pyodbc
python-dotenv
python-jose[cryptography]
passlib==1.7.4
bcrypt==4.0.1
email-validator
pydantic
python-multipart
```

Para imágenes/modelos:

```text
numpy
pandas
scikit-learn
xgboost
joblib
tensorflow
pillow
opencv-python
```

Ajustar según los modelos reales que se usen.

## Herramientas de desarrollo

### Swagger

FastAPI genera documentación automática:

```text
http://127.0.0.1:8000/docs
```

### Postman o Insomnia

Útil para probar:

- Login.
- Rutas protegidas.
- Carga de archivos.
- Headers con token.

### Gemini CLI / MCP SQL Server

Usarlo para:

- Inspeccionar tablas.
- Ver columnas y tipos.
- Validar relaciones.
- Generar código basado en la estructura real.

Prompt útil:

```text
Usa el MCP de SQL Server para inspeccionar la tabla dbo.NombreTabla.
Dime sus columnas, tipos, primary key, foreign keys y relaciones.
Después genera el modelo SQLAlchemy correspondiente respetando nombres reales.
```

### Git

Usar control de versiones.

Comandos básicos:

```bash
git status
git add .
git commit -m "Add auth module"
git push
```

## Organización sugerida del proyecto

```text
backend_app_pneumonia/
  app/
    main.py
    core/
      config.py
      database.py
      security.py
      dependencies.py
    modules/
      auth/
      patients/
      evaluations/
      predictions/
      images/
      recommendations/
      dashboard/
      reports/
  models/
    ml/
    dl/
  uploads/
    xrays/
  .env
  .gitignore
  requirements.txt
```

## `.gitignore` recomendado

```text
env/
venv/
__pycache__/
*.pyc
.env
uploads/
*.pkl
*.h5
*.keras
*.joblib
```

Si los modelos son grandes, no subirlos directamente a Git. Guardarlos en almacenamiento externo o usar Git LFS si es necesario.

## Frontend futuro

Opciones compatibles:

- Next.js.
- React.
- Angular.

Módulos visuales sugeridos:

- Login.
- Dashboard.
- Pacientes.
- Evaluaciones.
- Carga de radiografía.
- Resultado de predicción.
- Historial.
- Reportes.
- Administración.

## Pruebas mínimas

Antes de avanzar a otro módulo, probar:

- Endpoint responde en Swagger.
- Valida datos inválidos.
- Protege rutas por token.
- Protege rutas por rol.
- Guarda datos correctamente.
- No expone contraseñas.
- Maneja errores comunes.

## Comandos útiles

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Levantar servidor:

```bash
uvicorn app.main:app --reload
```

Ver paquetes instalados:

```bash
pip freeze
```

Ver versión de un paquete:

```bash
pip show bcrypt
```
