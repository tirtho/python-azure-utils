# pyodbc documentation is here - https://github.com/mkleehammer/pyodbc
# Configure your development environment for pyodbc Python development
# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15#windows
# For Windows, you need to install Microsoft ODBC Driver for SQL Server on Windows
# For Linux, install Microsoft ODBC Driver for SQL Server on Linux
# Then
# For Windows, from commandline, install pyodbc - 
# > pip install pyodbc
# For Linux, from termiinal
# > sudo -H pip install pyodbc

import pyodbc
import sys
from datetime import datetime
import random

server = 'tbdemosqldb.database.windows.net'
database = 'TBDemoSqlDB'
driver = '{ODBC Driver 17 for SQL Server}'
# Get the TB_DEMO_SQL_DB_USERNAME and TB_DEMO_SQL_DB_PWD from environment variables
import os
try:
    username = os.environ['TB_DEMO_SQL_DB_USERNAME']
    password = os.environ['TB_DEMO_SQL_DB_PWD']
except Exception as e:
    print('Could not read system environment variables TB_DEMO_SQL_DB_USERNAME & TB_DEMO_SQL_DB_PWD')
    print(e)
    sys.exit(1)

# Connect to database
try:

    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
except pyodbc.Error as dbError:
    print(dbError)
    sys.exit(1)

# Insert row to a table in database
try:
    TIME_NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    aRandomNumber = str(random.randint(1000, 9999))
    # Write one row in table
    cursor.execute("INSERT INTO [RandomNumbers] (time, randomNumber, description) VALUES (?,?,?)", TIME_NOW, aRandomNumber, 'Count-'+aRandomNumber)
    conn.commit()
except pyodbc.Error as insertError:
    print(insertError)
    conn.close()
    sys.exit(1)

# Read back the row added from above
try:
    cursor.execute("SELECT r.time as CreationTime, r.randomNumber as RandomNumber, r.description as Description FROM [dbo].[RandomNumbers] r WHERE r.randomNumber = ?", aRandomNumber)
    row = cursor.fetchone()
    while row:
        print('Listing newly inserted row\n')
        print (str(row[0]) + " || " + str(row[1]) + " || " + str(row[2]))
        row = cursor.fetchone()
except pyodbc.Error as readError:
    print(readError)
    conn.close()
    sys.exit(1)

# Closing connection before exiting
try:
    conn.close()
    print("Database connection closed")
except pyodbc.Error as closingError:
    print(closingError)

sys.exit()

