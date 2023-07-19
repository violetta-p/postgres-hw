-- Напишите запросы, которые выводят следующую информацию:
-- 1. Название компании заказчика (company_name из табл. customers) и ФИО сотрудника, работающего над заказом этой компании (см таблицу employees),
-- когда и заказчик и сотрудник зарегистрированы в городе London, а доставку заказа ведет компания United Package (company_name в табл shippers)
SELECT customers.company_name, CONCAT(employees.first_name, ' ', employees.last_name) AS fullname
FROM orders
INNER JOIN customers USING (customer_id)
INNER JOIN employees USING (employee_id)
WHERE orders.ship_via = (SELECT shipper_id FROM shippers WHERE company_name = 'United Package')
AND customers.city = 'London' AND employees.city = 'London'

-- 2. Наименование продукта, количество товара (product_name и units_in_stock в табл products),
-- имя поставщика и его телефон (contact_name и phone в табл suppliers) для таких продуктов,
-- которые не сняты с продажи (поле discontinued) и которых меньше 25 и которые в категориях Dairy Products и Condiments.
-- Отсортировать результат по возрастанию количества оставшегося товара.

SELECT product_name, units_in_stock, suppliers.contact_name, suppliers.phone
FROM products
INNER JOIN categories USING(category_id)
INNER JOIN suppliers USING(supplier_id)
WHERE category_name IN ('Dairy Products', 'Condiments')
AND discontinued <> 1 AND units_in_stock < 25
ORDER BY units_in_stock

-- 3. Список компаний заказчиков (company_name из табл customers), не сделавших ни одного заказа

SELECT customers.company_name, order_id
FROM orders
RIGHT JOIN customers USING(customer_id)
WHERE order_id IS NULL

-- 4. уникальные названия продуктов, которых заказано ровно 10 единиц (количество заказанных единиц см в колонке quantity табл order_details)
-- Этот запрос написать именно с использованием подзапроса.
SELECT product_name from products
WHERE product_id IN (SELECT product_id FROM order_details WHERE quantity = 10)