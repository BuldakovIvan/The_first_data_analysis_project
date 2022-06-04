# a table with personal data of employees is created here

import sqlite3 as sq
import random as rd
import datetime as dt


data_base_name = 'Employee_Data.db'
table_one = "2009_v.1"
table_two = "2009_v.2"
table_three = "personal_data"

with sq.connect(data_base_name) as con:
    cur = con.cursor()

    # create a list of names from an existing table in the database
    cur.execute(f'''select Name from "{table_one}"
                    group by Name''')

    fio = cur.fetchall()

    # create a list of id numbers
    id_num = [n for n in range(1000, len(fio) + 3000)]
    rd.seed(1)
    rd.shuffle(id_num)
    print(id_num)

    # create a table for personal data of employees
    cur.execute(f'''drop table if exists "{table_three}"''')

    cur.execute(f'''create table if not exists "{table_three}"
                    (
                    "Personnel number" integer not null primary key,
                    "Name" text not null,
                    "Date of birth" integer not null,
                    "Sex" varchar(8) not null
                    )''')

    # create data for the table with personal data of employees
    max_date = dt.date(1990, 12, 31) - dt.date(1949, 1, 1)
    for i, s in enumerate(fio):
        b_date = str(dt.date(1990, 12, 31) - dt.timedelta(days=rd.randint(0, max_date.days)))  # date of birth
        sex = "М"
        id = id_num[i]
        name = str(*s)
        print(id, name, b_date, sex)

        # fill in the table with personal data of employees
        cur.execute(f'''insert into "{table_three}" values (?, ?, ?, ?)''', (id, name, b_date, sex))
