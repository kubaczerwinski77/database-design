from pymongo import MongoClient
import csv
from nosql.DataGeneratorsNoSql import *


def get_random(list_of_values):
    return random.choice(list_of_values)


def pop_random(list_of_values):
    return list_of_values.pop(random.randrange(len(list_of_values)))


def csv_to_list(filename: str):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        return [item for sublist in reader for item in sublist]


client = MongoClient("mongodb+srv://car-salon:LmrVociSmTXvTjFQ@cluster0.3tezxec.mongodb.net/test")
db = client["car-salon-Pawel"]


def insert_cars(count: int):
    countries = list(set(csv_to_list("../../data/Countries.csv")))
    brands = csv_to_list("../../data/brands.csv")
    vins = generate_vins(100000)
    dates = genereate_ints(count, 1990, 2020)
    prices = generate_floats(100000, 10000, 500000)
    mileages = genereate_ints(100000, 0, 200000)
    statuses = csv_to_list('../../data/CarStatusesTypes.csv')
    capacities = generate_floats(10000, 0, 8)
    powers = genereate_ints(500, 0, 1000)
    torques = genereate_ints(700, 0, 1500)
    engine_cylinder_arrangement = csv_to_list('../../data/cylinder_arrangement.csv')
    engine_power_supplies = csv_to_list('../../data/CarPowerSuppliesTypes.csv')
    models = list(set(csv_to_list('../../data/Models (1).csv')))
    drivetrains = csv_to_list('../../data/drivetrains.csv')
    gearbox_types = ['5mt', '6mt', '6at', '7dct', '8at']
    gearbox_ratios = generate_floats(10, 0, 1)
    bodies = csv_to_list('../../data/CarBodyTypes.csv')
    doors = [3, 5]
    seats = [2, 4, 5, 7]
    varnish_types = csv_to_list('../../data/VarnishTypes.csv')
    varnish_colors = csv_to_list('../../data/Colors.csv')
    varnish_codes = csv_to_list('../../data/ColorCodes.csv')
    steering_wheels = csv_to_list('../../data/steering_wheels.csv')
    equipment_elements_number = genereate_ints(5, 1, 10)
    equipment_names = csv_to_list('../../data/CarEquipmentsNames.csv')

    equipment_codes = generate_equipment_codes(count)

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

        cars_id = db.cars.insert_one(data).inserted_id
        print(cars_id)


insert_cars(10)
