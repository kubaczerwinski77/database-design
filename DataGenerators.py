import csv
import random
import uuid
from datetime import timedelta


def generate_registration_numbers(count):
    alphabet="ABCDEFGHIJKLMNOPRSTUWYZ1234567890"
    s = set()
    while(len(s)<count):
        s.add(''.join(random.sample(alphabet,n:=random.randrange(1,3)))+' '+''.join(random.sample(alphabet,8-n)))
    return list(s)

def generate_floats(count, min, max):
        return [round(random.uniform(min, max), 2) for x in range(count)]
def generate_ints(count,min,max):
    return [random.randrange(min,max)for x in range(count)]

def generate_strings(length,min,max):
    alphabet = "ABCDEFGHIJKLMNOPRSTUWYZ1234567890"
    s = set()
    while (len(s) < length):
        s.add(''.join(random.sample(alphabet,random.randrange(min,max))))
    return list(s)

def generate_timestamps(count,start,stop):
        return [f"{(random.randrange(start, stop))}-{random.randrange(1, 12)}-{random.randrange(1, 27)} {random.randrange(1,24)}:{random.randrange(1,60)}:{random.randrange(1,60)}" for x in range(count)]

def generate_vins(Count):
    alphabet = "ABCDEFGHIJKLMNOPRSTUWYZ1234567890"
    s = set()
    while (len(s) < Count):
        s.add(''.join(random.sample(alphabet,17)))
    return list(s)

def generate_dates(count,start,stop):
    return [f"{(random.randrange(start,stop))}-{random.randrange(1,12)}-{random.randrange(1,27)}" for x in range(count)]

def generate_phones(count):
    return  [str(random.randrange(100000000,999999999)) for x in range(count)]

def generate_pesels(count):

    return [str(random.randrange(10000000000,99999999999)) for x in range(count)]

def generate_uuids(count):
    uuids=set()
    i=0
    while(len(uuids)<count):
        uuids.add(str(uuid.uuid4()))
        i+=1
        print(i)
    return list(uuids)

def generate_equipment_codes(count):
    codes = set()
    while(len(codes)<count):
        codes.add(random.randrange(1000,1000000))
    return list(codes)





