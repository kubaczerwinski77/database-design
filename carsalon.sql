BEGIN;
  CREATE TABLE AccessoryTypes (
    id   uuid NOT NULL, 
    name varchar(100) NOT NULL UNIQUE, 
    PRIMARY KEY (id));

  CREATE TABLE Brands (
    id   uuid NOT NULL, 
    name varchar(100) NOT NULL UNIQUE, 
    PRIMARY KEY (id));

  CREATE TABLE CarAccessories (
    id                  uuid NOT NULL, 
    name                varchar(255) NOT NULL, 
    registration_number varchar(100) NOT NULL UNIQUE, 
    price_per_unit      float4 NOT NULL CHECK (price_per_unit > 0), 
    comments            varchar(255), 
    FK_AccessoryTypes   uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE CarBodies (
    id          uuid NOT NULL, 
    type        varchar(100), 
    door_number INT NOT NULL CHECK(door_number > 0), 
    seat_number INT NOT NULL CHECK(seat_number > 0), 
    PRIMARY KEY (id));

  CREATE TABLE CarDrivetrains (
    id   uuid NOT NULL, 
    type varchar(255) NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE CarEquipments (
    id    uuid NOT NULL, 
    name  varchar(255) NOT NULL, 
    price float4 CHECK (price > 0), 
    code  INT NOT NULL UNIQUE, 
    PRIMARY KEY (id));

  CREATE TABLE CarPowerSupplies (
    id   uuid NOT NULL, 
    type varchar(100) NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE Cars (
    id                 uuid NOT NULL, 
    vin                varchar(17) NOT NULL UNIQUE, 
    price              float4 CHECK (price > 0), 
    production_date    date NOT NULL, 
    mileage            INT NOT NULL CHECK (mileage > 0), 
    description        varchar(255), 
    FK_Engines         uuid NOT NULL, 
    FK_Models          uuid NOT NULL, 
    FK_OriginCountries uuid NOT NULL, 
    FK_CarBodies       uuid NOT NULL, 
    FK_Varnishes       uuid NOT NULL, 
    FK_Users           uuid NOT NULL, 
    FK_SteeringWheels  uuid NOT NULL, 
    FK_CarStatuses     uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE CarStatuses (
    id     uuid NOT NULL, 
    status varchar(255) NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE Configurations (
    id               uuid NOT NULL, 
    FK_Cars          uuid NOT NULL, 
    FK_CarEquipments uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE Employments (
    id              uuid NOT NULL, 
    employment_date date NOT NULL, 
    dismissal_date  date CHECK (dismissal_date > employment_date), 
    FK_Positions    uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE Engines (
    id                   uuid NOT NULL, 
    name                 INT NOT NULL, 
    capacity             float4 NOT NULL CHECK (capacity > 0), 
    power                INT NOT NULL CHECK (power > 0), 
    torque               INT CHECK (torque > 0), 
    cylinder_arrangement INT, 
    FK_CarPowerSupplies  uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE Gearboxes (
    id   uuid NOT NULL, 
    type varchar(255) NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE Insurances (
    id                uuid NOT NULL, 
    policy_number     INT NOT NULL UNIQUE CHECK (policy_number > 0), 
    commitment_period_in_days INT NOT NULL CHECK (commitment_period_in_days > 0), 
    conclusion_date   date NOT NULL, 
    comments          varchar(255), 
    FK_InsuranceTypes uuid NOT NULL, 
    FK_Orders         uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE InsuranceTypes (
    id   uuid NOT NULL, 
    type INT, 
    PRIMARY KEY (id));

  CREATE TABLE Models (
    id                uuid NOT NULL, 
    name              varchar(100) NOT NULL UNIQUE, 
    description       varchar(255), 
    FK_Brands         uuid NOT NULL, 
    FK_CarDrivetrains uuid NOT NULL, 
    FK_Gearboxes      uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE OrderPositions (
    id                uuid NOT NULL, 
    amount            INT NOT NULL CHECK (amount > 0), 
    comments          varchar(100), 
    FK_Orders         uuid, 
    FK_Cars           uuid, 
    FK_Services       uuid, 
    FK_CarAccessories uuid, 
    PRIMARY KEY (id));

  CREATE TABLE Orders (
    id                  uuid NOT NULL, 
    number              varchar(50) NOT NULL, 
    date_of_application date NOT NULL, 
    date_of_realisation date CHECK (date_of_realisation >= date_of_application), 
    comments            varchar(255), 
    FK_Users            uuid NOT NULL, 
    FK_OrderStatuses    uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE OrderStatuses (
    id     uuid NOT NULL, 
    status varchar(255) NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE OriginCountries (
    id   uuid NOT NULL, 
    name varchar(100) NOT NULL UNIQUE, 
    PRIMARY KEY (id));

  CREATE TABLE Payments (
    id             uuid NOT NULL, 
    amount         float4 NOT NULL CHECK (amount > 0), 
    invoice_number varchar(100),
    deadline_date  date, 
    payment_date   date NOT NULL, 
    FK_Orders      uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE Positions (
    id   uuid NOT NULL, 
    name varchar(100) NOT NULL UNIQUE, 
    PRIMARY KEY (id));

  CREATE TABLE Services (
    id          uuid NOT NULL, 
    name        varchar(50) NOT NULL UNIQUE, 
    description varchar(255), 
    price       float4 CHECK (price > 0), 
    PRIMARY KEY (id));

  CREATE TABLE Sexes (
    id     uuid NOT NULL, 
    symbol varchar(1) NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE SteeringWheels (
    id   uuid NOT NULL, 
    type varchar(255) NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE TestDrives (
    id          uuid NOT NULL, 
    "date"      date NOT NULL, 
    start_time  timestamp NOT NULL, 
    end_time    timestamp NOT NULL CHECK (end_time > start_time), 
    comments    varchar(255), 
    FK_Employee uuid NOT NULL, 
    FK_Customer uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE Users (
    id             uuid NOT NULL, 
    username       varchar(50) NOT NULL UNIQUE, 
    email          varchar(100) NOT NULL UNIQUE, 
    password       varchar(255) NOT NULL, 
    first_name     varchar(255), 
    last_name      varchar(255), 
    date_of_birth  date CHECK(date_of_birth > '1900-01-01'), 
    phone_number   varchar(20), 
    pesel          varchar(11), 
    address        varchar(255), 
    FK_Employments uuid, 
    FK_Sexes       uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE MATERIALIZED VIEW Employees AS
    SELECT id FROM Users
    WHERE FK_Employments IS NOT NULL;

  CREATE MATERIALIZED VIEW Customers AS
    SELECT id FROM Users
    WHERE FK_Employments IS NULL;

  CREATE TABLE Varnishes (
    id              uuid NOT NULL, 
    name            varchar(100) NOT NULL, 
    code            varchar(50) NOT NULL, 
    FK_VarnishTypes uuid NOT NULL, 
    PRIMARY KEY (id));

  CREATE TABLE VarnishTypes (
    id   uuid NOT NULL, 
    type varchar(100) NOT NULL, 
    PRIMARY KEY (id));
COMMIT;

BEGIN;
  ALTER TABLE Cars ADD FOREIGN KEY (FK_Models) REFERENCES Models (id);
  ALTER TABLE Models ADD FOREIGN KEY (FK_Brands) REFERENCES Brands (id);
  ALTER TABLE Cars ADD FOREIGN KEY (FK_OriginCountries) REFERENCES OriginCountries (id);
  ALTER TABLE Cars ADD FOREIGN KEY (FK_CarBodies) REFERENCES CarBodies (id);
  ALTER TABLE Cars ADD FOREIGN KEY (FK_Varnishes) REFERENCES Varnishes (id);
  ALTER TABLE Configurations ADD FOREIGN KEY (FK_Cars) REFERENCES Cars (id);
  ALTER TABLE Configurations ADD FOREIGN KEY (FK_CarEquipments) REFERENCES CarEquipments (id);
  ALTER TABLE Cars ADD FOREIGN KEY (FK_Users) REFERENCES Users (id);
  ALTER TABLE Employments ADD FOREIGN KEY (FK_Positions) REFERENCES Positions (id);
  ALTER TABLE Payments ADD FOREIGN KEY (FK_Orders) REFERENCES Orders (id) ON DELETE CASCADE;
  ALTER TABLE OrderPositions ADD FOREIGN KEY (FK_Orders) REFERENCES Orders (id) ON DELETE CASCADE;
  ALTER TABLE OrderPositions ADD FOREIGN KEY (FK_Cars) REFERENCES Cars (id);
  ALTER TABLE OrderPositions ADD FOREIGN KEY (FK_Services) REFERENCES Services (id);
  ALTER TABLE OrderPositions ADD FOREIGN KEY (FK_CarAccessories) REFERENCES CarAccessories (id);
  ALTER TABLE OrderPositions ADD CHECK ((FK_Cars IS NOT NULL AND FK_Services IS NULL AND FK_CarAccessories IS NULL) OR 
    (FK_Cars IS NULL AND FK_Services IS NOT NULL AND FK_CarAccessories IS NULL) OR (FK_Cars IS NULL AND FK_Services IS NULL AND 
    FK_CarAccessories IS NOT NULL));
  ALTER TABLE CarAccessories ADD FOREIGN KEY (FK_AccessoryTypes) REFERENCES AccessoryTypes (id);
  ALTER TABLE Orders ADD FOREIGN KEY (FK_Users) REFERENCES Users (id) ON DELETE CASCADE;
  ALTER TABLE Users ADD FOREIGN KEY (FK_Employments) REFERENCES Employments (id) ON DELETE CASCADE;
  ALTER TABLE TestDrives ADD FOREIGN KEY (FK_Employee) REFERENCES Users (id);
  ALTER TABLE TestDrives ADD FOREIGN KEY (FK_Customer) REFERENCES Users (id);
  ALTER TABLE Insurances ADD FOREIGN KEY (FK_InsuranceTypes) REFERENCES InsuranceTypes (id);
  ALTER TABLE Orders ADD FOREIGN KEY (FK_OrderStatuses) REFERENCES OrderStatuses (id);
  ALTER TABLE Engines ADD FOREIGN KEY (FK_CarPowerSupplies) REFERENCES CarPowerSupplies (id);
  ALTER TABLE Cars ADD FOREIGN KEY (FK_SteeringWheels) REFERENCES SteeringWheels (id);
  ALTER TABLE Cars ADD FOREIGN KEY (FK_CarStatuses) REFERENCES CarStatuses (id);
  ALTER TABLE Models ADD FOREIGN KEY (FK_CarDrivetrains) REFERENCES CarDrivetrains (id);
  ALTER TABLE Models ADD FOREIGN KEY (FK_Gearboxes) REFERENCES Gearboxes (id);
  ALTER TABLE Varnishes ADD FOREIGN KEY (FK_VarnishTypes) REFERENCES VarnishTypes (id);
  ALTER TABLE Users ADD FOREIGN KEY (FK_Sexes) REFERENCES Sexes (id);
  ALTER TABLE Insurances ADD FOREIGN KEY (FK_Orders) REFERENCES Orders (id) ON DELETE CASCADE;
COMMIT;
-- create or replace function trigger_function()
-- returns trigger as $$
	
-- 	begin
-- 		if tg_op = 'INSERT' then
--       raise exception
-- 		end if;

-- 		return null;
-- 	end;
-- $$ language plpgsql;

-- create trigger nazwa_triggera before insert on TestDrives for each row execute procedure trigger_function();

