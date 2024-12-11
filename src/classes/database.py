import sqlite3
import os
import datetime


class Database:
    def __init__(self):

        # Set the db file location
        self.database_file = "data/employees.db"

        self.conn = None
        self.cursor = None

    def connect_to_db(self):
        """Connects to the database and sets the conn, and cursor objects"""
        # Check if the file exists
        if not os.path.exists(self.database_file):
            # If not create the db file and table
            try:
                conn = sqlite3.connect(self.database_file)
                cursor = conn.cursor()

                # SQL query to cerate a the database table
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

                # execute and commit
                cursor.execute(sql_query)
                conn.commit()

                # Close the connection
                cursor.close()
                conn.close()

                print("Sucessfully created and connected to database.")
            except Exception as e:
                print("Error connecting to database.", e)
        # If the file exists aptempt to connect to the db
        if os.path.exists(self.database_file):

            try:
                # set the connection and the cursor as variables
                self.conn = sqlite3.connect(self.database_file)
                self.cursor = self.conn.cursor()

                print("Sucessfully connected to database.")

            except Exception as e:
                print("Error connecting to database.", e)

    def close_db_connection(self):
        """Close the database connection"""
        # if the cursor and connection are live close them
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

            print("Database connection closed.")
        except Exception as e:
            print("Error closing connectin to database.", e)

    def get_all_records(self, filter=None):
        """Executes and sql query based on the the filter passes intot he method
        and returns the data"""
        # conencto to db
        self.connect_to_db()

        # set sql query based on function arg
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
        # execute the sql query
        self.cursor.execute(sql_query)
        # set the data retreived to the variable data
        data = self.cursor.fetchall()
        # close the bd conection
        self.close_db_connection()

        return data

    def check_clocked_in(self, employee_id):
        """Checks if an employee is already clocked in and returns a boolean value"""
        # Connect to db
        self.connect_to_db()

        sql_query = """
        SELECT clocked_in
        FROM employees
        WHERE id = ?
        """

        try:
            # try to execute the sql query passings the employee id as an arg
            self.cursor.execute(sql_query, (employee_id,))
            field = self.cursor.fetchone()
            # based on if the employee is clocked in or our set the value of clocked_in
            if field[0] == "True":
                clocked_in = True
                print("Employee is clocked in.")
            else:
                clocked_in = False
        except Exception as e:
            print("Failed to query the database.", e)

        return clocked_in

    def clock_in(self, location, employee_id):
        """Clocks the employee in, and updates the employee records clocked_in field in the database to True"""
        # check if the employee is not clocked in already
        if not self.check_clocked_in(employee_id):
            self.connect_to_db()
            # set current time for time stamp
            time_str = str(datetime.datetime.now().replace(microsecond=0))

            sql_query = f"""
            UPDATE employees
            SET clocked_in = 'True',
                location = ?,
                timestamp = '{time_str:00}'
            WHERE id = ?
            """

            try:
                # execute the query, passing the location and employee id as args
                self.cursor.execute(sql_query, (location, employee_id))
                self.conn.commit()

                print("Record updated sucessfully, employee clocked in.")

                self.close_db_connection()
            except Exception as e:
                print("Error updating record.", e)

    def clock_out(self, employee_id):
        """Clocks the employee out, and updates the employee records clocked_out field in the database to True"""
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
        """counts the employes clocked in at each location and returns a dictionary"""
        # create a dictionary of sites for employee count
        employees_onsite = {"Mill Bank": 0, "Moss Fold": 0}
        # connect to the database
        self.connect_to_db()

        sql_query = """
        SELECT * FROM employees
        """

        try:
            # execute the sql query
            self.cursor.execute(sql_query)
            # set the retreived information to the data variable
            data = self.cursor.fetchall()
            # clise the connection
            self.close_db_connection()

            # Loop thought the data and increase the employee count based on location
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
        """Connects to the database, takes employee details as args and inserts a new employee record 
        into the data"""
        # Connecto to db
        self.connect_to_db()

        sql_query = """
        INSERT INTO employees (first_name, last_name, department, shift_start, shift_end, location, timestamp, clocked_in)
        VALUES (?, ?, ?, ?, ?, '', '', 'False')
        """

        try:
            # Execute query, taking employee details as args
            self.cursor.execute(sql_query, (f_name, l_name, dept, s_start, s_end))
            # commit the insert
            self.conn.commit()
        except Exception as e:
            print("Error inserting employee into table.", e)
        # Close the database connection
        self.close_db_connection()

    def employee_details(self, employee_id):
        # connected to db
        self.connect_to_db()

        sql_query = """
        SELECT *
        FROM employees
        WHERE id = ?
        """
        try:
            # execute the sql statement, passing employee id
            self.cursor.execute(sql_query, (employee_id,))
            employee = self.cursor.fetchone()
        except Exception as e:
            print("Failed to get employee details from db.", e)

        details = None

        try:
            # if employee record found
            if len(employee) > 0:
                # create a dictionary for that employee
                details = {
                    "ID": str(employee[0]),
                    "Name": employee[1] + " " + employee[2],
                    "Location": employee[3],
                    "Clocked_in": employee[7],
                }
                print("Sucessfully retrieved employee details from db.")
        except Exception as e:
            print(e)
        # Close the db
        self.close_db_connection()

        if not details:
            print("No employee found with ID, employee details value is 'None'.")

        return details
