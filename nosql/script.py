import csv

from pymongo import MongoClient

import DataGeneratorsNoSql
from DataGeneratorsNoSql import *


def get_random(list_of_values):
    return random.choice(list_of_values)


def pop_random(list_of_values):
    return list_of_values.pop(random.randrange(len(list_of_values)))


def is_present(probability: float):
    return probability > random.uniform(0, 1)


def decide_to_remove_property(data: dict, properties: list[str], probability: float):
    for property in properties:
        if random.random() > probability:
            del data[property]
    return data


def csv_to_list(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        return [item for sublist in reader for item in sublist]


# create connection
client = MongoClient("mongodb+srv://car-salon:LmrVociSmTXvTjFQ@cluster0.3tezxec.mongodb.net")
db = client["car-salon-script"]


def insert_customer(count: int):
    print("insert customers")
    addresses = csv_to_list('../data/addresses.csv')
    date_of_births = DataGeneratorsNoSql.generate_dates(10, "1900-01-01", "2020-01-01")
    emails = csv_to_list('../data/emails.csv')
    names = csv_to_list('../data/Names.csv')
    lastNames = csv_to_list('../data/Surnames.csv')
    passwords = DataGeneratorsNoSql.generate_strings(10, 8, 16)
    pesels = DataGeneratorsNoSql.generate_pesels(10)
    phones = DataGeneratorsNoSql.generate_phones(10)
    sexes = ['f', 'm']
    usernames = csv_to_list('../data/usernames.csv')

    customers = []

    for i in range(count):
        data = {
            'address': get_random(addresses),
            'date_of_birth': get_random(date_of_births),
            'email': get_random(emails),
            'firstName': get_random(names),
            'lastName': get_random(lastNames),
            'password': get_random(passwords),
            'pesel': get_random(pesels),
            'phone': get_random(phones),
            'sex': get_random(sexes),
            'username': get_random(usernames)
        }

        data = decide_to_remove_property(data, ["address", "date_of_birth", "firstName", "lastName", "pesel", "phone"],
                                         0.5)

        customers.append(data)

    db.customers.insert_many(customers)


def insert_employees(count: int):
    print("insert employees")
    addresses = csv_to_list('../data/addresses.csv')
    date_of_births = DataGeneratorsNoSql.generate_dates(10, "1900-01-01", "2020-01-01")
    employment_dates = DataGeneratorsNoSql.generate_end_dates(date_of_births, 999)
    dismissals_dates = DataGeneratorsNoSql.generate_end_dates(employment_dates, 999)
    emails = csv_to_list('../data/emails.csv')
    names = csv_to_list('../data/Names.csv')
    lastNames = csv_to_list('../data/Surnames.csv')
    passwords = DataGeneratorsNoSql.generate_strings(10, 8, 16)
    pesels = DataGeneratorsNoSql.generate_pesels(10)
    phones = DataGeneratorsNoSql.generate_phones(10)
    positions = csv_to_list('../data/PositionsNames.csv')
    sexes = ['f', 'm']
    usernames = csv_to_list('../data/usernames.csv')

    employees = []

    for i in range(count):
        data = {
            'address': get_random(addresses),
            'date_of_birth': get_random(date_of_births),
            'dismissal_date': get_random(dismissals_dates),
            'email': get_random(emails),
            'employment_date': get_random(employment_dates),
            'firstName': get_random(names),
            'lastName': get_random(lastNames),
            'password': get_random(passwords),
            'pesel': get_random(pesels),
            'phone': get_random(phones),
            'positionName': get_random(positions),
            'sex': get_random(sexes),
            'username': get_random(usernames)
        }
        data = decide_to_remove_property(data, ["address", "date_of_birth", "dismissal_date", "firstName", "lastName",
                                                "pesel",
                                                "phone", ], 0.5)
        employees.append(data)

    db.employees.insert_many(employees)


def insert_cars(count: int):
    print("insert cars")
    countries = list(set(csv_to_list("../data/Countries.csv")))
    brands = csv_to_list("../data/brands.csv")
    vins = generate_vins(1000000)
    dates = genereate_ints(count, 1990, 2020)
    prices = generate_floats(100000, 10000, 500000)
    mileages = genereate_ints(100000, 0, 200000)
    statuses = csv_to_list('../data/CarStatusesTypes.csv')
    capacities = generate_floats(10000, 0, 8)
    powers = genereate_ints(500, 0, 1000)
    torques = genereate_ints(700, 0, 1500)
    engine_cylinder_arrangement = csv_to_list('../data/cylinder_arrangement.csv')
    engine_power_supplies = csv_to_list('../data/CarPowerSuppliesTypes.csv')
    models = list(set(csv_to_list('../data/Models (1).csv')))
    drivetrains = csv_to_list('../data/drivetrains.csv')
    gearbox_types = ['5mt', '6mt', '6at', '7dct', '8at']
    gearbox_ratios = generate_floats(10, 0, 1)
    bodies = csv_to_list('../data/CarBodyTypes.csv')
    doors = [3, 5]
    seats = [2, 4, 5, 7]
    varnish_types = csv_to_list('../data/VarnishTypes.csv')
    varnish_colors = csv_to_list('../data/Colors.csv')
    varnish_codes = csv_to_list('../data/ColorCodes.csv')
    steering_wheels = csv_to_list('../data/steering_wheels.csv')
    equipment_elements_number = genereate_ints(5, 1, 10)
    equipment_names = csv_to_list('../data/CarEquipmentsNames.csv')
    equipment_codes = generate_equipment_codes(count)

    cars = []

    for i in range(count):
        data = {
            "origin_country": get_random(countries),
            "brand": get_random(brands),
            "vin": get_random(vins),
            "price": get_random(prices),
            "production_date": get_random(dates),
            "mileage": get_random(mileages),
            "description": "",
            "status": get_random(statuses),
            "engine": {
                "name": "",
                "capacity": get_random(capacities),
                "power": get_random(powers),
                "torque": get_random(torques),
                "cylinder_arrangement": get_random(engine_cylinder_arrangement),
                "power_supply": get_random(engine_power_supplies),
            },
            "model": {
                "name": get_random(models),
                "description": "",
                "drivetrain": get_random(drivetrains),
                "gearbox": {
                    "type": get_random(gearbox_types),
                    "ratio": get_random(gearbox_ratios),
                },
            },
            "body": {
                "type": get_random(bodies),
                "door_number": get_random(doors),
                "seat_number": get_random(seats),
            },
            "varnish": {
                "name": get_random(varnish_colors),
                "type": get_random(varnish_types),
                "code": get_random(varnish_codes),
            },
            "steering_wheel": get_random(steering_wheels),
            "equipment": list(map(lambda name: {"name": name, "code": get_random(equipment_codes)},
                                  random.choices(equipment_names, k=get_random(equipment_elements_number))))
        }
        cars.append(data)
        if i % 1000 == 0:
            print(i)

    db.cars.insert_many(cars)


def get_payments(count: int):
    amounts = generate_floats(10, 0.0, 500.0)
    payment_dates = generate_dates(count, '1967-1-1', '2000-1-1')
    deadline_dates = generate_end_dates(payment_dates, 40)
    invoice_numbers = [str(x) for x in genereate_ints(10, 0, 1000000)]

    payments_list = []

    for i in range(count):
        data = {
            "amount": get_random(amounts),
            "payment_date": get_random(payment_dates)
        }

        if is_present(0.8):
            data["deadline_date"] = get_random(deadline_dates)

        if is_present(0.8):
            data["invoice_number"] = get_random(invoice_numbers)

        payments_list.append(data)

    return payments_list


def get_car_accessories(count: int):
    names = csv_to_list("../data/AccessoryNameParts.csv")
    registration_numbers = [str(x) for x in genereate_ints(10, 0, 1000000)]
    prices_per_unit = generate_floats(10, 0.0, 500.0)
    amounts = genereate_ints(10, 0, 20)
    accessory_types = csv_to_list("../data/AccesoryTypes.csv")

    car_accessories_list = []

    for i in range(count):
        data = {
            "name": get_random(names),
            "registration_number": pop_random(registration_numbers),
            "price_per_unit": get_random(prices_per_unit),
            "amount": get_random(amounts),
            "accessory_type": get_random(accessory_types)
        }
        car_accessories_list.append(data)

    return car_accessories_list


def get_services(count: int):
    names = csv_to_list("../data/service_names.csv")
    descriptions = ['yearly', 'free', 'varranty']
    prices = generate_floats(10, 0.0, 500.0)

    services_list = []

    for i in range(count):
        data = {
            "name": get_random(names),
            "price": get_random(prices)
        }

        if is_present(0.8):
            data["description"] = get_random(descriptions)

        services_list.append(data)

    return services_list


def insert_orders(count: int):
    print("insert orders")
    numbers = [str(x) for x in genereate_ints(10, 0, 1000000)]
    dates_of_application = generate_dates(count, '1967-1-1', '2020-1-1')
    dates_of_realisation = generate_end_dates(dates_of_application, 40)
    comments = ['lost in delivery', 'unavaliable at the moment', ' delivery from china', 'must be manufactured first']
    order_statuses = csv_to_list("../data/order_statuses.csv")
    # customers = list(db.customers.find())
    # cars = list(db.cars.find())



    orders = []

    for i in range(count):

        if i % 10000 == 0:
            print(i)
            customers = list(db.customers.aggregate(
                [{
                    "$sample":
                        {"size": 10000}}
                ]))

            cars = list(db.cars.aggregate(
                [{
                    "$sample":
                        {"size": 10000}}
                ]))

        data = {
            "number": get_random(numbers),
            "date_of_application": get_random(dates_of_application),
            "order_status": get_random(order_statuses),
            "payments": get_payments(random.randint(0, 5)),
            "car_accessories": get_car_accessories(random.randint(0, 5)),
            "services": get_services(random.randint(0, 5)),
            "customer": get_random(customers)
        }

        if is_present(0.8):
            data["date_of_realisation"] = get_random(dates_of_realisation)

        if is_present(0.8):
            data["comment"] = get_random(comments)

        if is_present(1):
            data["cars"] = get_random(cars)

        orders.append(data)
    db.orders.insert_many(orders)


def insert_test_drives(count: int):
    print("insert test drives")
    start_times = generate_timestamps(count, '2015-1-1 12:00:00', '2022-1-1 12:00:00')
    end_times = generate_end_timestamps(start_times, max_minutes=180)
    comments = ['car crashed', 'driver caused accident', 'custromer didnt attend']

    test_drives = []

    employees = list(db.employees.aggregate(
        [{
            "$sample":
                {"size": 10000}}
        ]))

    cars = list(db.cars.aggregate(
        [{
            "$sample":
                {"size": 10000}}
        ]))
    customers = list(db.customers.aggregate(
        [{
            "$sample":
                {"size": 10000}}
        ]))

    for i in range(count):

        if i % 10000 == 0:
            print(i)
            employees = list(db.employees.aggregate(
                [{
                    "$sample":
                        {"size": 10000}}
                ]))

            cars = list(db.cars.aggregate(
                [{
                    "$sample":
                        {"size": 10000}}
                ]))
            customers = list(db.customers.aggregate(
                [{
                    "$sample":
                        {"size": 10000}}
                ]))

        data = {
            "start_time": start_times[i],
            "end_time": end_times[i],
            "employee": get_random(employees),
            "customer": get_random(customers),
            "car": get_random(cars)
        }
        if random.random() < 0.3:
            data["comments"] = get_random(comments)

        test_drives.append(data)
    db.test_drives.insert_many(test_drives)


insert_customer(800000)
insert_employees(500000)
insert_cars(1000000)
insert_orders(500000)
insert_test_drives(100000)
