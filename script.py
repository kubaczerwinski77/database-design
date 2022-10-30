import random

import psycopg2
import uuid

#connection to database
conn = psycopg2.connect("dbname=test1 user=postgres password=admin")
cur= conn.cursor()

def get_foreign_keys(tablename,cursor):
    cursor.execute(f"""SELECT id from {tablename}""")
    data = cursor.fetchall()
    uuids = []
    for row in data:
        uuids.append(row[0])
    return uuids


def get_random(list):
    return random.choice(list)

def pop_random(list):
    return list.pop(random.randrange(len(list)))


def add_value(column, values_list):

    if (column[:7]== 'UNIQUE_'):
        val = pop_random(values_list)
        if type(val) is int:
            return str(val)
        return f"""'{val}'"""

    val=get_random(values_list)
    if type(val) is int:
        return str(val)
    return f"""'{val}'"""



def generateSql(count,table_name,**kwargs):
    # kwargs are in form of column_name: list_of_values to be chosen at random and inserted ie. drivetrain:['rwd','fwd']
    # if column should have only unique values then name the column UNIQUE_column_name such as UNIQUE_type
    sql_list=[]
    for i in range(count):
        sql=f"""INSERT INTO {table_name} ("""
        columns=list(kwargs)

        for column in columns:
            if(column[:7]=='UNIQUE_'):
                column = column[7:]
            sql+=column+','
        sql = sql[:-1]

        sql+=') VALUES('

        for key,item in kwargs.items():
            sql+=add_value(key,item)+','
        sql = sql[:-1]
        sql+=');'
        sql_list.append(sql)
    return sql_list


def generate_uuids(count):
    uuids=[]
    for i in range(count):
        uuids.append(uuid.uuid4())
    return uuids

uuids= generate_uuids(10)
types=['rwd','fwd','4wd']
test_ints = [1,2,3,4,5]


statements=generateSql(4,'Car_drivetrains',id=uuids,type=types)
for statement in statements:
    cur.execute(statement)


print(statements)

conn.commit()
cur.close()
conn.close()
