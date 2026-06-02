import os
import pytest
from unittest.mock import patch, MagicMock
from sentinel.processor import FileProcessor
from config.config import Config

@pytest.fixture
def temp_dirs(tmpdir):
    # Use pytest's tmpdir to override configured directories during testing
    Config.DIR_WATCH = str(tmpdir.mkdir("watch"))
    Config.DIR_PROCESADO = str(tmpdir.mkdir("procesado"))
    Config.DIR_ERRORES = str(tmpdir.mkdir("errores"))
    return tmpdir

@patch("sentinel.processor.db_manager")
def test_processor_success(mock_db_manager, temp_dirs):
    # Setup mock returns
    mock_db_manager.query_table_1.return_value = [{"id": 1}]
    mock_db_manager.query_table_2.return_value = [{"info": "test"}]
    mock_db_manager.insert_record.return_value = True

    # Setup file
    processor = FileProcessor()
    test_file = os.path.join(Config.DIR_WATCH, "z12345.001")
    with open(test_file, "w") as f:
        f.write("test content")

    # Process
    processor.process(test_file)

    # Verify DB calls
    mock_db_manager.query_table_1.assert_called_once()
    mock_db_manager.query_table_2.assert_called_once()
    mock_db_manager.insert_record.assert_called_once()

    # Verify file moved to procesado
    procesado_file = os.path.join(Config.DIR_PROCESADO, "z12345.001")
    assert os.path.exists(procesado_file)
    assert not os.path.exists(test_file)

@patch("sentinel.processor.db_manager")
def test_processor_failure(mock_db_manager, temp_dirs):
    # Setup mock returns (Simulate a failure in insertion)
    mock_db_manager.insert_record.return_value = False

    # Setup file
    processor = FileProcessor()
    test_file = os.path.join(Config.DIR_WATCH, "z98765.002")
    with open(test_file, "w") as f:
        f.write("test content for failure")

    # Process
    processor.process(test_file)

    # Verify DB calls
    mock_db_manager.insert_record.assert_called_once()

    # Verify file moved to errores
    errores_file = os.path.join(Config.DIR_ERRORES, "z98765.002")
    assert os.path.exists(errores_file)
    assert not os.path.exists(test_file)

@patch("sentinel.processor.db_manager")
def test_processor_exception(mock_db_manager, temp_dirs):
    # Setup mock to raise exception
    mock_db_manager.query_table_1.side_effect = Exception("DB Connection Error")

    # Setup file
    processor = FileProcessor()
    test_file = os.path.join(Config.DIR_WATCH, "z00000.003")
    with open(test_file, "w") as f:
        f.write("bad content")

    # Process
    processor.process(test_file)

    # Verify file moved to errores due to exception
    errores_file = os.path.join(Config.DIR_ERRORES, "z00000.003")
    assert os.path.exists(errores_file)
