import pytest
from sqlalchemy.exc import OperationalError
from unittest.mock import mock_open, patch

from app.core.db import create_db_and_tables, read_sql_file


def test_read_sql_file():
    """
    Test mocking of reading a sql file
    """
    sqline = """INSERT INTO "organisations" ( "id",  "name",  "business_id") VALUES ( 1,  'Lamb LLC',  '7861602-9');"""
    m = mock_open(read_data=sqline)
    with patch('builtins.open', m):
        content = read_sql_file("/fake/path/dump.sql")
        assert "Lamb LLC" in content


def test_create_db_and_tables_no_existing_db():
    """
    Test mocking of create_db_and_tables()
    """
    with patch('app.core.db.database_exists', return_value=False), \
         patch('app.core.db.create_database') as mock_create, \
         patch('app.core.db.Base.metadata.create_all') as mock_metadata:
        create_db_and_tables()
        assert mock_create.called
        assert mock_metadata.called


def test_create_db_and_tables_error_handling():
    """
    Test error handling of create_db_and_tables()
    """
    with patch('app.core.db.database_exists', return_value=False), \
         patch('app.core.db.Base.metadata.create_all', side_effect=OperationalError("db", "stmt", "params")):
        with pytest.raises(Exception):
            create_db_and_tables()
