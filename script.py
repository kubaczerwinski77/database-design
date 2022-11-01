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
    uuids=set()
    while(len(uuids)<count):
        uuids.add(str(uuid.uuid4()))
    return list(uuids)



uuids= generate_uuids(3)
names=["318i",'316i','320i']
descriptions=['Small city Car']
FK_car_drivetrains = get_foreign_keys('CarDrivetrains',cur)


statements=generateSql(3,'Models',id=uuids,UNIQUE_name=names,description=descriptions,fk_cardrivetrains=FK_car_drivetrains)
for statement in statements:
    cur.execute(statement)


print(statements)

conn.commit()
cur.close()
conn.close()
