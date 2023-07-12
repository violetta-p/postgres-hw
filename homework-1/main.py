import psycopg2
import os
import csv
from abc import ABC, abstractmethod

conn_password: str = os.getenv('POSTGRES_PW')

conn = psycopg2.connect(
    host="localhost",
    database="north",
    user="postgres",
    password=conn_password
)

curs = conn.cursor()


class Writer(ABC):
    @abstractmethod
    def write_data(self):
        pass


class OpenCSV:
    def __init__(self, dir_name, file_name):
        self.full_path_to_data = os.path.join(os.path.abspath("."), dir_name, file_name)

    def get_data_from_csv(self):
        all_data = []
        with open(self.full_path_to_data, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                all_data.append(row)
            return all_data


class Employees(OpenCSV, Writer):

    def __init__(self, dir_name, file_name):
        super().__init__(dir_name, file_name)

    def write_data(self) -> None:
        employees_data = self.get_data_from_csv()
        for item in employees_data:
            all_data = (
                item["employee_id"], item["first_name"],
                item["last_name"], item["title"],
                item["birth_date"], item["notes"],
            )

            curs.execute("INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s)", all_data)
            conn.commit()


class Customers(OpenCSV, Writer):

    def __init__(self, dir_name, file_name):
        super().__init__(dir_name, file_name)

    def write_data(self) -> None:
        customers_data = self.get_data_from_csv()
        for item in customers_data:
            all_data = (
                item["customer_id"],
                item["company_name"],
                item["contact_name"],
            )

            curs.execute(f"INSERT INTO customer VALUES (DEFAULT,%s, %s, %s)", all_data)
            conn.commit()


class Orders(OpenCSV, Writer):
    EMPLOYEES_DATA_FILE = "employees_data.csv"

    def __init__(self, dir_name, file_name):
        super().__init__(dir_name, file_name)

    def write_data(self):
        orders_data = self.get_data_from_csv()
        for item in orders_data:
            all_data = (
                item["order_id"], item["employee_id"],
                item["customer_id"], item["order_date"],
                item["ship_city"],
            )

            curs.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s)", all_data)
            conn.commit()


if __name__ == "__main__":

    DIR_NAME = "north_data"
    EMPLOYEES_DATA_FILE = "employees_data.csv"
    CUSTOMERS_DATA_FILE = "customers_data.csv"
    ORDERS_DATA_FILE = "orders_data.csv"

    OpenCSV(DIR_NAME, EMPLOYEES_DATA_FILE)
    emp = Employees(DIR_NAME, EMPLOYEES_DATA_FILE)
    emp.write_data()

    OpenCSV(DIR_NAME, EMPLOYEES_DATA_FILE)
    cust = Customers(DIR_NAME, CUSTOMERS_DATA_FILE)
    cust.write_data()

    OpenCSV(DIR_NAME, ORDERS_DATA_FILE)
    order = Orders(DIR_NAME, ORDERS_DATA_FILE)
    order.write_data()
