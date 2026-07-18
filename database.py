import sqlite3
import re

class Database:

    def __init__(self, path):
        self.path = path
        self.conn = None

    def _check_identifier(self, name):
        pattern = r"[A-Za-z_][A-Za-z0-9_]*"

        if not re.fullmatch(pattern, name):
            raise ValueError(f"Invalid SQL identifier: {name}")
        
        return name
    
    def _execute(self, sql, params=()):
        if self.conn is None:
            raise RuntimeError("Database is not open")
        
        return self.conn.execute(sql, params)
    
    # Parameter binding sends values separately from the SQL statement.
    # Because the values are never parsed as SQL code, they cannot perform
    # SQL injection, even if they contain SQL keywords or special characters.

    def open(self):                     
        # Open the database connection

        self.conn = sqlite3.connect(self.path)

        #Allow rows to behave like dictionary
        self.conn.row_factory = sqlite3.Row

        #Enable foriegn key support
        self.conn.execute("PRAGMA foreign_keys = ON")

        print("Database opened successfully")

    def close(self):             
        # Close the database connection

        self.conn.commit()       # Save all pending changes

        self.conn.close()

        self.conn = None         # Remove the connection object

        print("Database closed successfully")

    def __enter__(self):        
        # Automatically called when entering a 'with' block
        self.open()

        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        # Automatically called when leaving a 'with' block
        
        if self.conn is not None:

            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()

            self.conn.close()

            self.conn = None
            print("Database connection closed.")

    # Always close the database connection when you're done.
    # Otherwise, uncommitted changes may be lost and the database file
    # may remain locked, preventing other programs or users from writing to it.

    def create_table(self, name, columns):
        self._check_identifier(name)

        column_list = []

        for column_name, column_type in columns.items():
            self._check_identifier(column_name)
            column_list.append(f'"{column_name}" {column_type}')

        column_sql = ", ".join(column_list)

        sql = f'CREATE TABLE IF NOT EXISTS "{name}" ({column_sql})'

        print(sql)
        self._execute(sql)

        self.conn.commit()

        print(f"Table '{name}' created successfully")

    # IF NOT EXISTS prevents an error if the table already exists.
    # This makes create_table() idempotent (safe to call multiple times).

    def update_table(self, name, add_column=None, rename_to=None):
        self._check_identifier(name)

        if add_column is not None:
            column_name, column_type = add_column

            self._check_identifier(column_name)

            sql = f'ALTER TABLE "{name}" ADD COLUMN "{column_name}" {column_type}'

            self._execute(sql)

            self.conn.commit()

            print(f"Column '{column_name}' added successfully")

        if rename_to is not None:
            self._check_identifier(rename_to)

            sql = f'ALTER TABLE "{name}" RENAME TO "{rename_to}"'

            self._execute(sql)

            print(f"Table renamed to '{rename_to}'")

        self.conn.commit()

    def delete_table(self, name):
        self._check_identifier(name)

        sql = f'DROP TABLE IF EXISTS "{name}"'

        self._execute(sql)

        self.conn.commit()

        print(f"Table '{name}' deleted successfully.")

    def list_tables(self):

        sql = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """

        cursor = self._execute(sql)
        return [row["name"] for row in cursor.fetchall()]
    
    def write(self, table, row):
        self._check_identifier(table)

        #Check all column names
        for column in row.keys():
            self._check_identifier(column)

        #Create column names
        columns = ", ".join(f' "{col}"' for col in row.keys())

        #Create ? placeholders
        placeholders = ", ".join("?" for _ in row)

        #Build SQL Query
        sql = f' INSERT INTO "{table}" ({columns}) VALUES ({placeholders})'

        #Execute SQL Query
        cursor = self._execute(sql, tuple(row.values()))

        self.conn.commit()

        #Return the id of the inserted row
        return cursor.lastrowid
    
    # Use ? placeholders for values instead of inserting them into the SQL string.
    # SQLite binds the values safely, preventing SQL injection and handling
    # quoting/escaping automatically.
    
    def read(self, table, where=None, params=()):
        self._check_identifier(table)

        #Basic SQL Query
        sql = f'SELECT * FROM "{table}"'

        #Add where condition if provided
        if where:
            sql += f" WHERE {where}"

        #Execute SQL Query
        cursor = self._execute(sql, params)

        return[dict(row) for row in cursor.fetchall()]
    
    def update(self, table, changes, where=None, params=()):
        # Update rows in a table

        self._check_identifier(table)

        #Validate column names
        for column in changes.keys():
            self._check_identifier(column)

        #Create SET clause
        set_clause = ", ".join(f'"{column}" = ?' for column in changes.keys())

        #Build SQL Query
        sql = f'UPDATE "{table}" SET {set_clause}'

        #Add WHERE condition if provided
        if where:
            sql += f" WHERE {where}"

        #Combine parameters
        all_params = tuple(changes.values()) + tuple(params)

        #Execute SQL Query
        cursor = self._execute(sql, all_params)

        self.conn.commit()

        return cursor.rowcount
    
    # Note:
    # update() modifies table data (DML), while 
    # update_table() modifies the table structure (DDL).

    def delete(self, table, where=None, params=()):
        # Delete rows from a table

        self._check_identifier(table)

        sql = f'DELETE FROM "{table}"'

        if where:
            sql += f" WHERE {where}"

        cursor = self._execute(sql, params)

        self.conn.commit()

        return cursor.rowcount

   # WARNING:
   # DELETE without a WHERE clause deletes all rows.
   # Always use a WHERE clause unless you intentionally want to empty the table.
   # This is the same safety rule as UPDATE, where omitting WHERE affects every row.




    
