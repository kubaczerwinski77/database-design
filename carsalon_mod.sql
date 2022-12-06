-- Denormalization
BEGIN;
ALTER TABLE insurances
ADD COLUMN type VARCHAR(50);
ALTER TABLE insurances
ADD COLUMN ratio float4;
UPDATE insurances
SET type = subquery.type,
    ratio = subquery.ratio
FROM (
        SELECT id,
            type,
            ratio
        FROM insurancetypes
    ) AS subquery
WHERE insurances.FK_InsuranceTypes = subquery.id;
ALTER TABLE insurances DROP COLUMN fk_insurancetypes;
DROP TABLE insurancetypes;
COMMIT;


-- Add price
BEGIN;
ALTER TABLE insurances
ADD COLUMN price float4;
UPDATE insurances
SET price = subquery.price * ratio
FROM (
        SELECT orders.id as Order_Id,
            Cars.price as price
        FROM Orders
            INNER JOIN orderpositions ON orders.id = orderpositions.FK_Orders
            INNER JOIN cars ON cars.id = orderpositions.FK_Cars
    ) AS subquery
WHERE insurances.FK_Orders = subquery.Order_Id;
SELECT *
from insurances;
ROLLBACK;