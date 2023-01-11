from pymongo import MongoClient
import random
import csv
from nosql import DataGeneratorsNoSql as gen


def get_random(list_of_values):
    return random.choice(list_of_values)


def pop_random(list_of_values):
    return list_of_values.pop(random.randrange(len(list_of_values)))


def csv_to_list(filename: str):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        return [item for sublist in reader for item in sublist]


def is_present(probability: float):
    return probability > random.uniform(0, 1)


# create connection
client = MongoClient("mongodb+srv://car-salon:LmrVociSmTXvTjFQ@cluster0.3tezxec.mongodb.net/test")
db = client["car-salon-Pawel"]


def get_payments(count: int):
    amounts = gen.generate_floats(10, 0.0, 500.0)
    payment_dates = gen.generate_dates(count, '1967-1-1', '2000-1-1')
    deadline_dates = gen.generate_end_dates(payment_dates, 40)
    invoice_numbers = [str(x) for x in gen.genereate_ints(10, 0, 1000000)]

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
    names = csv_to_list("../../data/AccessoryNameParts.csv")
    registration_numbers = [str(x) for x in gen.genereate_ints(10, 0, 1000000)]
    prices_per_unit = gen.generate_floats(10, 0.0, 500.0)
    amounts = gen.genereate_ints(10, 0, 20)
    accessory_types = csv_to_list("../../data/AccesoryTypes.csv")

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
    names = csv_to_list("../../data/service_names.csv")
    descriptions = ['yearly', 'free', 'varranty']
    prices = gen.generate_floats(10, 0.0, 500.0)

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
    numbers = [str(x) for x in gen.genereate_ints(10, 0, 1000000)]
    dates_of_application = gen.generate_dates(count, '1967-1-1', '2000-1-1')
    dates_of_realisation = gen.generate_end_dates(dates_of_application, 40)
    comments = ['lost in delivery', 'unavaliable at the moment', ' delivery from china', 'must be manufactured first']
    order_statuses = csv_to_list("../../data/order_statuses.csv")
    cars = list(db.cars.find())
    customers = list(db.customers.find())

    for i in range(count):
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

        if is_present(0.3):
            data["cars"] = get_random(cars)

        test_name_id = db.orders.insert_one(data).inserted_id
        print(test_name_id)


insert_orders(10)
