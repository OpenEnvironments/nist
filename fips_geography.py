#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Load the NAICS file into a table
Depends on the pgdata program with db_query function
"""

import csv
import time
start = time.perf_counter()

HOST = 'yogi'
PORT = '5432'
DBNAME = 'openenvironments'
USER = 'michael'
PASS = 'b3arclaw'

r = change_query(HOST, PORT, DBNAME, USER, PASS,
        """
        DROP TABLE IF EXISTS fips_geography
        """)

r = change_query(HOST, PORT, DBNAME, USER, PASS,
        """
        CREATE 
        UNLOGGED
        TABLE fips_geography
        (
        SummaryLevel text,
        StateCode text,
        CountyCode text,
        CountySubdivisionCode text,
        PlaceCode text,
        ConsolidatedCityCode text,
        AreaName text
        )        
        TABLESPACE  disk1
        """)

import csv
fields = [
    'SummaryLevel',
    'StateCode',
    'CountyCode',
    'CountySubdivisionCode',
    'PlaceCode',
    'ConsolidatedCityCode',
    'AreaName'
]
rows = []

with open('D:/Open Environments/data/census/fips/all-geocodes-v2019.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for i in range(5):    # skip 5 header rows
        skipper = next(csvreader)
        print('skipping')
    r = 0
    for row in csvreader:
        r += 1
        print('row',r)
        rows.append(row)
    print("Total no. of rows: %d"%(csvreader.line_num))

# sometimes a csv has extra columns so rows need to be trimmed
newrows = []
for row in csvreader:
    newrows.append(row[0:7])

from pandas import read_excel
my_sheet = 'all-geocodes-v2019'
file_name = 'D:/Open Environments/data/census/fips/all-geocodes-v2019.xlsx'
df = read_excel(file_name, sheet_name = my_sheet)
df = df.iloc[5:]
print(df.head()) # shows headers with top 5 rows

mute = bulk_load(HOST,PORT,DBNAME,USER,PASS,
    """
    INSERT INTO fips_geography (
        SummaryLevel,
        StateCode,
        CountyCode,
        CountySubdivisionCode,
        PlaceCode,
        ConsolidatedCityCode,
        AreaName
    ) VALUES (%s,%s,%s,%s,%s,%s,%s)
    """,
    df)




