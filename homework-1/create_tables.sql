-- SQL-команды для создания таблиц
CREATE TABLE employee
(
    employee_id int PRIMARY KEY,
	first_name varchar(100) NOT NULL,
	last_name varchar(100) NOT NULL,
    title varchar(100) NOT NULL,
	birth date,
    notes text
);

CREATE TABLE customer
(
    id SERIAL PRIMARY KEY,
    customer_id varchar(100) UNIQUE NOT NULL,
	company_name varchar(100) NOT NULL,
	contact_name varchar(100) NOT NULL
);

CREATE TABLE orders
(
    order_id int PRIMARY KEY,
	employee_id int NOT NULL REFERENCES employee(employee_id),
    customer_id varchar(100) NOT NULL REFERENCES customer(customer_id),
	order_date date,
	ship_city varchar(100) NOT NULL
);
