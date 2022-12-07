CREATE TYPE insurance_enum AS ENUM('ac', 'oc', 'assistance');

-- Denormalization
BEGIN;
ALTER TABLE insurances
ADD COLUMN type insurance_enum;
ALTER TABLE insurances
ADD COLUMN ratio float4;
UPDATE insurances
SET type = subquery.type::insurance_enum,
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

COMMIT;

-- Connect Car to Insurance
BEGIN;
ALTER TABLE Insurances
    ADD FK_Cars uuid;

UPDATE insurances
SET FK_Cars = subquery.Car_id
FROM (SELECT orders.id as Order_Id,
             Cars.id   as Car_id
      FROM Orders
               INNER JOIN orderpositions ON orders.id = orderpositions.FK_Orders
               INNER JOIN cars ON cars.id = orderpositions.FK_Cars) AS subquery
WHERE insurances.FK_Orders = subquery.Order_Id;

ALTER TABLE Insurances
    ADD FOREIGN KEY (FK_Cars) REFERENCES Cars (id);

ALTER TABLE Insurances
    DROP CONSTRAINT insurances_fk_orders_fkey;

ALTER TABLE Insurances
    DROP COLUMN FK_Orders;

COMMIT;

BEGIN;
ALTER TABLE Insurances ADD CHECK (FK_Cars IS NOT NULL);
ALTER TABLE Insurances ADD CHECK (ratio > 0 AND ratio < 1);
ALTER TABLE Insurances ADD CHECK (price > 0);
ALTER TABLE Insurances ALTER COLUMN ratio SET NOT NULL;
ALTER TABLE Insurances ALTER COLUMN price SET NOT NULL;
ALTER TABLE Insurances ALTER COLUMN FK_Cars SET NOT NULL;
ALTER TABLE Insurances ALTER COLUMN type SET NOT NULL;
COMMIT;


-- Query 11 do przerobienia
select insurancetypes.type AS "Typ ubezpieczenia", count(*) AS "Liczba sprzedanych w ostatnim roku" 
from insurances 
join insurancetypes 
on insurancetypes.id = insurances.fk_insurancetypes 
where date_part('year', age(insurances.conclusion_date)) < 1 
group by insurancetypes.type;

-- Queries

-- Samochody bez ubezpieczenia
SELECT insurances.id, Cars.id 
FROM Cars
LEFT JOIN insurances ON insurances.FK_Cars = cars.id
where insurances.id is null;

-- Query 11 przerobiona
select type AS "Typ ubezpieczenia", count(*) AS "Liczba sprzedanych w ostatnim roku" 
from insurances 
where date_part('year', age(conclusion_date)) < 1 
group by type;


-- Samochody z ubezpieczeniem po modyfikacji

SELECT COUNT(*)
FROM Cars
JOIN insurances ON insurances.FK_Cars = cars.id;

-- Samochody z ubezpieczeniem przed modyfikacją
SELECT COUNT(*)
FROM Cars
INNER JOIN orderpositions ON orderpositions.FK_Cars = cars.id
INNER JOIN orders ON orders.id = orderpositions.FK_Orders
INNER JOIN insurances ON insurances.FK_Orders = orders.id;
