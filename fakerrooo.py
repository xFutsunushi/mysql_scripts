import csv
from faker import Faker
import random
import mariadb
import sys
import time

def generate_employee_data(num_records):
    fake = Faker()
    with open('employee_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #writer.writerow(['Name', 'Age', 'Address', 'Phone', 'Email', 'Salary'])
        for i in range(num_records):
            name = fake.name()
            age = random.randint(18, 65)
            address = fake.address()
            phone = fake.phone_number()
            email = fake.email()
            job = fake.job()
            salary = random.randint(50000, 150000)
            #writer.writerow([name, age, address, phone, email, salary])
            writer.writerow([name, age, email, salary, job])


num_records = 1000000
generate_employee_data(num_records)

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="db_user",
        password="super_secret",
        host="localhost",
        port=3306,
        database="people"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
#print(cur)
cur.execute('DROP TABLE IF EXISTS employee;')
time.sleep(2)
cur.execute('CREATE TABLE IF NOT EXISTS employee (name VARCHAR(255) NULL, age INT(255) NULL, email VARCHAR(255) NULL, salary INT(10) NULL, job VARCHAR(255) NULL)')

cur.execute('SHOW TABLES')
for i in cur:
    print(i)

cur.execute('DESC employee')
for i in cur:
    print(i)

with open("employee_data.csv", 'r') as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
        time.sleep(1)
        cur.execute('INSERT INTO employee (name,age,email, salary, job) VALUES (%s,%s,%s, %s, %s)',row)
        conn.commit()
