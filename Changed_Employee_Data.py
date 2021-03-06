# creating new employee data based on initial data  (third step)

import sqlite3 as sq
import pandas as pd


data_base_name = 'Employee_Data.db'
table_one = "2009_v.1"
table_two = "2009_v.2"
table_three = "personal_data"

with sq.connect(data_base_name) as con:
    cur = con.cursor()

    # creating a table for new employee data
    cur.execute(f'''drop table if exists "{table_two}"''')

    cur.execute(f'''create table if not exists "{table_two}"
                    (
                    "Personnel number" integer not null,
                    "Name" text not null,
                    "Date of birth" integer not null,
                    "Sex" varchar(8) not null,
                    Profession VARCHAR(256) not null,
                    Rank integer not null default 3,
                    Equipment text not null,
                    "Harmfulness (score)" integer not null default 0,
                    "Production volume" integer not null default 0,
                    Month text not null,
                    Income integer not null default 0
                    )''')

    # collect data for a new table by joining data from existing tables
    cur.execute(f'''select 
                        "Personnel number",
                        "{table_one}".Name,
                        "Date of birth",
                        "Sex",
                        Profession,
                        Rank,
                        Equipment,
                        "Harmfulness (score)",
                        "Production volume",
                        Month,
                        Income                    
                    from "{table_one}" 
                    join "{table_three}"
                    on "{table_one}".Name = "{table_three}".Name''')

    tmp_data = cur.fetchall()

    cur.executemany(f'''insert into "{table_two}" values ({"?, " * 10 + "?"})''', tmp_data)

    # for several professions, replace men with women
    cur.execute(f'''SELECT "Personnel number", Name, Sex 
                        from "{table_two}" 
                        where Profession in
                        (
                        "?????????????????? ???????????????? ?????????????? ??????????????????",
                        "???????????????? ?????????? ????????????????????",
                        "??????????????"
                        )
                        GROUP by "Personnel number"
                        ORDER by Profession
                        ''')

    for_change = cur.fetchall()

    # add the letter "a" to the male surname at the end to turn it into a female one
    for ind, val in enumerate(for_change):
        if ind % 5 != 0:
            tmp = val[1].split()
            name = tmp[0] + "?? " + tmp[1] + " " + tmp[2]

            cur.execute(f'''update "{table_two}"
                            set Name = "{name}", Sex = "??"
                            where "Personnel number" = {val[0]}
                            ''')

    # creating an excel-file with new employees data
    new_data = pd.read_sql(f'''select * from "{table_two}"''', con)
    new_data.to_excel('New_Employees_Data.xlsx', sheet_name='????????????', index=False)
