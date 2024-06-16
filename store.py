#!/usr/bin/python3

import mysql.connector

# Establish a connection to the local MySQL server
mydb = mysql.connector.connect(
    host="localhost",
    user="whitney",
    port="0708"
)

# Create a cursor object
cursor = mydb.cursor()

# Execute a query
cursor.execute("SHOW DATABASES")

# Fetch and print the results
for db in cursor:
    print(db)


