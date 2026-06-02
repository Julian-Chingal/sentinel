import os
import shutil
from utils.logger import logger
from utils.connection import db_manager
from config.config import Config

class FileProcessor:
    def __init__(self):
        # Ensure directories exist
        os.makedirs(Config.DIR_PROCESADO, exist_ok=True)
        os.makedirs(Config.DIR_ERRORES, exist_ok=True)

    def process(self, filepath):
        """
        Main logic for processing a file.
        Reads the text file, interacts with the database, and moves the file.
        """
        filename = os.path.basename(filepath)
        logger.info(f"Starting to process file: {filename}")

        try:
            # 1. Read the file as plain text
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                logger.debug(f"File {filename} read successfully. Size: {len(content)} characters.")

            # 2. Extract information (stub)
            # Example: extract a code or ID from the content or filename
            extracted_param = self._extract_data(content, filename)

            # 3. Query DB tables
            # Call the stubbed query methods
            table1_result = db_manager.query_table_1(extracted_param)
            table2_result = db_manager.query_table_2(extracted_param)

            # 4. Prepare data for insertion
            insert_data = {
                'valor1': f"Data from {filename}",
                'valor2': extracted_param
            }

            # 5. Insert the record into the third table
            insert_success = db_manager.insert_record(insert_data)

            # 6. Move the file depending on success
            if insert_success:
                self._move_file(filepath, Config.DIR_PROCESADO)
                logger.info(f"File {filename} processed and moved to {Config.DIR_PROCESADO}")
            else:
                self._move_file(filepath, Config.DIR_ERRORES)
                logger.error(f"Failed to process/insert data for {filename}. Moved to {Config.DIR_ERRORES}")

        except Exception as e:
            logger.error(f"Error processing file {filename}: {e}")
            self._move_file(filepath, Config.DIR_ERRORES)

    def _extract_data(self, content, filename):
        """
        Stub to extract the necessary parameter for DB queries.
        The user can implement parsing logic here.
        """
        # Simply return the filename or part of it as an example
        return filename

    def _move_file(self, src_path, dest_dir):
        """Moves a file to the destination directory, handling overwrites if needed."""
        if not os.path.exists(src_path):
            return

        filename = os.path.basename(src_path)
        dest_path = os.path.join(dest_dir, filename)

        # Remove existing file in destination to avoid shutil.move errors
        if os.path.exists(dest_path):
            os.remove(dest_path)

        try:
            shutil.move(src_path, dest_path)
        except Exception as e:
            logger.error(f"Error moving file {filename} to {dest_dir}: {e}")

file_processor = FileProcessor()
