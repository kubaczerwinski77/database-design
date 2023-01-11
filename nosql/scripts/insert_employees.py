import csv
from nosql import DataGeneratorsNoSql
from pymongo import MongoClient
import random


def get_random(list_of_values):
    return random.choice(list_of_values)


def pop_random(list_of_values):
    return list_of_values.pop(random.randrange(len(list_of_values)))

def csv_to_list(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        return [item for sublist in reader for item in sublist]

def decide_to_remove_property(data: dict, properties: list[str], probability: float):
    for property in properties:
        if random.random() > probability:
            del data[property]
    return data


# create connection
client = MongoClient("mongodb+srv://car-salon:LmrVociSmTXvTjFQ@cluster0.3tezxec.mongodb.net/test")
db = client["car-salon-kubaS"]
employees = db.employees

# #
# for employee in employees.find():
#     pprint(employee)

# {'_id': ObjectId('63a3931d55919b8b57b9640e'),
#  'address': 'd21 pwr',
#  'date_of_birth': datetime.datetime(2014, 3, 1, 8, 0),
#  'dismissal_date': datetime.datetime(2014, 3, 1, 8, 0),
#  'email': 'emp1@carsalon.com',
#  'employment_date': datetime.datetime(2014, 3, 1, 8, 0),
#  'firstName': 'janusz',
#  'lastName': 'kolodziej',
#  'password': 'emp1',
#  'pesel': '01291301566',
#  'phone': '123123123',
#  'positionName': 'gornik',
#  'sex': 'm',
#  'username': 'emp1'}
#
# Process finished with exit code 0




def insert_employees(count: int):
    addresses = csv_to_list('../../data/addresses.csv')
    date_of_births = DataGeneratorsNoSql.generate_dates(10, "1900-01-01", "2020-01-01")
    employment_dates = DataGeneratorsNoSql.generate_end_dates(date_of_births, 999)
    dismissals_dates = DataGeneratorsNoSql.generate_end_dates(employment_dates, 999)
    emails = csv_to_list('../../data/emails.csv')
    names = csv_to_list('../../data/Names.csv')
    lastNames = csv_to_list('../../data/Surnames.csv')
    passwords = DataGeneratorsNoSql.generate_strings(10, 8, 16)
    pesels = DataGeneratorsNoSql.generate_pesels(10)
    phones= DataGeneratorsNoSql.generate_phones(10)
    positions=csv_to_list('../../data/PositionsNames.csv')
    sexes = ['f','m']
    usernames = csv_to_list('../../data/usernames.csv')
   # print(date_of_births)
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
        data = decide_to_remove_property(data,["address","date_of_birth","dismissal_date","firstName","lastName","pesel",
                                               "phone",],0.5)
        employee_id = employees.insert_one(data).inserted_id
        if i%100==0:
            print(i)


insert_employees(20000)
