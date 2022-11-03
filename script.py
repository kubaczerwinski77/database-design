import random
import csv
import psycopg2
import DataGenerators

# connection to database
conn = psycopg2.connect("dbname=carsalon user=postgres password=admin")
cur = conn.cursor()


def get_random(list_of_values):
    return random.choice(list_of_values)


def pop_random(list_to_pop):
    return list_to_pop.pop(random.randrange(len(list_to_pop)))


def add_value(column, values_list):
    if column[:7] == 'UNIQUE_':
        val = pop_random(values_list)
        if type(val) is int:
            return str(val)
        return f"""'{val}'"""
    elif column[:5] == "NULL_":
        if random.randrange(1, 10) < 3:
            return """NULL"""
    val = get_random(values_list)
    if type(val) is int:
        return str(val)
    return f"""'{val}'"""


def generate_sql(table_name, **kwargs):
    # kwargs are in form of column_name: list_of_values to be chosen at random and inserted ie. drivetrain:['rwd','fwd']
    # if column should have only unique values then name the column UNIQUE_column_name such as UNIQUE_type

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
        sql += add_value(key, item) + ','
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


def generate_prices(count, min, max):
    return [round(random.uniform(min, max), 2) for x in range(count)]


def csv_to_list(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        return [item for sublist in reader for item in sublist]


def insert_accessory_types():
    names = csv_to_list('data/AccesoryTypes.csv')
    count = len(names)
    uuids = DataGenerators.generate_uuids(count)

    for i in range(count):
        statement = generate_sql('AccessoryTypes', UNIQUE_id=uuids, UNIQUE_name=names)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_brands():
    names = csv_to_list('data/brands.csv')
    count = len(names)
    uuids = DataGenerators.generate_uuids(count)

    for i in range(count):
        statement = generate_sql('Brands', UNIQUE_id=uuids, UNIQUE_name=names)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_car_accessories(count):
    uuids = DataGenerators.generate_uuids(count)

    names = csv_to_list('data/AccessoryNameParts.csv')
    registration = DataGenerators.generate_registration_numbers(count)
    prices = DataGenerators.generate_floats(count, 10, 1000)
    comments = ["good part", 'Oem', 'Oe', 'Custom']
    Fk_accessory_type = get_foreign_keys('AccessoryTypes', cur)

    for i in range(count):
        statement = generate_sql('CarAccessories', UNIQUE_id=uuids, name=names, UNIQUE_registration_number=registration,
                                 price_per_unit=prices, NULL_comments=comments, FK_AccessoryTypes=Fk_accessory_type)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_car_bodies(count):
    types = csv_to_list('data/CarBodyTypes.csv')
    uuids = DataGenerators.generate_uuids(count)
    doors = [3, 5]
    seats = [2, 4, 5, 7]

    for i in range(count):
        statement = generate_sql('CarBodies', UNIQUE_id=uuids, type=types, door_number=doors, seat_number=seats)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_car_drivetrains():
    types = csv_to_list('data/drivetrains.csv')[0:]
    count = len(types)
    uuids = DataGenerators.generate_uuids(count)

    for i in range(count):
        statement = generate_sql('CarDrivetrains', UNIQUE_id=uuids, UNIQUE_type=types)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_car_equipments(count):
    uuids = DataGenerators.generate_uuids(count)
    names = csv_to_list('data/CarEquipmentsNames.csv')
    prices = DataGenerators.generate_floats(count, 1000, 10000)
    codes = DataGenerators.generate_equipment_codes(count)

    for i in range(count):
        statement = generate_sql('CarEquipments', UNIQUE_id=uuids, name=names, price=prices, UNIQUE_code=codes)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def inset_car_power_supplies():
    types = csv_to_list('data/CarPowerSuppliesTypes.csv')
    count = len(types)

    uuids = DataGenerators.generate_uuids(count)

    for i in range(count):
        statement = generate_sql('CarPowerSupplies', UNIQUE_id=uuids, UNIQUE_type=types)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_car_statues():
    statuses = csv_to_list('data/CarStatusesTypes.csv')
    count = len(statuses)
    uuids = DataGenerators.generate_uuids(count)
    for i in range(count):
        statement = generate_sql('CarStatuses', UNIQUE_id=uuids, UNIQUE_status=statuses)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_engines(count):
    uuids = DataGenerators.generate_uuids(count)
    name = DataGenerators.generate_strings(count, 2, 6)
    capacities = DataGenerators.generate_floats(count, 600, 7000)
    powers = DataGenerators.generate_ints(count, 100, 1000)
    torques = DataGenerators.generate_ints(count, 50, 500)
    cylinders = csv_to_list('data/cylinder_arrangement.csv')
    fk_power = get_foreign_keys('CarPowerSupplies', cur)

    for i in range(count):
        statement = generate_sql('Engines', UNIQUE_id=uuids, name=name, capacity=capacities, power=powers,
                                 torque=torques, cylinder_arrangement=cylinders, FK_CarPowerSupplies=fk_power)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def inset_gearboxes():
    types = ['5mt', '6mt', '6at', '7dct', '8at']
    count = len(types)
    uuids = DataGenerators.generate_uuids(count)

    for i in range(count):
        statement = generate_sql('Gearboxes', UNIQUE_id=uuids, UNIQUE_type=types)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_insurace_types():
    types = DataGenerators.generate_ints(10, 1, 20)
    count = len(types)
    uuids = DataGenerators.generate_uuids(count)

    for i in range(count):
        statement = generate_sql('InsuranceTypes', UNIQUE_id=uuids, type=types)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def inset_models():
    models = list(set(csv_to_list('data/Models (1).csv')))
    count = len(models)
    uuids = DataGenerators.generate_uuids(count)
    descriptions = ['fast coupe', 'sport sedan', 'racecar', 'family car']
    fk_brands = get_foreign_keys('Brands', cur)
    fk_drivetrains = get_foreign_keys('CarDrivetrains', cur)
    fk_gearboxes = get_foreign_keys('Gearboxes', cur)

    for i in range(count):
        statement = generate_sql('Models', UNIQUE_id=uuids, UNIQUE_name=models, NULL_description=descriptions,
                                 FK_Brands=fk_brands, FK_CarDrivetrains=fk_drivetrains, FK_Gearboxes=fk_gearboxes)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_order_statuses():
    statuses = csv_to_list('data/order_statuses.csv')
    count = len(statuses)
    uuids = DataGenerators.generate_uuids(count)
    for i in range(count):
        statement = generate_sql('OrderStatuses', UNIQUE_id=uuids, status=statuses)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_origin_countries():
    names = csv_to_list('data/Countries.csv')
    count = len(names)
    uuids = DataGenerators.generate_uuids(count)

    for i in range(count):
        statement = generate_sql('OriginCountries', UNIQUE_id=uuids, UNIQUE_name=names)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def inset_positions():
    names = list(set(csv_to_list('data/PositionsNames.csv')))
    count = len(names)
    uuids = DataGenerators.generate_uuids(count)
    for i in range(count):
        statement = generate_sql('Positions', UNIQUE_id=uuids, UNIQUE_name=names)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_services():
    names = csv_to_list('data/service_names.csv')
    count = len(names)
    uuids = DataGenerators.generate_uuids(count)
    descriptions = ['yearly', 'free', 'varranty']
    prices = DataGenerators.generate_floats(count, 100, 10000)

    for i in range(count):
        statement = generate_sql('Services', UNIQUE_id=uuids, UNIQUE_name=names, NULL_description=descriptions,
                                 price=prices)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_sexes():
    sexes = csv_to_list('data/sexes.csv')
    count = len(sexes)
    uuids = DataGenerators.generate_uuids(count)
    for i in range(count):
        statement = generate_sql('Sexes', UNIQUE_id=uuids, UNIQUE_symbol=sexes)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_steering():
    types = csv_to_list('data/steering_wheels.csv')
    count = len(types)
    uuids = DataGenerators.generate_uuids(count)

    for i in range(count):
        statement = generate_sql('SteeringWheels', UNIQUE_id=uuids, UNIQUE_type=types)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_users(count):
    uuids = DataGenerators.generate_uuids(count)
    usenrames = csv_to_list('data/usernames.csv')
    emails = csv_to_list('data/emails.csv')
    passwords = DataGenerators.generate_strings(count, 6, 19)
    first_names = csv_to_list('data/Names.csv')
    last_names = csv_to_list('data/Surnames.csv')
    birth = DataGenerators.generate_dates(count, 1967, 2000)
    phones = DataGenerators.generate_phones(count)
    pesels = DataGenerators.generate_pesels(count)
    addresses = csv_to_list('data/addresses.csv')
    Fk_sexes = get_foreign_keys('Sexes', cur)

    for i in range(count):
        statement = generate_sql('Users', UNIQUE_id=uuids, UNIQUE_username=usenrames, UNIQUE_email=emails,
                                 password=passwords, first_name=first_names, last_name=last_names, date_of_birth=birth,
                                 phone_number=phones, pesel=pesels, address=addresses, FK_Sexes=Fk_sexes)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_varnish_types():
    types = csv_to_list('data/VarnishTypes.csv')
    count = len(types)
    uuids = DataGenerators.generate_uuids(count)

    for i in range(count):
        statement = generate_sql('VarnishTypes', UNIQUE_id=uuids, UNIQUE_type=types)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_varnish():
    names = csv_to_list('data/Colors.csv')
    codes = csv_to_list('data/ColorCodes.csv')
    count = len(codes)
    uuids = DataGenerators.generate_uuids(count)
    fk_varnishtypes = get_foreign_keys('VarnishTypes', cur)

    for i in range(count):
        statement = generate_sql('Varnishes', UNIQUE_id=uuids, UNIQUE_name=names, UNIQUE_code=codes,
                                 FK_VarnishTypes=fk_varnishtypes)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_customers(count):
    uuids = DataGenerators.generate_uuids(count)
    fk_users = get_foreign_keys('Users', cur)[:count]
    print(len(fk_users))
    for i in range(count):
        statement = generate_sql('Customers', UNIQUE_id=uuids, UNIQUE_FK_Users=fk_users)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_employees(count):
    uuids = DataGenerators.generate_uuids(count)
    emplyment_dates = DataGenerators.generate_dates(count, 1980, 2011)
    dismissals = DataGenerators.generate_dates(count // 4, 2015, 2022)
    fk_positions = get_foreign_keys('Positions', cur)
    fk_users = get_foreign_keys('Users', cur)

    for i in range(count):
        statement = generate_sql('Employees', UNIQUE_id=uuids, employment_date=emplyment_dates,
                                 NULL_dismissal_date=dismissals, FK_Positions=fk_positions, FK_Users=fk_users)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_cars(count):
    uuids = DataGenerators.generate_uuids(count)
    vins = DataGenerators.generate_vins(count)
    prices = DataGenerators.generate_floats(count // 2, 1000, 100000)
    production_dates = DataGenerators.generate_dates(count, 1968, 2022)
    mileages = DataGenerators.generate_ints(count, 1, 100000)
    descriptions = ["new", 'used', 'grandma drove to church']
    fk_engines = get_foreign_keys('Engines', cur)
    fk_models = get_foreign_keys('Models', cur)
    fk_origin = get_foreign_keys('OriginCountries', cur)
    fk_car_bodies = get_foreign_keys('CarBodies', cur)
    fk_varnishes = get_foreign_keys('Varnishes', cur)
    fk_customers = get_foreign_keys('Customers', cur)
    fk_steering = get_foreign_keys('SteeringWheels', cur)
    fk_car_statuses = get_foreign_keys('CarStatuses', cur)

    for i in range(count):
        statement = generate_sql('Cars', UNIQUE_id=uuids, UNIQUE_vin=vins, price=prices,
                                 production_date=production_dates,
                                 mileage=mileages, NULL_description=descriptions, FK_Engines=fk_engines,
                                 FK_Models=fk_models,
                                 FK_OriginCountries=fk_origin, FK_CarBodies=fk_car_bodies, FK_Varnishes=fk_varnishes,
                                 FK_Customers=fk_customers,
                                 FK_SteeringWheels=fk_steering, FK_CarStatuses=fk_car_statuses)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_configurations(count):
    uuids = DataGenerators.generate_uuids(count)
    fk_cars = get_foreign_keys('Cars', cur)
    fk_eq = get_foreign_keys('CarEquipments', cur)

    for i in range(count):
        statement = generate_sql('Configurations', UNIQUE_id=uuids, FK_Cars=fk_cars, FK_CarEquipments=fk_eq)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_orders(count):
    uuids = DataGenerators.generate_uuids(count)
    numbers = DataGenerators.generate_strings(count, 8, 20)
    date_of_applications = DataGenerators.generate_dates(count, 2018, 2019)
    date_of_realisations = DataGenerators.generate_dates(count, 2020, 2022)
    comments = ['lost in delivery', 'unavaliable at the moment', ' delivery from china', 'must be manufactured first']
    fk_customers = get_foreign_keys('Customers', cur)
    fk_order_statuses = get_foreign_keys('OrderStatuses', cur)

    for i in range(count):
        statement = generate_sql('Orders', UNIQUE_id=uuids, UNIQUE_number=numbers,
                                 date_of_application=date_of_applications,
                                 NULL_date_of_realisation=date_of_realisations, NULL_comments=comments,
                                 FK_Customers=fk_customers,
                                 FK_OrderStatuses=fk_order_statuses)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_order_positions(count):
    uuids = DataGenerators.generate_uuids(count)
    amounts = DataGenerators.generate_ints(count, 1, 100)
    comments = ['lost in delivery', 'unavaliable at the moment', ' delivery from china', 'must be manufactured first']
    fk_orders = get_foreign_keys('Orders', cur)
    fk_cars = get_foreign_keys('Cars', cur)
    fk_services = get_foreign_keys('Services', cur)
    fk_car_accessories = get_foreign_keys('CarAccessories', cur)
    for i in range(count):
        # print(i)
        r = random.randrange(1, 3)
        if r == 1:
            statement = generate_sql('OrderPositions', UNIQUE_id=uuids, amount=amounts, NULL_comments=comments,
                                     FK_Orders=fk_orders, NULL_FK_Cars=fk_cars, NULL_FK_Services=fk_services,
                                     FK_CarAccessories=fk_car_accessories)
        elif r == 2:
            statement = generate_sql('OrderPositions', UNIQUE_id=uuids, amount=amounts, NULL_comments=comments,
                                     FK_Orders=fk_orders, NULL_FK_Cars=fk_cars, FK_Services=fk_services,
                                     NULL_FK_CarAccessories=fk_car_accessories)
        else:
            statement = generate_sql('OrderPositions', UNIQUE_id=uuids, amount=amounts, NULL_comments=comments,
                                     FK_Orders=fk_orders, FK_Cars=fk_cars, NULL_FK_Services=fk_services,
                                     NULL_FK_CarAccessories=fk_car_accessories)
        print(i)
        try:
            cur.execute(statement)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_insurances(count):
    uuids = DataGenerators.generate_uuids(count)
    policy_number = DataGenerators.generate_ints(count, 100, 10000000)
    commitments = DataGenerators.generate_ints(count, 1, 700)
    conclusions = DataGenerators.generate_dates(count, 2015, 2022)
    comments = ['bought with car', 'witout discounts', 'SalePakage']
    fk_insurance_types = get_foreign_keys('InsuranceTypes', cur)
    fk_orders = get_foreign_keys('Orders', cur)
    for i in range(count):

        statement = generate_sql('Insurances', UNIQUE_id=uuids, UNIQUE_policy_number=policy_number,
                                 commitment_period_in_days=commitments, conclusion_date=conclusions,
                                 NULL_comments=comments, FK_InsuranceTypes=fk_insurance_types, FK_Orders=fk_orders)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)

            # rollback the previous transaction before starting another
            conn.rollback()


def insert_payments(count):
    uuids = DataGenerators.generate_uuids(count)
    amounts = DataGenerators.generate_floats(count, 1, 100000)
    invoices = DataGenerators.generate_strings(count, 12, 16)
    deadlines = DataGenerators.generate_dates(count, 2018, 2019)
    payment_dates = DataGenerators.generate_dates(count, 2020, 2021)
    fk_orders = get_foreign_keys('Orders', cur)
    for i in range(count):

        statement = generate_sql('Payments', UNIQUE_id=uuids, amount=amounts, NULL_invoice_number=invoices,
                                 NULL_deadline_date=deadlines, payment_date=payment_dates, FK_Orders=fk_orders)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)


def insert_test_drives(count):
    uuids = DataGenerators.generate_uuids(count)
    date = DataGenerators.generate_dates(count, 2015, 2022)
    start_times = DataGenerators.generate_timestamps(count, 2018, 2019)
    end_times = DataGenerators.generate_timestamps(count, 2020, 2022)
    comments = ['car crashed', 'driver caused accident', 'custromer didnt attend']
    fk_employees = get_foreign_keys('Employees', cur)
    fk_customers = get_foreign_keys("Customers", cur)
    fk_cars = get_foreign_keys('Cars', cur)

    for i in range(count):

        statement = generate_sql('TestDrives', UNIQUE_id=uuids, date=date, start_time=start_times, end_time=end_times,
                                 NULL_comments=comments, FK_Employees=fk_employees, FK_Customers=fk_customers,
                                 FK_Cars=fk_cars)
        try:
            cur.execute(statement)
            print(i)
        except Exception as err:
            # pass exception to function
            print(err)


# insert_accessory_types(cur)
# insert_brands()
# insert_CarAccessories(100)
# insert_car_bodies(20)
# insert_car_drivetrains()
# insert_car_equipments(30)
# inset_car_power_supplies()
# insert_car_statues()
# insert_engines(21)
# inset_gearboxes()
# insert_insurace_types()
# inset_models()
# insert_order_statuses()
# insert_origin_countries()
# inset_positions()
# insert_services()
# insert_sexes()
# insert_steering()
# insert_users(1000)
# insert_varnish_types()
# insert_varnish()
# insert_customers(800)
# insert_employees(200)
# insert_cars(10000)
# insert_configurations(300000)
# print(DataGenerators.generate_timestamps(10,1960,2000))

# insert_orders(1000)
# insert_order_positions(300000)
# insert_insurances(30000)
# insert_payments(30000)

# insert_testDrives(30000)


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


conn.commit()
cur.close()
conn.close()
