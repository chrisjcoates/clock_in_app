import sqlite3
import os
import datetime


class Database:
    def __init__(self):

        self.database_file = "data/employees.db"
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
                department TEXT NOT NULL,
                shift_start TEXT NOT NULL,
                shift_end TEXT NOT NULL,
                clocked_in TEXT,
                timestamp TEXT
                )
                """
                cursor.execute(sql_query)
                conn.commit()

                cursor.close()
                conn.close()

                print("Sucessfully created and connected to database.")
            except Exception as e:
                print("Error connecting to database.", e)

        if os.path.exists(self.database_file):

            try:
                self.conn = sqlite3.connect(self.database_file)
                self.cursor = self.conn.cursor()

                print("Sucessfully connected to database.")

            except Exception as e:
                print("Error connecting to database.", e)

    def close_db_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

            print("Database connection closed.")
        except Exception as e:
            print("Error closing connectin to database.", e)

    def get_all_records(self, filter=None):

        self.connect_to_db()

        if filter == "all":
            sql_query = """
            SELECT * FROM employees
            """
        elif filter == "clocked in":
            sql_query = """
            SELECT * FROM employees
            WHERE clocked_in = 'True'
            """
        else:
            sql_query = """
            SELECT * FROM employees
            WHERE clocked_in = 'False'
            """

        self.cursor.execute(sql_query)

        data = self.cursor.fetchall()

        self.close_db_connection()

        return data

    def check_clocked_in(self, employee_id):

        self.connect_to_db()

        sql_query = """
        SELECT clocked_in
        FROM employees
        WHERE id = ?
        """

        try:
            self.cursor.execute(sql_query, (employee_id,))
            field = self.cursor.fetchone()

            if field[0] == "True":
                clocked_in = True
                print("Employee is clocked in.")
            else:
                clocked_in = False
        except Exception as e:
            print("Failed to query the database.", e)

        return clocked_in

    def clock_in(self, location, employee_id):
        if not self.check_clocked_in(employee_id):
            self.connect_to_db()

            time_str = str(datetime.datetime.now().replace(microsecond=0))

            sql_query = f"""
            UPDATE employees
            SET clocked_in = 'True',
                location = ?,
                timestamp = '{time_str:00}'
            WHERE id = ?
            """

            try:
                self.cursor.execute(sql_query, (location, employee_id))
                self.conn.commit()

                print("Record updated sucessfully, employee clocked in.")

                self.close_db_connection()
            except Exception as e:
                print("Error updating record.", e)

    def clock_out(self, employee_id):
        if self.check_clocked_in(employee_id):
            self.connect_to_db()

            sql_query = """
            UPDATE employees
            SET clocked_in = 'False',
                location = '',
                timestamp = ''
            WHERE id = ?
            """

            try:
                self.cursor.execute(sql_query, (employee_id,))
                self.conn.commit()

                print("Record updated sucessfully, employee clocked out.")

                self.close_db_connection()
            except Exception as e:
                print("Error updating record.", e)

    def count_employess_on_site(self):

        employees_onsite = {"Mill Bank": 0, "Moss Fold": 0}

        self.connect_to_db()

        sql_query = """
        SELECT * FROM employees
        """

        try:
            self.cursor.execute(sql_query)
            data = self.cursor.fetchall()

            self.close_db_connection()

            for row in data:
                if row[3] == "Mill Bank":
                    employees_onsite["Mill Bank"] += 1
                elif row[3] == "Moss Fold":
                    employees_onsite["Moss Fold"] += 1
                else:
                    pass
        except Exception as e:
            print("Error counting employees on site.", e)

        return employees_onsite

    def create_employee(self, f_name, l_name, dept, s_start, s_end):

        self.connect_to_db()

        sql_query = """
        INSERT INTO employees (first_name, last_name, department, shift_start, shift_end, location, timestamp, clocked_in)
        VALUES (?, ?, ?, ?, ?, '', '', 'False')
        """
        try:
            self.cursor.execute(
                sql_query, (f_name, l_name, dept, s_start, s_end))
            self.conn.commit()
        except Exception as e:
            print("Error inserting employee into table.", e)

        self.close_db_connection()

    def employee_details(self, employee_id):

        self.connect_to_db()

        sql_query = """
        SELECT *
        FROM employees
        WHERE id = ?
        """
        try:
            self.cursor.execute(sql_query, (employee_id,))
            employee = self.cursor.fetchone()
        except Exception as e:
            print("Failed to get employee details from db.", e)

        details = None

        try:
            if len(employee) > 0:

                details = {
                    "ID": str(employee[0]),
                    "Name": employee[1] + " " + employee[2],
                    "Location": employee[3],
                    "Clocked_in": employee[7],
                }
                print("Sucessfully retrieved employee details from db.")
        except Exception as e:
            print(e)

        self.close_db_connection()

        if not details:
            print("No employee found with ID, employee details value is 'None'.")

        return details
