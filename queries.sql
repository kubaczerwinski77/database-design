-- Query 1
SELECT Positions.name, COUNT(Employees.id) as number
FROM Employees
INNER JOIN Positions
ON Employees.FK_Positions = Positions.id
WHERE employment_date > current_date - interval '20' year
GROUP BY Positions.name
ORDER BY number ASC;

-- Query 2
SELECT first_name, last_name, email, phone_number
FROM Customers
INNER JOIN Users
ON Customers.FK_Users = Users.id
INNER JOIN Orders
ON Orders.FK_Customers = Customers.id
INNER JOIN OrderStatuses
ON Orders.FK_OrderStatuses = OrderStatuses.id
WHERE OrderStatuses.status = 'awaiting payment';

-- Query 3
SELECT * FROM CarAccessories
LEFT JOIN OrderPositions 
ON CarAccessories.id = OrderPositions.fk_caraccessories
WHERE OrderPositions.fk_caraccessories IS NULL;

-- Query 4
SELECT name
FROM OriginCountries
INNER JOIN Cars
ON Cars.FK_OriginCountries = OriginCountries.id
GROUP BY name;

--Query 5

select avg((carstatuses.status = 'Historic')::int * 100) AS "Historic cars percentage" 
from cars 
join carstatuses 
on cars.fk_carstatuses = carstatuses.id;

-- Query 6
SELECT name, COUNT(Services.id) as number
FROM 
Services
INNER JOIN OrderPositions 
ON OrderPositions.FK_Services = Services.id
INNER JOIN Orders
ON OrderPositions.FK_Orders = Orders.id
GROUP BY name
ORDER BY number ASC;

-- Query 7
select brands.name as "Brand name", count(*) as "Sold" 
from brands 
join models 
on models.fk_brands = brands.id 
join cars 
on cars.fk_models = models.id 
join orderpositions 
on orderpositions.fk_cars = cars.id 
group by brands.name 
order by count(*) desc 
limit 5;

-- Query 8
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

-- Query 10
SELECT Positions.name, COUNT(Employees.id) as number
FROM Employees
INNER JOIN Positions
ON Employees.FK_Positions = Positions.id
WHERE employment_date < current_date - interval '10' year
GROUP BY Positions.name
ORDER BY number DESC;

-- Query 11
select insurancetypes.type AS "Typ ubezpieczenia", count(*) AS "Liczba sprzedanych w ostatnim roku" 
from insurances 
join insurancetypes 
on insurancetypes.id = insurances.fk_insurancetypes 
where date_part('year', age(insurances.conclusion_date)) < 1 
group by insurancetypes.type;

-- Query 12
SELECT Customers.id, Users.first_name, Users.last_name, COUNT(Orders.id) AS Number, Payments.id
FROM Customers JOIN Users ON Users.id = Customers.fk_users JOIN Orders ON Orders.FK_Customers = Customers.id LEFT JOIN Payments on Payments.FK_Orders = Orders.id
WHERE Payments.id IS NULL
GROUP BY Customers.id
ORDER BY Number DESC;

