
import configparser
import mysql.connector
import os
import uuid
import re

def load_db_config(path):

    """
    Loads MySQL database configuration from a config.ini file, substituting environment 
    variables for sensitive credentials.

    Parameters
    ----------
    path : str
        Path to the configuration file; defaults to "config.ini."

    Returns
    -------
    dict
        A dictionary containing rersolved database connection parameters
        (host, user, password, database).

    Raises
    ------
    EnvironmentError
        If required environment variables MySQL_DB_USER or MySQL_DB_PASS
        are not set.
    
    """

    config = configparser.ConfigParser()

    config.read(path)

    if "value" not in config:
        raise EnvironmentError("Section 'value' not found in config file.")
    
    db_cfg = config["value"]

    # Replace environment variable placeholders manually.

    host = db_cfg.get("host")

    user = db_cfg.get("user")

    password = db_cfg.get("password")

    database = db_cfg.get("database")

    if not user or not password:
        raise EnvironmentError("Environment variables are not set.")
    
    resolved_config = {
        "host": host,
        "user": user,
        "password": password,
        "database": database
    }

    return resolved_config

class Database:

    """
    A class for interfacing with the value measurement MySQL database.

    Attributes
    ----------
    conn : mysql.connector.connection.MySQLConnection
        Connection object to the MySQL database.

    cursor : mysql.connector.cursor.MySQLCursorDict
        Cursor object to execute SQL queries.
    
    Methods
    -------
    insert(table, data):
        Inserts a new record into the specified table.

    fetch_all(table):
        Fetches all records from the specified table.

    update(table, data, conditions):
        Updates records in the specified table based on given conditions.

    delete(table, conditions):
        Deletes records from the specified table based on given conditions.

    call_procedure(procedure_name, params=()):
        Calls a stored procedure with optional parameters.

    validate_query(query_str):
        Validates a user-input SQL to ensure it is a safe SELECT statement.

    execute_query(query_str):
        Executes a pre-defined or user-input SQL query after validation.

    close():
        Closes the database connection.

    """

    def __init__(self):
        
        """
        Initializes the database connection using the config.ini file.

        Raises
        ------
        Exception
            If the database connection fails.

        """

        config_file_path = "G:/My Drive/Projects/value/interface/config.ini"

        db_config = load_db_config(config_file_path)

        try:
            self.conn = mysql.connector.connect(
                host = db_config["host"],
                user = db_config["user"],
                password = db_config["password"],
                database = db_config["database"]
            )

            self.cursor = self.conn.cursor(dictionary = True)

        except mysql.connector.Error as e:
            raise Exception(f"Database connection attempt failed: {e}")
            return []
        
    def get_columns(self, table):

        """
        Retrieves the column names of a given table.

        Parameters
        ----------
        table : str
            The name of the table.

        Returns
        -------
        list
            A list of column names.

        Raises
        ------
        Exception
            If an error occurs while calling the stored procedure.
        
        """

        sql = f"SHOW COLUMNS FROM {table}"

        try:
            self.cursor.execute(sql)
            return [row["Field"] for row in self.cursor.fetchall()]
        except mysql.connector.Error as e:
            raise Exception(f"value_db: get_columns: error: {e}")
            return []

    def insert(self, table, data):

        """
        Inserts a new record into the specified table, excluding auto-generated primary key.

        Parameters
        ----------
        table : str
            The table name where data should be inserted.

        data : dict
            A dictionary containing column names as keys and corresponding values.

        Raises
        ------
        Exception
            If an error occurs while calling the stored procedure.
        
        """

        composite_keys = {"event_plan": ["event_id", "plan_id"]}

        primary_keys = composite_keys.get(table, [self.get_columns(table)[0]])

        for key in primary_keys:
            if key not in data or not data[key]:
                data[key] = str(uuid.uuid4())[:8]  # Generate a short unique id.

        columns = ", ".join(data.keys())

        placeholders = ", ".join(["%s"] * len(data))

        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()
        except mysql.connector.Error as e:
            raise Exception(f"value_db: insert: error: {e}")
        
    def fetch_all(self, table):

        """
        Fetches all records from the specified table.

        Parameters
        ----------
        table : str
            The table name to fetch data from.

        Returns
        -------
        list
            A list of dictionaries representing the rows.

        Raises
        ------
        Exception
            If an error occurs during the fetch.
        
        """

        sql = f"SELECT * FROM {table}"

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            raise Exception(f"Error on attempted fetch from {table}: {e}")
            return[]
        
    def update(self, table, data, conditions):

        """
        Updates records in the specified table based on given conditions.

        Parameters
        ----------
        table : str
            The table name where the update should occur.

        data : dict
            A dictionary of column names and values to update.

        conditions : dict
            A dictionary of column names and values to specify which rows to update.

        Raises
        ------
        Exception
            If an error occurs while calling the stored procedure.
        
        """

        composite_keys = {"event_plan": ["event_id", "plan_id"]}

        primary_keys = composite_keys.get(table, [self.get_columns(table)[0]])
        
        updates = ", ".join([f"{col} = %s" for col in data.keys() if col not in primary_keys])

        condition_str = " AND ".join([f"{col} = %s" for col in primary_keys])
        
        if not updates:
            raise Exception(f"Database Insert Error: {e}")
            return
        
        sql = f"UPDATE {table} SET {updates} WHERE {condition_str}"
        
        try:
            values = tuple(data[col] for col in data.keys() if col not in primary_keys) + tuple(conditions[col] for col in primary_keys)
            self.cursor.execute(sql, values)
            self.conn.commit()
        except mysql.connector.Error as e:
            raise Exception(f"value_db: update: error: {e}")
        
    def delete(self, table, conditions):

        """
        Deletes records from the specified table based on given conditions.

        Parameters
        ----------
        table : str
            The table name where deletion should occur.

        conditions : dict
            A dictionary of column names and values specifying which rows to delete.

        Raises
        ------
        Exception
            If an error occurs while calling the stored procedure.
        
        """

        condition_str = " AND ".join([f"{col} = %s" for col in conditions.keys()])

        sql = f"DELETE FROM {table} WHERE {condition_str}"

        try:
            self.cursor.execute(sql, tuple(conditions.values()))
            self.conn.commit()
        except mysql.connector.Error as e:
            raise Exception(f"value_db: delete: error: {e}")
        
    def call_procedure(self, procedure_name, params = ()):

        """
        Calls a stored procedure with optional parameters.

        Parameters
        ----------
        procedure_name : str
            The name of the stored procedure to call.

        params : tuple, optional
            The paramaters to pass to the stored procedures (default is an empty tuple).

        Returns
        -------
        list
            A list of dictionaries representing the procedure's output.

        Raises
        ------
        Exception
            If an error occurs while calling the stored procedure.
        
        """

        try:
            self.cursor.callproc(procedure_name, params)
            return []
        except mysql.connector.Error as e:
            raise Exception(f"Error calling procedure {procedure_name}: {e}")
            return []
        
    def validate_query(self, query_str):

        """
        Validates a user-input SQL to ensure it is a safe statement.

        Parameters
        ----------
        query_str : str
            The query string to be validated.

        bool
            True if the query is safe, False otherwise.

        Raises
        ------
        TypeError
            If the input is not a string.

        ValueError
            If the query is empty.

        Exception
            If an error occurs while calling the stored procedure.
        
        """

        if not isinstance(query_str, str):
            raise TypeError("Query must be a string.")
        
        query_str = query_str.strip().lower()
        
        if not query_str:
            raise ValueError("Query cannot be empty.")

        forbidden = ["drop", "delete", "alter", "truncate"]

        # Use regex to match forbidden words as whole words.

        pattern = r'\b(' + '|'.join(forbidden) + r')\b'
        
        if re.search(pattern, query_str):
            raise ValueError("Query contains forbidden SQL keywords.")

        return True
    
    def execute_query(self, query_str):

        """
        Executes a predifined or user-input SQL query after validation.

        Parameters
        ----------
        query_str : str
            String representing the query to be executed.

        Returns
        -------
        list
            A list of dictionaries representing the rows.

        Raises
        ------
        Exception
            If an error occurs while calling the stored procedure.
        
        """

        if not self.validate_query(query_str):
            raise Exception(f"invalid or unsafe query.")
        
        try: 
            self.cursor.execute(query_str)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            raise Exception(f"Error executing query: {e}")
            return []
        
    def close(self):

        """
        Closes the database connection.
        
        """

        self.cursor.close()
        self.conn.close()
    