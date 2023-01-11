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
db = client["car_salon"]
test_drives = db["test-drives"]
customers_collection = db["customers"]
employees_collection = db["employees"]
cars_collection = db["cars"]


def insert_test_drives(count: int):
    start_times = gen.generate_timestamps(count, '2015-1-1 12:00:00', '2022-1-1 12:00:00')
    end_times = gen.generate_end_timestamps(start_times, max_minutes=180)
    employees = list(employees_collection.find())
    customers = list(customers_collection.find())
    cars = list(cars_collection.find())
    comments = ['car crashed', 'driver caused accident', 'custromer didnt attend']

    for i in range(count):
        data = {
            "start_time": start_times[i],
            "end_time": end_times[i],
            "employee": get_random(employees),
            "customer": get_random(customers),
            "car": get_random(cars),
        }
        if random.random() < 0.3:
            data["comments"] = get_random(comments)

        test_name_id = test_drives.insert_one(data).inserted_id
        print(test_name_id)


insert_test_drives(10)
