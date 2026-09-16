from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.config import get_settings
from app.database.models import Base
config=context.config; config.set_main_option("sqlalchemy.url",get_settings().database_url)
if config.config_file_name: fileConfig(config.config_file_name)
target_metadata=Base.metadata
def do_run_migrations(connection:Connection):
    context.configure(connection=connection,target_metadata=target_metadata,compare_type=True);
    with context.begin_transaction(): context.run_migrations()
async def run_async_migrations():
    engine=async_engine_from_config(config.get_section(config.config_ini_section),prefix="sqlalchemy.",poolclass=pool.NullPool)
    async with engine.connect() as connection: await connection.run_sync(do_run_migrations)
    await engine.dispose()
def run_migrations_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"),target_metadata=target_metadata,literal_binds=True,dialect_opts={"paramstyle":"named"})
    with context.begin_transaction(): context.run_migrations()
if context.is_offline_mode(): run_migrations_offline()
else:
    import asyncio; asyncio.run(run_async_migrations())
