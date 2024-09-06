from .migrations import Migration

migrate = Migration()
migrate.run()

DB_CONNECTION = migrate.db_connection
DB_CURSOR = migrate.db_cursor


