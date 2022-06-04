# creating the initial database from the excel-file here

import pandas as pd
import sqlite3 as sq


data_base_name = 'Employee_Data.db'
table_one = "2009_v.1"
table_two = "2009_v.2"
table_three = "personal_data"

# read data from excel-file:
data = pd.read_excel('Initial_Employees_Data.xlsx', sheet_name=0, header=0)

column_name = data.columns


# changing the format of the data in the cells for correct entry into the database:
data = data.astype({'Месяц': 'str', 'Доход': 'int'})


# create database with initial data of employee:
with sq.connect(data_base_name) as con:
    cur = con.cursor()

    cur.execute(f'''drop table if exists "{table_one}"''')

    cur.execute(f'''create table if not exists "{table_one}"
                    (
                    Name text not null,
                    Month text not null,
                    Profession VARCHAR(256) not null,
                    Rank integer not null default 3,
                    Equipment text not null,
                    "Harmfulness (score)" integer not null default 0,
                    "Production volume" integer not null default 0,
                    Income integer not null default 0
                    )''')

    cur.executemany(f'''insert into "{table_one}" values (?, ?, ?, ?, ?, ?, ?, ?)''', data.values)
