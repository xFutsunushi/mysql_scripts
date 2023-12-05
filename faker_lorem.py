import csv
from faker import Faker
import random
import mariadb
import sys
import time


def generate_lorem_data(num_records):
    fake = Faker()
    with open('lorem_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #writer.writerow(['Name', 'Age', 'Address', 'Phone', 'Email', 'Salary'])
        for i in range(num_records):
            lorem = fake.paragraph(nb_sentences=5, variable_nb_sentences=False)
            writer.writerow([lorem])

num_records = 100000
generate_lorem_data(num_records)


# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="user",
        password="secret",
        host="host",
        port=3307,
        database="people"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS lorem;')
time.sleep(2)
cur.execute('CREATE TABLE IF NOT EXISTS lorem (lorem VARCHAR(16383) NULL)')

with open("lorem_data.csv", 'r') as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
        time.sleep(1)
        cur.execute('INSERT INTO lorem (lorem) VALUES (%s)',row)
        conn.commit()
