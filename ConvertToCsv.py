import csv

l1 = []
with open('data/Models.csv','r+',newline='')as f:
    reader = csv.reader(f)
    for row in range(1000):
        print(row[0])
        l1.append([row[0]])


with open('data/Models.csv','w',newline='') as f1:
    writer = csv.writer(f1)
    writer.writerows(l1)



