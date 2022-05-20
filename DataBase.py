import pandas as pd
import os
import psycopg2

database = psycopg2.connect(database='Sobol', user='postgres', password=' ', host='127.0.0.1', port=5432)
database_cursor = database.cursor()

"""
Запросы на создание бд 

create table Category(id serial, name varchar, primary key (id));

create table Sub_category(id serial, name varchar, category_id int, primary key (id),
 foreign key (category_id) references category);

create table Goods (id serial, name varchar, sub_category_id int, rating float, primary key (id), foreign key (sub_category_id) references Sub_category);

create table Properties (id serial, name varchar, value varchar,goods_id int, primary key (id), foreign key (goods_id) references Goods);

create table Client (login varchar, password varchar, name varchar, surname varchar, primary key (login));

create table Evaluations (id serial, value float, client_login varchar, goods_id int, primary key (id),
foreign key (goods_id) references Goods, foreign key (client_login) references Client);

create table Cart (id serial, client_login varchar, status varchar, date_of_creation date,primary key (id),
 foreign key (client_login) references Client);

create table Goods_in_cart (id serial, goods_id int, cart_id int, primary key (id),
foreign key (goods_id) references Goods, foreign key (cart_id) references Cart);
"""

"""
Заполнение бд

for filename in os.listdir("Товары"):
    data = pd.read_excel(f'Товары/' + filename, header=None)
    database_cursor.execute(f"Select id from category where name = ('{str(data[0][1]).strip()}')")
    category_id = -1
    for row in database_cursor:
        if row is not None:
            category_id = row[0]
    if category_id == -1:
        database_cursor.execute(f"INSERT INTO category (name) VALUES ('{str(data[0][1]).strip()}')")
        database.commit()
        database_cursor.execute(f"Select id from category where name = ('{str(data[0][1]).strip()}')")
        for cat_id in database_cursor:
            category_id = cat_id[0]

    database_cursor.execute(f"Select id from Sub_category where name = ('{str(data[0][2]).strip()}')")
    sub_category_id = -1
    for row in database_cursor:
        if row is not None:
            sub_category_id = row[0]
    if sub_category_id == -1:
        database_cursor.execute(f"INSERT INTO Sub_category (name, category_id) VALUES "
                                f"('{str(data[0][2]).strip()}', '{category_id}')")
        database.commit()
        database_cursor.execute(f"Select id from Sub_category where name = ('{str(data[0][2]).strip()}')")
        for cat_id in database_cursor:
            sub_category_id = cat_id[0]

    print("Len ", len(data))
    for i in range(3, len(data)):
        print(data[0][i])
    print(data[0][2])  # subcategory
    print('data', data)
    print(data.shape[1] - 1)  # Количество столбцов

    for i in range(3, len(data)):

        database_cursor.execute(f"Select id from goods where name = ('{str(data[0][i]).strip()}')")
        goods_id = -1
        for row in database_cursor:
            if row is not None:
                goods_id = row[0]
        else:
            print(data[0][i])
            database_cursor.execute(f"INSERT INTO goods (name, sub_category_id)"
                                    f" VALUES ('{str(data[0][i]).strip()}', '{sub_category_id}')")
            database.commit()

            database_cursor.execute(f"Select id from goods where name = ('{str(data[0][i]).strip()}')")
            for row in database_cursor:
                goods_id = row[0]
            for j in range(1, data.shape[1]):
                print(data[j][2])
                print(data[j][i])
                database_cursor.execute(f"INSERT INTO properties (name, value, goods_id)"
                                        f" VALUES ('{str(data[j][2]).strip()}', '{str(data[j][i]).strip()}',"
                                        f" '{goods_id}')")
                database.commit()
"""