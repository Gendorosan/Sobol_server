import psycopg2

database = psycopg2.connect(database='Sobol', user='postgres', password=' ', host='127.0.0.1', port=5432)
database_cursor = database.cursor()


def get_content_rec(id):
    database_cursor.execute(f"Select sub_category_id, name from goods where id = ('{id}')")
    data = database_cursor.fetchall()
    name = data[0][1]
    sub_category_id = data[0][0]
    sub_category_info = {}
    database_cursor.execute(f"Select * from sub_category")

    for row in database_cursor:
        sub_category_info.update({row[1]: row[0]})
    database_cursor.execute(f"Select name from sub_category where id = ('{sub_category_id}')")

    for row in database_cursor:
        recomedation = []
        if row[0] == 'Лодки':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Аксессуары для лодок']} order by  rating LIMIT 3")

            for boat_accessory in database_cursor:
                recomedation.append(boat_accessory[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Весло']} order by  rating LIMIT 2")
            for oar in database_cursor:
                recomedation.append(oar[1])

            database_cursor.execute(f"select value from properties where goods_id = {id} and name = 'Тип'")
            for boat_type in database_cursor:
                if boat_type[0] == 'Моторная':
                    database_cursor.execute(f"select * from Goods where sub_category_id = "
                                            f"{sub_category_info['Мотор']} order by  rating LIMIT 2")
                    for engine in database_cursor:
                        recomedation.append(engine[1])

                if boat_type[0] == 'Гребная с креплением под транец':
                    database_cursor.execute(f"select value from properties where goods_id = {id} "
                                            f"and name = 'Длина, см'")
                    boat_len = 0
                    for boats_len in database_cursor:
                        boat_len = boats_len[0]

                    database_cursor.execute(f"select value from properties where goods_id = {id} "
                                            f"and name = 'Грузоподъемность, кг'")
                    boat_weight = 0
                    for boats_weight in database_cursor:
                        boat_weight = boats_weight[0]

                    database_cursor.execute(
                        f"select * from Goods as g where sub_category_id = {sub_category_info['Электромотор']} and "
                        f"id = (select goods_id from properties as p where p.goods_id = g.id "
                        f"and p.name = 'Макс длина лодки, см' and p.value > '{boat_len}') and id = "
                        f"(select goods_id from properties as p where p.goods_id = g.id and p.name "
                        f"= 'Макс вес лодки, кг' and p.value > '{boat_weight}') order by  rating "
                        f"LIMIT 2")
                    for engine in database_cursor:
                        recomedation.append(engine[1])

        if row[0] == 'Ледобуры':

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Леска']} order by  rating LIMIT 2")
            for fishing_line in database_cursor:
                recomedation.append(fishing_line[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Газ.баллон']} order by  rating LIMIT 2")
            for gas in database_cursor:
                recomedation.append(gas[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Газ.горелка']} order by  rating LIMIT 2")
            for gas in database_cursor:
                recomedation.append(gas[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Палатки']} order by  rating LIMIT 2")
            for tent in database_cursor:
                recomedation.append(tent[1])

        if row[0] == 'Ножи КИЗЛЯР':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Аксессуары для ножей']} order by  rating LIMIT 5")
            for knife in database_cursor:
                recomedation.append(knife[1])

        if row[0] == 'Газ.баллон':
            database_cursor.execute(
                f"select value from properties where goods_id = {id} and name = 'Тип баллона'")
            for ballon_type in database_cursor:
                database_cursor.execute(f"select * from Goods as g where sub_category_id ="
                                        f" {sub_category_info['Газ.горелка']} and "
                                        f"id = (select goods_id from properties as p where p.goods_id = g.id and "
                                        f"name = 'Тип баллона' and "
                                        f"value = '{ballon_type[0]}') "
                                        f"order by  rating LIMIT 5")
                for goods in database_cursor:
                    recomedation.append(goods[1])

        if row[0] == 'Аксессуары для лодок':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Весло']} order by  rating LIMIT 2")
            for oar in database_cursor:
                recomedation.append(oar[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Удочки']} order by  rating LIMIT 2")
            for rod in database_cursor:
                recomedation.append(rod[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Катушка']} order by  rating LIMIT 2")
            for coil in database_cursor:
                recomedation.append(coil[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Леска']} order by  rating LIMIT 2")
            for fishing_line in database_cursor:
                recomedation.append(fishing_line[1])

        if row[0] == 'Спальник':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Коврики, матрацы']} order by  rating LIMIT 3")
            for rug in database_cursor:
                recomedation.append(rug[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Палатки']} order by  rating LIMIT 2")
            for tent in database_cursor:
                recomedation.append(tent[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Средство от насекомых']} order by  rating LIMIT 2")
            for repellent in database_cursor:
                recomedation.append(repellent[1])

        if row[0] == 'Газ.горелка':
            database_cursor.execute(
                f"select value from properties where goods_id = {id} and name = 'Тип баллона'")
            for ballon_type in database_cursor:
                database_cursor.execute(f"select * from Goods as g where sub_category_id ="
                                        f" {sub_category_info['Газ.баллон']} and "
                                        f"id = (select goods_id from properties as p where p.goods_id = g.id and "
                                        f"name = 'Тип баллона' and "
                                        f"value = '{ballon_type[0]}') "
                                        f"order by  rating LIMIT 5")
                for goods in database_cursor:
                    recomedation.append(goods[1])

        if row[0] == 'Палатки':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Спальник']} order by  rating LIMIT 2")
            for sleeping_bag in database_cursor:
                recomedation.append(sleeping_bag[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Коврики, матрацы']} order by  rating LIMIT 2")
            for rug in database_cursor:
                recomedation.append(rug[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Аксесуары для палаток']} order by  rating LIMIT 2")
            for tent in database_cursor:
                recomedation.append(tent[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Средство от насекомых']} order by  rating LIMIT 2")
            for repellent in database_cursor:
                recomedation.append(repellent[1])

        if row[0] == 'Мотор':
            database_cursor.execute(f"select * from Goods as g where sub_category_id = "
                                    f"{sub_category_info['Лодки']} and id = "
                                    f"(select goods_id from properties as p where p.goods_id = g.id and p.name = 'Тип' "
                                    f"and p.value = 'Гребная с креплением под транец') order by  rating LIMIT 2")
            for boat in database_cursor:
                recomedation.append(boat[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Аксессуары для лодок']} order by  rating LIMIT 3")

            for boat_accessory in database_cursor:
                recomedation.append(boat_accessory[1])

        if row[0] == 'Катушка':
            database_cursor.execute(f"select * from Goods as g where sub_category_id = "
                                    f"{sub_category_info['Удочки']} and id = "
                                    f"(select goods_id from properties as p where p.goods_id = g.id and"
                                    f" p.name = 'Тип' and p.value = 'Спиннинг') order by  rating LIMIT 2;")
            for rod in database_cursor:
                recomedation.append(rod[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Леска']} order by  rating LIMIT 2")
            for fishing_line in database_cursor:
                recomedation.append(fishing_line[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Блесна']} order by  rating LIMIT 3")
            for spinner in database_cursor:
                recomedation.append(spinner[1])

        if row[0] == 'Электромотор':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Аксессуары для лодок']} order by  rating LIMIT 3")

            for boat_accessory in database_cursor:
                recomedation.append(boat_accessory[1])

            database_cursor.execute(f"select * from Goods as g where sub_category_id = "
                                    f"{sub_category_info['Лодки']} and id = "
                                    f"(select goods_id from properties as p where p.goods_id = g.id and p.name = 'Тип' "
                                    f"and p.value = 'Гребная с креплением под транец') order by  rating LIMIT 2")
            for boat in database_cursor:
                recomedation.append(boat[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Весло']} order by  rating LIMIT 2")
            for oar in database_cursor:
                recomedation.append(oar[1])

        if row[0] == 'Леска':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Удочки']} order by  rating LIMIT 3")
            for rod in database_cursor:
                recomedation.append(rod[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Катушка']} order by  rating LIMIT 2")
            for coil in database_cursor:
                recomedation.append(coil[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Блесна']} order by  rating LIMIT 3")
            for spinner in database_cursor:
                recomedation.append(spinner[1])

        if row[0] == 'Коврики, матрацы':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Спальник']} order by  rating LIMIT 3")
            for sleeping_bag in database_cursor:
                recomedation.append(sleeping_bag[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Палатки']} order by  rating LIMIT 2")
            for tent in database_cursor:
                recomedation.append(tent[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Средство от насекомых']} order by  rating LIMIT 2")
            for repellent in database_cursor:
                recomedation.append(repellent[1])

        if row[0] == 'Средство от насекомых':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Спальник']} order by  rating LIMIT 3")
            for sleeping_bag in database_cursor:
                recomedation.append(sleeping_bag[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Палатки']} order by  rating LIMIT 2")
            for tent in database_cursor:
                recomedation.append(tent[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Коврики, матрацы']} order by  rating LIMIT 2")
            for rug in database_cursor:
                recomedation.append(rug[1])

        if row[0] == 'Аксессуары для ножей':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Ножи КИЗЛЯР']} order by  rating LIMIT 3")
            for knife in database_cursor:
                recomedation.append(knife[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Средство от насекомых']} order by  rating LIMIT 2")
            for repellent in database_cursor:
                recomedation.append(repellent[1])

        if row[0] == 'Весло':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Аксессуары для лодок']} order by  rating LIMIT 3")

            for knife in database_cursor:
                recomedation.append(knife[1])

            database_cursor.execute(f"select * from Goods as g where sub_category_id = "
                                    f"{sub_category_info['Лодки']} and id = "
                                    f"(select goods_id from properties as p where p.goods_id = g.id and p.name = 'Тип' "
                                    f"and p.value = 'Гребная') order by  rating LIMIT 2")
            for boat in database_cursor:
                recomedation.append(boat[1])

        if row[0] == 'Удочки':
            database_cursor.execute(f"select value from properties where goods_id = {id} and name = 'Тип'")
            for rod in database_cursor:
                if rod[0] == 'Спиннинг':
                    database_cursor.execute(f"select * from Goods where sub_category_id = "
                                            f"{sub_category_info['Катушка']} order by  rating LIMIT 2")
                    for coil in database_cursor:
                        recomedation.append(coil[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Леска']} order by  rating LIMIT 2")
            for fishing_line in database_cursor:
                recomedation.append(fishing_line[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Блесна']} order by  rating LIMIT 4")
            for spinner in database_cursor:
                recomedation.append(spinner[1])

            database_cursor.execute(f"select * from Goods as g where sub_category_id = "
                                    f"{sub_category_info['Рюкзаки,сумки ,мешки']} "
                                    f"and id = (select goods_id from properties as p where p.goods_id = g.id and"
                                    f" p.name = 'Назначение' and p.value = 'для охоты и рыбалки') order by  rating"
                                    f" LIMIT 2;")
            for bag in database_cursor:
                recomedation.append(bag[1])

        if row[0] == 'Рюкзаки,сумки ,мешки':

            database_cursor.execute(
                f"select value from properties where goods_id = {id} and name = 'Назначение'")
            for boat_type in database_cursor:
                if boat_type[0] == 'для охоты и рыбалки':
                    database_cursor.execute(f"select * from Goods where sub_category_id = "
                                            f"{sub_category_info['Удочки']} order by  rating LIMIT 2")
                    for rod in database_cursor:
                        recomedation.append(rod[1])

                    database_cursor.execute(f"select * from Goods where sub_category_id = "
                                            f"{sub_category_info['Катушка']} order by  rating LIMIT 2")
                    for coil in database_cursor:
                        recomedation.append(coil[1])

                    database_cursor.execute(f"select * from Goods where sub_category_id = "
                                            f"{sub_category_info['Леска']} order by  rating LIMIT 2")
                    for fishing_line in database_cursor:
                        recomedation.append(fishing_line[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Средство от насекомых']} order by  rating LIMIT 2")
            for repellent in database_cursor:
                recomedation.append(repellent[1])

        if row[0] == 'Блесна':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Удочки']} order by  rating LIMIT 3")
            for rod in database_cursor:
                recomedation.append(rod[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Катушка']} order by  rating LIMIT 2")
            for coil in database_cursor:
                recomedation.append(coil[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Леска']} order by  rating LIMIT 2")
            for fishing_line in database_cursor:
                recomedation.append(fishing_line[1])

        if row[0] == 'Аксесуары для палаток':
            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Спальник']} order by  rating LIMIT 2")
            for sleeping_bag in database_cursor:
                recomedation.append(sleeping_bag[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Коврики, матрацы']} order by  rating LIMIT 2")
            for rug in database_cursor:
                recomedation.append(rug[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Палатки']} order by  rating LIMIT 2")
            for tent in database_cursor:
                recomedation.append(tent[1])

            database_cursor.execute(f"select * from Goods where sub_category_id = "
                                    f"{sub_category_info['Средство от насекомых']} order by  rating LIMIT 2")
            for repellent in database_cursor:
                recomedation.append(repellent[1])

        poplar_goods = 10 - len(recomedation)

        if len(recomedation) < 10:
            rest = 10 - len(recomedation)

            database_cursor.execute(f"select * from Goods where name not in ({str(recomedation)[1:-1]}, '{name}')"
                                    f" order by  rating LIMIT {rest}")
            for knife in database_cursor:
                recomedation.append(knife[1])

        for i in range(len(recomedation)):
            recomedation[i] = str(recomedation[i]).strip()

        goods = []
        for good in recomedation:
            database_cursor.execute(f"select id from goods where name = '{good}'")
            for el in database_cursor:
                goods.append({"id": el[0], "name": good})

        return goods
