from pymongo import MongoClient
import random


def get_random(list_of_values):
    return random.choice(list_of_values)


def pop_random(list_of_values):
    return list_of_values.pop(random.randrange(len(list_of_values)))


# create connection
client = MongoClient("mongodb+srv://car-salon:LmrVociSmTXvTjFQ@cluster0.3tezxec.mongodb.net/test")
db = client["car-salon-kubaS"]
testNames = db.testNames


def insert_customer(count: int):
    names = ['kuba', 'jakub', 'wojtek', 'pawel']
    surnames = ['Samulski', 'Kluska', 'Dominiak', 'Czerwinski']

    for i in range(count):
        data = {
            "Name": get_random(names),
            "Surname": get_random(surnames)
        }
        test_name_id = testNames.insert_one(data).inserted_id
        print(test_name_id)


insert_customer(4)
