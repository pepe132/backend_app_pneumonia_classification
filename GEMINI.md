# Neumonia Platform Backend - Instructions

## Project Overview
This project is a clinical support backend for the severity classification of pediatric pneumonia using Machine Learning (tabular data) and Deep Learning (X-ray images). It is built with **FastAPI** and uses **SQL Server** as the primary database.

### Key Technologies
- **Language:** Python 3.x
- **Framework:** FastAPI
- **ORM:** SQLAlchemy (using `pymssql`)
- **Database:** SQL Server
- **Authentication:** JWT (JSON Web Tokens) with `passlib` (bcrypt)
- **Validation:** Pydantic
- **AI Models:** XGBoost/LightGBM (Tabular), CNN/MobileNetV2 (Images) - *Pending full integration*

## Architecture & Structure
The project follows a modular Clean Code architecture.

```text
app/
├── core/             # Centralized configurations and utilities
│   ├── config.py     # Environment variables and settings
│   ├── database.py   # SQLAlchemy engine and session management
│   ├── security.py   # Auth logic (hashing, JWT)
│   └── dependencies.py # Shared FastAPI dependencies (auth guards)
└── modules/          # Feature-based modules
    ├── auth/         # Login, registration, and user management
    ├── patients/     # Patient registration and records
    ├── evaluations/  # Clinical evaluation forms and results
    ├── predictions/  # ML/DL model inference logic
    ├── images/       # X-ray image management
    └── ...
```

### Module Components
Each module typically contains:
- `models.py`: SQLAlchemy database models.
- `schema.py`: Pydantic schemas for request/response validation.
- `service.py`: Business logic and database interactions.
- `router.py`: FastAPI endpoints and route handlers.

## Building and Running

### Prerequisites
- Python 3.10+
- SQL Server instance (local or remote)
- `.env` file with required variables

### Setup
1. **Environment Variables:** Create a `.env` file in the root directory.
   ```env
   APP_NAME="Neumonia Platform"
   APP_VERSION="1.0.0"
   DB_SERVER="localhost"
   DB_PORT="1433"
   DB_NAME="Prueba"
   DB_USER="sa"
   DB_PASSWORD="your_password"
   SECRET_KEY="your-secret-key"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
2. **Install Dependencies:** (TODO: Create requirements.txt)
   ```bash
   pip install fastapi uvicorn sqlalchemy pymssql python-dotenv pydantic[email] passlib[bcrypt] python-jose[cryptography]
   ```

### Execution
Run the development server:
```bash
uvicorn app.main:app --reload
```
Access the documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development Conventions

### Coding Standards
- **Naming:** Use `snake_case` for functions, variables, and files. Use `PascalCase` for classes (Models, Schemas).
- **Language:** Code (variables, functions, classes) should be in **English**. Messages, documentation, and user-facing strings should be in **Spanish**.
- **Surgical Changes:** Maintain existing architecture patterns. Do not mix logic across layers (e.g., no database queries in routers).

### Database Rules
- Use SQLAlchemy ORM for all standard operations.
- All models must inherit from `Base` in `app.core.database`.
- Tables should specify the schema if necessary (e.g., `dbo`).

### Authentication & Authorization
- Use `get_current_user` dependency for protected routes.
- Roles: `1 = Admin`, `2 = Specialist/Doctor`, `3 = Read-only`.
- Use `require_roles([role_id])` for fine-grained access control.

## Project Documents
Refer to the `docs/` directory for detailed information:
- `arquitectura_clean_code_backend_v2.md`: Detailed architecture rules.
- `guia_desarrollo_app_neumonia_v2.md`: Step-by-step development guide.
- `contexto_app_neumonia_pediatrica_v2.md`: Business context and goals.
