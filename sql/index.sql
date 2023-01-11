BEGIN;
-- Btree troche lepszy - kilka ms

-- create index last_name_index on Users using HASH(last_name);
 create index last_name_index on Users(last_name);

explain analyse SELECT Users.first_name, Users.last_name, Orders.number
FROM Users
INNER JOIN Customers
ON Customers.FK_Users = Users.id
INNER JOIN Orders
ON Orders.FK_Customers = Customers.id
WHERE Users.last_name = 'Kempa';

ROLLBACK;

-- Query 1
-- dodanie indeksu na date urodzenia spowodowalo zmniejszenie czasu o jakieś 20-30%

BEGIN;
CREATE INDEX Users_date_of_birth_index ON Users(date_of_birth);


EXPLAIN ANALYZE
SELECT Customers.id, Users.first_name, Users.last_name, Users.date_of_birth 
FROM Customers 
JOIN Users 
ON Users.id = Customers.fk_users 
WHERE date_part('year', age(Users.date_of_birth)) > 50;

ROLLBACK;

-- Query 8
-- po dodaniu indeksu dla Order.date_of_application execution time zmniejszyl sie o ponad polowe

BEGIN;

CREATE INDEX date_of_application_index on Orders(date_of_application);

EXPLAIN ANALYZE
SELECT Orders.number as "Order number", first_name, last_name, email
FROM Orders
INNER JOIN OrderStatuses
ON Orders.FK_OrderStatuses = OrderStatuses.id
INNER JOIN Customers
ON Orders.FK_Customers = Customers.id
INNER JOIN Users
ON Customers.FK_Users = Users.id
WHERE OrderStatuses.status = 'cancelled' AND (date_of_application >= current_date - interval '1' month
  AND date_of_application < current_date);

ROLLBACK;

BEGIN;
-- Hash lepszy, poprawa z 50 ms do 0.05 ms

 create index start_time_index on TestDrives using HASH(start_time);
-- create index start_time_index on TestDrives(start_time);

explain analyse SELECT Users.first_name, Users.last_name
from Users
INNER JOIN Customers
ON Customers.FK_Users = Users.id
INNER JOIN TestDrives
ON Customers.id = TestDrives.FK_Customers
WHERE start_time = '2018-05-14 14:42:22';

ROLLBACK;

BEGIN;
-- Nie pomoglo, bardzo mala roznica
-- create index start_time_index on Payments using HASH(payment_date);
-- create index start_time_index on Payments(payment_date);

explain analyse SELECT Users.first_name, Users.last_name, Orders.number
FROM Users
INNER JOIN Customers
ON Customers.FK_Users = Users.id
INNER JOIN Orders
ON Orders.FK_Customers = Customers.id
INNER JOIN Payments
ON Orders.id = Payments.FK_Orders
WHERE Payments.payment_date = '2019-04-07';

ROLLBACK;

BEGIN;
-- Nulle sa wiec nieefektywnie
-- hash poprawia najbardziej
 create index phone_number_index on Users using HASH(phone_number);
-- create index phone_number_index on Users(phone_number);

explain analyse SELECT Users.first_name, Users.last_name
FROM Users
WHERE phone_number = '183440023';

ROLLBACK;


BEGIN;
-- Query 10
-- Nic nie daje , dalej sequence
-- create index employment_date_index on Employees(employment_date);

explain analyse SELECT Positions.name, COUNT(Employees.id) as number
FROM Employees
INNER JOIN Positions
ON Employees.FK_Positions = Positions.id
WHERE employment_date < current_date - interval '10' year
GROUP BY Positions.name
ORDER BY number DESC;

ROLLBACK;



