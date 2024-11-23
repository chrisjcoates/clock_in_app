import sqlite3
import os


class Database:
    def __init__(self):

        self.database_file = 'data/employees.db'
        self.conn = None
        self.cursor = None

    def connect_to_db(self):

        if not os.path.exists(self.database_file):
            try:
                conn = sqlite3.connect(self.database_file)
                cursor = conn.cursor()

                sql_query = """
                CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                location TEXT,
                clocked_in TEXT,
                timestamp TEXT
                )
                """
                cursor.execute(sql_query)
                conn.commit()

                cursor.close()
                conn.close()

                print('Sucessfully created and connected to database.')
            except Exception as e:
                print('Error connecting to database.', e)

        if os.path.exists(self.database_file):

            try:
                self.conn = sqlite3.connect(self.database_file)
                self.cursor = self.conn.cursor()

                print('Sucessfully connected to database.')

            except Exception as e:
                print('Error connecting to database.', e)

    def close_db_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

            print('Database connection closed.')
        except Exception as e:
            print('Error closing connectin to database.', e)

    def check_clocked_in(self, employee_id):

        self.connect_to_db()

        self.clocked_in = False

        sql_query = """
        SELECT clocked_in
        FROM employees
        WHERE id = ?
        """

        try:
            self.cursor.execute(sql_query, employee_id)
            field = self.cursor.fetchone()

            if field == 'True':
                self.clocked_in = True
        except Exception as e:
            print('Failed to query the database.', e)

        return self.clocked_in

    def clock_in(self, location, employee_id):
        if not self.check_clocked_in(employee_id):
            self.connect_to_db()

            sql_query = """
            UPDATE employees
            SET clocked_in = 'True',
                location = ?
            WHERE id = ?
            """

            try:
                self.cursor.execute(sql_query, (location, employee_id))
                self.conn.commit()

                print('Record updated sucessfully.')

                self.close_db_connection()
            except Exception as e:
                print('Error updating record.', e)


database = Database()

print(database.check_clocked_in('1'))
