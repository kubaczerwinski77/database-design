import random
import csv
import psycopg2
import DataGenerators

# connection to database
conn = psycopg2.connect("dbname=carsalon user=postgres password=admin")
cur = conn.cursor()


def get_random(list_of_values):
    return random.choice(list_of_values)


def pop_random(list_of_values):
    return list_of_values.pop(random.randrange(len(list_of_values)))


def add_value(column, values_list,prob, iteration):
    if column == 'start_time' or column == 'end_time' or column == 'date_of_application':
            return f"""'{values_list[iteration]}'"""
    elif column == 'NULL_date_of_realisation':
        if random.randrange(1, 10) < prob:
                return """NULL"""
        else:
                return f"""'{values_list[iteration]}'"""
    
    if column[:7] == 'UNIQUE_':
        val = pop_random(values_list)
        if type(val) is int:
            return str(val)
        return f"""'{val}'"""
    elif column[:5] == "NULL_":
        if random.randrange(1, 10) < prob:
            return """NULL"""
    val = get_random(values_list)
    if type(val) is int:
        return str(val)
    return f"""'{val}'"""


def generate_sql(table_name, iteration, **kwargs):
    # kwargs are in form of column_name: list_of_values to be chosen at random and inserted ie. drivetrain:['rwd','fwd']
    # if column should have only unique values then name the column UNIQUE_column_name such as UNIQUE_type
    null_probability=3
    if(table_name=='OrderPositions'):
        null_probability=11

    sql = f"""INSERT INTO {table_name} ("""
    columns = list(kwargs)

    for column in columns:
        if column[:7] == 'UNIQUE_':
            column = column[7:]
        if column[:5] == "NULL_":
            column = column[5:]
        sql += column + ','
    sql = sql[:-1]

    sql += ') VALUES('

    for key, item in kwargs.items():
        sql += add_value(key, item,null_probability, iteration) + ','
    sql = sql[:-1]
    sql += ');'

    return sql


def get_foreign_keys(tablename, cursor):
    cursor.execute(f"""SELECT id from {tablename}""")
    data = cursor.fetchall()
    uuids = []
    for row in data:
        uuids.append(row[0])
    return uuids


def csv_to_list(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        return [item for sublist in reader for item in sublist]


# DATA lists and counts of inserets to the table
# Naming scheme is list: TABLENAME_ATTRIBUTE ie ACCESORY_TYPES_NAMES
# Count of inserts: COUNT_OF_TABLENAME ie COUNT_OF_ACCESSORY_TYPES=len(ACCESORY_TYPES_NAMES)


def insert(table_name, count, **kwargs):
    for i in range(count):
        statement = generate_sql(table_name, i, **kwargs)
        try:
            cur.execute(statement)
            print(table_name)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()
    conn.commit()


# AccessoryTypes
def insert_accessory_type():
    name = csv_to_list('data/AccesoryTypes.csv')
    count = len(name)
    uuid = DataGenerators.generate_uuids(count)
    insert('AccessoryTypes', count, UNIQUE_id=uuid, UNIQUE_name=name)


# Brands
def insert_brands():
    names = csv_to_list('data/brands.csv')
    count = len(names)
    uuids = DataGenerators.generate_uuids(count)
    insert('Brands', count, UNIQUE_id=uuids, UNIQUE_name=names)


# CarAccessories
def insert_car_accessories(count):
    names = csv_to_list('data/AccessoryNameParts.csv')
    uuids = DataGenerators.generate_uuids(count)
    registrations = DataGenerators.generate_registration_numbers(count)
    prices = DataGenerators.generate_floats(count, 10, 1000)
    comments = ["good part", 'Oem', 'Oe', 'Custom']
    fk_accessory_type = get_foreign_keys('AccessoryTypes', cur)
    insert('CarAccessories', count, UNIQUE_id=uuids, name=names
           , UNIQUE_registration_number=registrations, price_per_unit=prices
           , NULL_comments=comments, FK_AccessoryTypes=fk_accessory_type)


# CarBodies
def insert_car_bodies(count):
    types = csv_to_list('data/CarBodyTypes.csv')
    uuids = DataGenerators.generate_uuids(count)
    doors = [3, 5]
    seats = [2, 4, 5, 7]
    insert('CarBodies', count, UNIQUE_id=uuids, type=types, door_number=doors
           , seat_number=seats)


# CarDrivetrains
def insert_car_drivetrains():
    types = csv_to_list('data/drivetrains.csv')
    count = len(types)
    uuids = DataGenerators.generate_uuids(count)
    insert('CarDrivetrains', count, UNIQUE_id=uuids, UNIQUE_type=types)


# CarEquipments
def insert_car_equipments(count):
    uuids = DataGenerators.generate_uuids(count)
    names = csv_to_list('data/CarEquipmentsNames.csv')
    prices = DataGenerators.generate_floats(count, 1000, 10000)
    codes = DataGenerators.generate_equipment_codes(count)
    insert('CarEquipments', count, UNIQUE_id=uuids, name=names
           , price=prices, UNIQUE_code=codes)


# CarPowerSupplies
def insert_car_power_supplies():
    types = csv_to_list('data/CarPowerSuppliesTypes.csv')
    count = len(types)
    uuids = DataGenerators.generate_uuids(count)
    insert('CarPowerSupplies', count, UNIQUE_id=uuids,
           UNIQUE_type=types)


# CarStatuses
def insert_car_statuses():
    statuses = csv_to_list('data/CarStatusesTypes.csv')
    count = len(statuses)
    uuids = DataGenerators.generate_uuids(count)
    insert('CarStatuses', count, UNIQUE_id=uuids, UNIQUE_status=statuses)



# Engines
def insert_engines(count):
    uuids = DataGenerators.generate_uuids(count)
    names = DataGenerators.generate_strings(count, 2, 6)
    capacities = DataGenerators.generate_floats(count, 600, 7000)
    powers = DataGenerators.generate_ints(count, 100, 1000)
    torques = DataGenerators.generate_ints(count, 50, 500)
    cylinders = csv_to_list('data/cylinder_arrangement.csv')
    fk_power_supplies = get_foreign_keys('CarPowerSupplies', cur)
    insert('Engines', count, UNIQUE_id=uuids, name=names, capacity=capacities,
           power=powers, torque=torques, cylinder_arrangement=cylinders,
           FK_CarPowerSupplies=fk_power_supplies)


# Gearboxes
def insert_gearboxes():
    types = ['5mt', '6mt', '6at', '7dct', '8at']
    count = len(types)
    uuids = DataGenerators.generate_uuids(count)
    insert('Gearboxes', count, UNIQUE_id=uuids, UNIQUE_type=types)


def insert_insurance_types():
    types = ['oc','ac','assistance']
    count = len(types)
    uuids = DataGenerators.generate_uuids(count)
    insert('InsuranceTypes', count, UNIQUE_id=uuids, UNIQUE_type=types)


def insert_models():
    names = list(set(csv_to_list('data/Models (1).csv')))
    count = len(names)
    uuids = DataGenerators.generate_uuids(count)
    descriptions = ['fast coupe', 'sport sedan', 'racecar', 'family car']
    fk_brands = get_foreign_keys('Brands', cur)
    fk_drivetrains = get_foreign_keys('CarDrivetrains', cur)
    fk_gearboxes = get_foreign_keys('Gearboxes', cur)
    insert('Models', count, UNIQUE_id=uuids, UNIQUE_name=names, NULL_description=descriptions,
           FK_Brands=fk_brands, FK_CarDrivetrains=fk_drivetrains, FK_Gearboxes=fk_gearboxes)


def insert_order_statuses():
    statuses = csv_to_list('data/order_statuses.csv')
    count = len(statuses)
    uuids = DataGenerators.generate_uuids(count)
    insert('OrderStatuses', count, UNIQUE_id=uuids, status=statuses)


def insert_origin_countries():
    names = csv_to_list('data/Countries.csv')
    count = len(names)
    uuids = DataGenerators.generate_uuids(count)
    insert('OriginCountries', count, UNIQUE_id=uuids, UNIQUE_name=names)


# positions
def insert_positions():
    names = list(set(csv_to_list('data/PositionsNames.csv')))
    count = len(names)
    uuids = DataGenerators.generate_uuids(count)
    insert('Positions', count, UNIQUE_id=uuids, UNIQUE_name=names)


# Services
def insert_services():
    names = csv_to_list('data/service_names.csv')
    count = len(names)
    uuids = DataGenerators.generate_uuids(count)
    descriptions = ['yearly', 'free', 'varranty']
    prices = DataGenerators.generate_floats(count, 100, 10000)
    insert('Services', count, UNIQUE_id=uuids, UNIQUE_name=names,
           NULL_description=descriptions, price=prices)


# Sexes
def insert_sexes():
    names = csv_to_list('data/sexes.csv')
    count = len(names)
    uuids = DataGenerators.generate_uuids(count)
    insert('Sexes', count, UNIQUE_id=uuids, UNIQUE_symbol=names)


# SteeringWheels
def insert_steering_wheels():
    types = csv_to_list('data/steering_wheels.csv')
    count = len(types)
    uuids = DataGenerators.generate_uuids(count)
    insert('SteeringWheels', count, UNIQUE_id=uuids, UNIQUE_type=types)


# Users
def insert_users(count):
    uuids = DataGenerators.generate_uuids(count)
    usernames = csv_to_list('data/usernames.csv')
    emails = csv_to_list('data/emails.csv')
    passwords = DataGenerators.generate_strings(count, 6, 19)
    first_names = csv_to_list('data/Names.csv')
    last_names = csv_to_list('data/Surnames.csv')
    births = DataGenerators.generate_dates(count, '1967-1-1', '2000-1-1')
    phones = DataGenerators.generate_phones(count)
    pesels = DataGenerators.generate_pesels(count)
    addresses = csv_to_list('data/addresses.csv')
    fk_sexes = get_foreign_keys('Sexes', cur)
    insert('Users', count, UNIQUE_id=uuids, UNIQUE_username=usernames, UNIQUE_email=emails,
           password=passwords, first_name=first_names, last_name=last_names
           , date_of_birth=births, phone_number=phones, pesel=pesels, address=addresses
           , FK_Sexes=fk_sexes)


# VarnishTYpes
def insert_varnish_types():
    types = csv_to_list('data/VarnishTypes.csv')
    count = len(types)
    uuids = DataGenerators.generate_uuids(count)
    insert('VarnishTypes', count, UNIQUE_id=uuids, UNIQUE_type=types)


# Varnishes
def insert_varnishes():
    names = csv_to_list('data/Colors.csv')
    codes = csv_to_list('data/ColorCodes.csv')
    count = len(codes)
    uuids = DataGenerators.generate_uuids(count)
    fk_varnish_types = get_foreign_keys('VarnishTypes', cur)
    insert('Varnishes', count, UNIQUE_id=uuids, UNIQUE_name=names, UNIQUE_code=codes,
           FK_VarnishTypes=fk_varnish_types)


# Customers
def insert_customers(count):
    uuids = DataGenerators.generate_uuids(count)
    fk_users = get_foreign_keys('Users',
                                cur)  # [:COUNT_OF_CUSTOMERS]#TODO jeśli user może być klientem i pracownikiem to usunąc
    insert('Customers', count, UNIQUE_id=uuids, UNIQUE_FK_Users=fk_users)


# Employees
def insert_employees(count):
    uuids = DataGenerators.generate_uuids(count)
    employment_dates = DataGenerators.generate_dates(count, '1980-1-1', '2011-1-1')
    dismissals_dates = DataGenerators.generate_dates(count // 4, '2015-1-1', '2022-1-1')
    fk_positions = get_foreign_keys('Positions', cur)
    fk_users = get_foreign_keys('Users', cur)
    insert('Employees', count, UNIQUE_id=uuids, employment_date=employment_dates,
           NULL_dismissal_date=dismissals_dates, FK_Positions=fk_positions, FK_Users=fk_users)


# Cars
def insert_cars(count):
    uuids = DataGenerators.generate_uuids(count)
    vins = DataGenerators.generate_vins(count)
    prices = DataGenerators.generate_floats(count // 2, 1000, 100000)
    production_dates = DataGenerators.generate_dates(count, '1968-1-1', '2022-1-1')
    mileages = DataGenerators.generate_ints(count, 1, 100000)
    descriptions = ["new", 'used', 'grandma drove to church']
    fk_engines = get_foreign_keys('Engines', cur)
    fk_models = get_foreign_keys('Models', cur)
    fk_origin_countries = get_foreign_keys('OriginCountries', cur)
    fk_car_bodies = get_foreign_keys('CarBodies', cur)
    fk_varnishes = get_foreign_keys('Varnishes', cur)
    fk_customers = get_foreign_keys('Customers', cur)
    fk_steeringwheels = get_foreign_keys('SteeringWheels', cur)
    fk_car_statuses = get_foreign_keys('CarStatuses', cur)
    insert('Cars', count, UNIQUE_id=uuids, UNIQUE_vin=vins, price=prices,
           production_date=production_dates,
           mileage=mileages, NULL_description=descriptions, FK_Engines=fk_engines,
           FK_Models=fk_models, FK_OriginCountries=fk_origin_countries,
           FK_CarBodies=fk_car_bodies, FK_Varnishes=fk_varnishes,
           FK_Customers=fk_customers, FK_SteeringWheels=fk_steeringwheels, FK_CarStatuses=fk_car_statuses)


# configurations
def insert_configurations(count):
    uuids = DataGenerators.generate_uuids(count)
    fk_cars = get_foreign_keys('Cars', cur)
    fk_equipments = get_foreign_keys('CarEquipments', cur)
    insert('Configurations', count, UNIQUE_id=uuids, FK_Cars=fk_cars,
           FK_CarEquipments=fk_equipments)


# Orders
def insert_orders(count):
    uuids = DataGenerators.generate_uuids(count)
    numbers = DataGenerators.generate_strings(count, 8, 20)
    dates_of_applications = DataGenerators.generate_dates(count, '2018-1-1', '2019-1-1')
    dates_of_realisations = DataGenerators.generate_end_dates(dates_of_applications, max_days=30) 
    comments = ['lost in delivery', 'unavaliable at the moment', ' delivery from china', 'must be manufactured first']
    fk_order_statuses = get_foreign_keys('OrderStatuses', cur)
    fk_customers = get_foreign_keys('Customers', cur)
    insert('Orders', count, UNIQUE_id=uuids, UNIQUE_number=numbers,
           date_of_application=dates_of_applications,
           NULL_date_of_realisation=dates_of_realisations, NULL_comments=comments,
           FK_Customers=fk_customers,
           FK_OrderStatuses=fk_order_statuses)


# OrderPositions

def insert_order_positions(count):
    uuids = DataGenerators.generate_uuids(count)
    amounts = DataGenerators.generate_ints(count, 1, 100)
    comments = ['lost in delivery', 'unavaliable at the moment', ' delivery from china', 'must be manufactured first']
    fk_orders = get_foreign_keys('Orders', cur)
    fk_cars = get_foreign_keys('Cars', cur)
    fk_services = get_foreign_keys('Services', cur)
    fk_car_accessories = get_foreign_keys('CarAccessories', cur)

    for i in range(count):
        r = random.randint(1, 3)
        if r == 1:
            statement = generate_sql('OrderPositions', i,  UNIQUE_id=uuids, amount=amounts, NULL_comments=comments,
                                     FK_Orders=fk_orders, NULL_FK_Cars=fk_cars, NULL_FK_Services=fk_services,
                                     FK_CarAccessories=fk_car_accessories)
        elif r == 2:
            statement = generate_sql('OrderPositions', i,  UNIQUE_id=uuids, amount=amounts, NULL_comments=comments,
                                     FK_Orders=fk_orders, NULL_FK_Cars=fk_cars, FK_Services=fk_services,
                                     NULL_FK_CarAccessories=fk_car_accessories)
        else:
            statement = generate_sql('OrderPositions', i, UNIQUE_id=uuids, amount=amounts, NULL_comments=comments,
                                     FK_Orders=fk_orders, FK_Cars=fk_cars, NULL_FK_Services=fk_services,
                                     NULL_FK_CarAccessories=fk_car_accessories)
        try:
            print('order positions')
            cur.execute(statement)
        except Exception as err:
            print(err)
            conn.rollback()


def insert_insurances(count):
    uuids = DataGenerators.generate_uuids(count)
    policy_number = DataGenerators.generate_ints(count, 100, 10000000)
    commitments = DataGenerators.generate_ints(count, 1, 700)
    conclusions = DataGenerators.generate_dates(count, '2015-1-1', '2022-1-1')
    comments = ['bought with car', 'witout discounts', 'SalePakage']
    fk_insurance_types = get_foreign_keys('InsuranceTypes', cur)
    fk_orders = get_foreign_keys('Orders', cur)
    insert('Insurances',count,UNIQUE_id=uuids, UNIQUE_policy_number=policy_number,
                                 commitment_period_in_days=commitments, conclusion_date=conclusions,
                                 NULL_comments=comments, FK_InsuranceTypes=fk_insurance_types, FK_Orders=fk_orders)


def insert_payments(count):
    uuids = DataGenerators.generate_uuids(count)
    amounts = DataGenerators.generate_floats(count, 1, 100000)
    invoices = DataGenerators.generate_strings(count, 12, 16)
    payment_dates = DataGenerators.generate_dates(count, '2019-1-1', '2020-1-1')
    deadlines = DataGenerators.generate_end_dates(payment_dates, max_days=30)
    fk_orders = get_foreign_keys('Orders', cur)
    insert('Payments', count, UNIQUE_id=uuids, amount=amounts, NULL_invoice_number=invoices,
           NULL_deadline_date=deadlines, payment_date=payment_dates, FK_Orders=fk_orders)


def insert_test_drives(count):
    uuids = DataGenerators.generate_uuids(count)
    start_times = DataGenerators.generate_timestamps(count, '2015-1-1 12:00:00', '2022-1-1 12:00:00')
    end_times = DataGenerators.generate_end_timestamps(start_times, max_minutes=180)
    comments = ['car crashed', 'driver caused accident', 'custromer didnt attend']
    fk_employees = get_foreign_keys('Employees', cur)
    fk_customers = get_foreign_keys("Customers", cur)
    fk_cars = get_foreign_keys('Cars', cur)

    insert('TestDrives',count,UNIQUE_id=uuids, start_time=start_times, end_time=end_times,
                                 NULL_comments=comments, FK_Employees=fk_employees, FK_Customers=fk_customers,
                                 FK_Cars=fk_cars)

def run():
    insert_accessory_type()
    insert_brands()
    insert_car_accessories(100)
    insert_car_bodies(20)
    insert_car_drivetrains()
    insert_car_equipments(30)
    insert_car_power_supplies()
    insert_car_statuses()
    insert_engines(21)
    insert_gearboxes()
    insert_insurance_types()
    insert_models()
    insert_order_statuses()
    insert_origin_countries()
    insert_positions()
    insert_services()
    insert_sexes()
    insert_steering_wheels()
    insert_users(1000)
    insert_varnish_types()
    insert_varnishes()
    insert_customers(800)
    insert_employees(200)
    insert_cars(10000)
    insert_configurations(300000)
    insert_orders(1000)
    insert_order_positions(300000)
    insert_insurances(30000)
    insert_payments(30000)
    insert_test_drives(30000)
run()
#
# uuids = DataGenerators.generate_uuids(3)
# names = ["318i", '316i', '320i']
# descriptions = ['Small city Car']
# FK_car_drivetrains = get_foreign_keys('CarDrivetrains', cur)
#
# statements = generateSql(3, 'Models', id=uuids, UNIQUE_name=names, description=descriptions,
#                          fk_cardrivetrains=FK_car_drivetrains)
# for statement in statements:
#     cur.execute(statement)


cur.close()
conn.close()
