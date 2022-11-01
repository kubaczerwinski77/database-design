import csv
import random
import uuid
def generate_registration_numbers(count):
    alphabet="ABCDEFGHIJKLMNOPRSTUWYZ1234567890"
    s = set()
    while(len(s)<count):
        s.add(''.join(random.sample(alphabet,n:=random.randrange(1,3)))+' '+''.join(random.sample(alphabet,8-n)))
    return s

def generate_prices(count,min,max):
    if(min>0):
        return [round(random.uniform(min, max), 2) for x in range(count)]


def generate_uuids(count):
    uuids=set()
    while(len(uuids)<count):
        uuids.add(str(uuid.uuid4()))
    return list(uuids)





