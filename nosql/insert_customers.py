import csv
from pprint import pprint
import DataGeneratorsNoSql
from pymongo import MongoClient
import random
import datetime


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
db = client["car-salon-kubaS"]
customers = db.customers


for customer in customers.find():
    pprint(customer)


# {'_id': ObjectId('63a3931e55919b8b57b9640f'),
#  'address': 'pwr',
#  'date_of_birth': datetime.datetime(2014, 3, 1, 8, 0),
#  'email': 'tomasz@gollob',
#  'firstName': 'Tomasz',
#  'lastName': 'Gollob',
#  'password': 'zmarzliklove',
#  'pesel': '01231301566',
#  'phone': '1234557788',
#  'sex': 'f',
#  'username': 'tomaszG'}
def insert_customer(count: int):
    addresses = csv_to_list('../data/addresses.csv')
    date_of_births = DataGeneratorsNoSql.generate_dates(10, "1900-01-01", "2020-01-01")
    emails = csv_to_list('../data/emails.csv')
    names = csv_to_list('../data/Names.csv')
    lastNames = csv_to_list('../data/Surnames.csv')
    passwords = DataGeneratorsNoSql.generate_strings(10,8,16)
    pesels = DataGeneratorsNoSql.generate_pesels(10)
    phones= DataGeneratorsNoSql.generate_phones(10)
    sexes = ['f','m']
    usernames = csv_to_list('../data/usernames.csv')
   # print(date_of_births)
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
        customer_id= customers.insert_one(data).inserted_id
        print(customer_id)


insert_customer(10)
