from pymongo import MongoClient
import random
import csv
import DataGeneratorsNoSql as gen


def get_random(list_of_values):
    return random.choice(list_of_values)


def pop_random(list_of_values):
    return list_of_values.pop(random.randrange(len(list_of_values)))


def csv_to_list(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        return [item for sublist in reader for item in sublist]


# create connection
client = MongoClient("mongodb+srv://car-salon:LmrVociSmTXvTjFQ@cluster0.3tezxec.mongodb.net/test")
db = client["car-salon-Pawel"]
orders = db.orders


def get_payments(count: int):
    amount = gen.generate_floats(10, 0.0, 500.0)
    payment_date = gen.generate_dates(count, '1967-1-1', '2000-1-1')
    deadline_date = gen.generate_end_dates(payment_date, 40)
    invoice_number = [str(x) for x in gen.genereate_ints(10, 0, 1000000)]

    payments_list = []

    for i in range(count):
        data = {
            "amount": get_random(amount),
            "deadline_date": get_random(deadline_date),
            "payment_date": get_random(payment_date),
            "invoice_number": get_random(invoice_number)
        }
        payments_list.append(data)

    return payments_list


def get_car_accessories(count: int):
    name = csv_to_list("../data/AccessoryNameParts.csv")
    registration_number = [str(x) for x in gen.genereate_ints(10, 0, 1000000)]
    price_per_unit = gen.generate_floats(10, 0.0, 500.0)
    amount = gen.genereate_ints(10, 0, 20)
    accessory_type = csv_to_list("../data/AccesoryTypes.csv")

    car_accessories_list = []

    for i in range(count):
        data = {
            "name": get_random(name),
            "registration_number": get_random(registration_number),
            "price_per_unit": get_random(price_per_unit),
            "amount": get_random(amount),
            "accessory_type": get_random(accessory_type)
        }
        car_accessories_list.append(data)

    return car_accessories_list


def get_services(count: int):
    name = csv_to_list("../data/service_names.csv")
    description = ['yearly', 'free', 'varranty']
    price = gen.generate_floats(10, 0.0, 500.0)

    services_list = []

    for i in range(count):
        data = {
            "name": get_random(name),
            "description": get_random(description),
            "price": get_random(price),
        }
        services_list.append(data)

    return services_list


def insert_orders(count: int):
    number = [str(x) for x in gen.genereate_ints(10, 0, 1000000)]
    date_of_application = gen.generate_dates(count, '1967-1-1', '2000-1-1')
    date_of_realisation = gen.generate_end_dates(date_of_application, 40)
    comment = ['lost in delivery', 'unavaliable at the moment', ' delivery from china', 'must be manufactured first']
    order_status = csv_to_list("../data/order_statuses.csv")
    payments = get_payments(10)
    car_accessories = get_car_accessories(10)
    services = get_services(10)
    cars = [] #TO DO
    customer = list(db.customers.find())

    for i in range(count):
        data = {
            "number": get_random(number),
            "date_of_application": get_random(date_of_application),
            "date_of_realisation": get_random(date_of_realisation),
            "comment": get_random(comment),
            "order_status": get_random(order_status),
            "payments": payments,
            "car_accessories": car_accessories,
            "services": services,
            "customer": get_random(customer)
        }
        test_name_id = orders.insert_one(data).inserted_id
        print(test_name_id)


insert_orders(10)
