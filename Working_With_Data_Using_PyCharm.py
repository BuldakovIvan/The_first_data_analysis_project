import sqlite3 as sq
import pandas as pd
import matplotlib.pyplot as plt


data_base_name = 'Employee_Data.db'
table_one = "2009_v.1"
table_two = "2009_v.2"
table_three = "personal_data"

with sq.connect(data_base_name) as con:
    cur = con.cursor()

    # making a selection from the database to create a table 'Cтруктура работников цеха по половому признаку'
    gender_structure = pd.read_sql(f'''SELECT Sex, count(Sex) as Amount FROM
                            (
                            SELECT "Personnel number", Sex
                            from "{table_two}"
                            GROUP by "Personnel number"
                            )
                        GROUP by Sex''', con)

    # data on the number of men and women for the pie chart:
    vals = gender_structure['Amount'].tolist()

    # data for pie chart legend:
    labels = ['Женщины' if s == 'Ж' else 'Мужчины' for s in gender_structure['Sex'].tolist()]

    # pie chart settings:
    my = plt.pie(vals,
                 colors=('violet', 'dodgerblue'),
                 startangle=-45,
                 autopct=lambda x: f'{round(x, 1)}%\n({int(round(x * sum(vals) / 100, 0))} чел.)',
                 textprops=dict(color="black", size=10, weight='bold')
                 )
    plt.title('Cтруктура работников цеха\nпо половому признаку',
              size=12,
              weight='bold',
              )

    plt.legend(labels, bbox_to_anchor=(0.85, 0.95))

    plt.show()

    print(vals)
    print(labels)


