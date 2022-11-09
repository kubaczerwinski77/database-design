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