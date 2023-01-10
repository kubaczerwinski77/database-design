import csv
import random
import uuid
from datetime import timedelta, datetime


def generate_registration_numbers(count):
    alphabet = "ABCDEFGHIJKLMNOPRSTUWYZ1234567890"
    s = set()
    while (len(s) < count):
        s.add(''.join(random.sample(alphabet, n := random.randrange(1, 3))
              )+' '+''.join(random.sample(alphabet, 8-n)))
    return list(s)


def generate_floats(count, min, max):
    return [round(random.uniform(min, max), 2) for x in range(count)]


def genereate_ints(count, min, max):
    return [random.randrange(min, max) for x in range(count)]

def generate_ints_unique(count, min, max):
    s = set()
    while len(s)<=count:
        s.add(random.randrange(min, max))
    return list(s)



def generate_strings(length, min, max):
    alphabet = "ABCDEFGHIJKLMNOPRSTUWYZ1234567890"
    s = set()
    while (len(s) < length):
        s.add(''.join(random.sample(alphabet, random.randrange(min, max))))
    return list(s)


def generate_timestamps(count, start, stop):
    start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    stop = datetime.strptime(stop, "%Y-%m-%d %H:%M:%S")
    return [(start + timedelta(seconds=random.randrange(0, (stop - start).total_seconds()))) for x in
            range(count)]

def generate_end_timestamps(list_start_timestamps, max_minutes):
    list_start_timestamps = list(
        map(lambda elem: datetime.strptime(elem, "%Y-%m-%dT%H:%M:%S"), list_start_timestamps.copy()))
    return [(list_start_timestamps[x] + timedelta(seconds=random.randrange(0, max_minutes * 60))) for x in
            range(len(list_start_timestamps))]

def generate_vins(Count):
    alphabet = "ABCDEFGHIJKLMNOPRSTUWYZ1234567890"
    s = set()
    while (len(s) < Count):
        s.add(''.join(random.sample(alphabet,17)))
    return list(s)

def generate_dates(count, start, stop):
    start = datetime.strptime(start, "%Y-%m-%d")
    stop = datetime.strptime(stop, "%Y-%m-%d")
    return [(start+timedelta(days=random.randrange(0, (stop-start).days))) for x in range(count)]

def generate_end_dates(list_start_dates, max_days):
    list_start_dates = list(map(lambda elem : datetime.strptime(elem, "%Y-%m-%dT%H:%M:%S"), list_start_dates.copy()))
    return [(list_start_dates[x]+timedelta(days=random.randrange(0, max_days))) for x in range(len(list_start_dates))]

def generate_phones(count):
    return  [str(random.randrange(100000000,999999999)) for x in range(count)]

def generate_pesels(count):
    return [str(random.randrange(10000000000,99999999999)) for x in range(count)]

def generate_equipment_codes(count):
    codes = set()
    while(len(codes)<count):
        codes.add(random.randrange(1000,1000000))
    return list(codes)





