from logging.config import fileConfig

from alembic import context

from app.core.database import Base, DATABASE_URL
from app.modules.auth import models as auth_models  # noqa: F401
from app.modules.evaluations import models as evaluation_models  # noqa: F401
from app.modules.patients import models as patient_models  # noqa: F401
from app.modules.radiographs import models as radiograph_models  # noqa: F401


config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL.replace("%", "%%"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
APP_TABLES = {
    "Roles",
    "Users",
    "Patients",
    "Evaluations",
    "Radiographs",
    "alembic_version",
}


def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name in {None, "dbo"}
    if type_ == "table":
        return name in APP_TABLES
    return True


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        compare_type=True,
        version_table_schema="dbo",
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    from app.core.database import engine

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
            compare_type=True,
            version_table_schema="dbo",
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
