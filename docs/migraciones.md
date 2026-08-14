# Migraciones de base de datos

El esquema del backend se administra con Alembic sobre SQL Server. La revisión
base es `20260811_0001` y contiene las tablas `Roles`, `Users`, `Patients`,
`Evaluations` y `Radiographs`, además de los tres roles iniciales.

## Comandos habituales

Con el entorno virtual activo:

```powershell
python -m alembic current
python -m alembic upgrade head
python -m alembic downgrade -1
```

Para crear una revisión después de modificar los modelos:

```powershell
python -m alembic revision --autogenerate -m "descripcion_del_cambio"
```

La revisión generada debe revisarse manualmente antes de ejecutarla. SQL Server
puede reflejar el esquema `dbo`, índices y tipos de fecha de forma distinta a
SQLAlchemy; nunca se deben aceptar operaciones generadas sin comprobarlas.

## Base existente

Una base que ya contenía el esquema antes de adoptar Alembic se registra una
sola vez con:

```powershell
python -m alembic stamp 20260811_0001
```

`stamp` no crea tablas ni modifica registros. La base de pruebas actual ya fue
marcada con esta revisión el 11 de agosto de 2026.

## Base nueva

Después de crear una base vacía y configurar `DB_NAME`:

```powershell
python -m alembic upgrade head
```

Esto crea el esquema completo y carga los roles `ADMINISTRADOR`, `ESPECIALISTA`
y `LECTURA`.

## Scripts SQL anteriores

Los archivos `scripts/001_*.sql` a `scripts/004_*.sql` se conservan como
histórico de la etapa previa a Alembic. No deben ejecutarse junto con la
migración base sobre una base nueva.

## Reglas operativas

- Respaldar la base antes de migrar un entorno con datos reales.
- Ejecutar primero en desarrollo o staging.
- Revisar `current` antes y después de `upgrade head`.
- No usar `downgrade` en producción sin un plan de recuperación aprobado.
- No guardar credenciales en `alembic.ini`; Alembic usa las variables `.env`.
