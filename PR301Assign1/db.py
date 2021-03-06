import sqlite3
from abc import abstractmethod, ABCMeta


class Subject(metaclass=ABCMeta):
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)
        observer.set_subject(self)
        observer.update()

    def detach(self, observer):
        self.observers.remove(observer)
        observer.set_subject(None)

    def notify(self):
        for observer in self.observers:
            observer.update()

    @abstractmethod
    def get_state(self):
        pass


class DatabaseHandler(Subject):
    def __init__(self, new_validator, database):
        Subject.__init__(self)
        self.validator = new_validator
        self.database = database

        try:
            self._connection = sqlite3.connect(database + ".db")
            self._cursor = self._connection.cursor()
            self.close_db()
        except Exception as e:
            print(e)

    def load(self):
        try:
            self.destroy_db()
            self.build_db()
        except Exception as e:
            print(e)
        else:
            print("Opened database successfully")
        finally:
            print("Finishing connecting to database")
            self.notify()

    def open_db(self):
        try:
            self._connection = sqlite3.connect(self.database + ".db")
            self._cursor = self._connection.cursor()
        except Exception as e:
            print(e)

    def destroy_db(self):
        self.open_db()
        self._cursor.execute("""DROP TABLE IF EXISTS employee;""")
        self.close_db()

    def build_db(self):
        self.open_db()
        sql_command = """
        CREATE TABLE employee (
        empid VARCHAR(20) PRIMARY KEY,
        gender CHAR(1),
        age INTEGER,
        sales INTEGER,
        bmi VARCHAR(20),
        salary INTEGER,
        birthday DATE);"""
        try:
            self._cursor.execute(sql_command)
        except Exception as e:
            print(e)
        else:
            self._connection.commit()
        self.close_db()

    def close_db(self):
        self._connection.close()

    def insert(self, employees):
        self.open_db()
        for employee in employees:
            format_str = """INSERT INTO employee (empid, gender, age, sales, bmi, salary, birthday)
                VALUES ("{empid}", "{gender}", "{age}", "{sales}", "{bmi}", "{salary}", "{birthday}");"""
            sql_command = format_str.format(
                empid=employee["EMPID"],
                gender=employee["GENDER"],
                age=employee["AGE"],
                sales=employee["SALES"],
                bmi=employee["BMI"],
                salary=employee["SALARY"],
                birthday=employee["BIRTHDAY"])
            try:
                self._cursor.execute(sql_command)
            except Exception as e:
                print(e)
            else:
                print("Successfully added employee {0} to database".format(employee["EMPID"]))
                self._connection.commit()
        self.close_db()
        self.notify()

    #Rosemary
    def query(self, emp_id):
        self.open_db()
        sql_result = self._cursor.execute('SELECT * FROM employee WHERE empid = "{empid}"'.format(empid=emp_id))
        employee = sql_result.fetchone()
        if employee:
            print(employee)
        else:
            print("No such employee found")
        self.close_db()

    def get_data(self, field):
        self.open_db()
        if not self.validator.check_in_attributes(field):
            return False
        else:
            sql_result = self._cursor.execute('SELECT EMPID, {field} FROM employee'.format(field=field))
            employees = sql_result.fetchall()
            self.close_db()
            return employees

    def get_state(self):
        self.open_db()
        sql_result = self._cursor.execute('SELECT * FROM employee')
        results = sql_result.fetchall()
        self.close_db()
        employees = []
        for data in results:
            employee = dict()
            employee["EMPID"] = data[0]
            employee["GENDER"] = data[1]
            employee["AGE"] = data[2]
            employee["SALES"] = data[3]
            employee["BMI"] = data[4]
            employee["SALARY"] = data[5]
            employee["BIRTHDAY"] = data[6]
            employees.append(employee)
        return employees
