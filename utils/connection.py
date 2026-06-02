import mysql.connector
from mysql.connector import Error
from config.config import Config
from utils.logger import logger

class DatabaseManager:
    def __init__(self):
        self.host = Config.DB_HOST
        self.port = Config.DB_PORT
        self.database = Config.DB_NAME
        self.user = Config.DB_USER
        self.password = Config.DB_PASSWORD

    def get_connection(self):
        """Returns a new database connection."""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if connection.is_connected():
                return connection
        except Error as e:
            logger.error(f"Error connecting to MySQL database: {e}")
            return None

    def query_table_1(self, parameter):
        """
        Stub to query the first table.
        The user should complete the logic/schema here.
        """
        query = "SELECT * FROM tabla_1 WHERE columna = %s"
        logger.debug(f"Executing query_table_1 with parameter: {parameter}")
        connection = self.get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (parameter,))
            result = cursor.fetchall()
            return result
        except Error as e:
            logger.error(f"Error querying table 1: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def query_table_2(self, parameter):
        """
        Stub to query the second table.
        The user should complete the logic/schema here.
        """
        query = "SELECT * FROM tabla_2 WHERE columna = %s"
        logger.debug(f"Executing query_table_2 with parameter: {parameter}")
        connection = self.get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (parameter,))
            result = cursor.fetchall()
            return result
        except Error as e:
            logger.error(f"Error querying table 2: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def insert_record(self, data):
        """
        Stub to insert into the specific registration table.
        The user should complete the mapping/schema here.
        """
        query = "INSERT INTO tabla_registro (columna1, columna2) VALUES (%s, %s)"
        logger.debug(f"Executing insert_record with data: {data}")
        connection = self.get_connection()
        if not connection:
            return False

        try:
            cursor = connection.cursor()
            # The user should adjust this tuple according to their mapping
            cursor.execute(query, (data.get('valor1'), data.get('valor2')))
            connection.commit()
            logger.info("Record inserted successfully")
            return True
        except Error as e:
            logger.error(f"Error inserting record: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

db_manager = DatabaseManager()
