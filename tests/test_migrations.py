from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

from app.core.database import engine


def test_database_revision_matches_alembic_head():
    config = Config("alembic.ini")
    scripts = ScriptDirectory.from_config(config)

    with engine.connect() as connection:
        context = MigrationContext.configure(
            connection,
            opts={"version_table_schema": "dbo"},
        )

        assert context.get_current_revision() == scripts.get_current_head()
