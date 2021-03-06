from flask import Flask, jsonify, request
from flask import send_from_directory
import psycopg2
import datetime
import pandas as pd
import numpy as np
from Content_recommendation import get_content_rec
from –°ollaborative_recommendation import  get_collab_rec
app = Flask(__name__)

database = psycopg2.connect(database='Sobol', user='postgres', password=' ', host='127.0.0.1', port=5432)
database_cursor = database.cursor()


@app.route('/registration', methods=['POST'])
def registration():
    try:
        data = request.get_json()
        database_cursor.execute(
            "INSERT INTO Client (login, password, name, surname)"
            f"VALUES ('{data['login']}', '{data['password']}', '{data['name']}',"
            f" '{data['surname']}')")
        database.commit()
        return_answer = {'answer': 'success'}
        return jsonify(return_answer)
    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/authentication', methods=['POST'])
def authentication():
    try:
        data = request.get_json()
        database_cursor.execute("select name, surname from Client "
                                f"where login = '{data['login']}' and password = '{data['password']}'")
        user_info = []
        for row in database_cursor:
            print(row)
            user_info.append(row)

        return_answer = {'answer': 'success', 'name': str(user_info[0][0]).strip(),
                         'surname': str(user_info[0][1]).strip()}
        return jsonify(return_answer)
    except IndexError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/get_content_recommendation', methods=['POST'])
def get_content_recommendation():
    try:
        """
                [
                    {
                        'name': name,
                        'id': id            
                    },
    
                    {
                        'name': name,
                        'id': id            
                    }
                ]
                
         """
        data = request.get_json()
        return jsonify(get_content_rec(data['id']))

    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/get_collaborative_recommendation', methods=['POST'])
def get_collaborative_recommendation():
    try:
        """
        –ü—Ä–ł—Ö–ĺ–ī–ł—ā:
        {
            'login': login,
            'basketArray': []
        }

         """
        data = request.get_json()

        recomendation = [{'id': 254, 'name': '–°–Ņ–ł–Ĺ–Ĺ–ł–Ĺ–≥ Aiko Pro Jigger PJ 792M', 'price': '10500'},
                         {'id': 255, 'name': '–°–Ņ–ł–Ĺ–Ĺ–ł–Ĺ–≥ Aiko Espada Pro ESPP 240ML', 'price': '5760'},
                         {'id': 253, 'name': '–°–Ņ–ł–Ĺ–Ĺ–ł–Ĺ–≥ MAJOR CRAFT Vierra 862H', 'price': '9770'},
                         {'id': 86, 'name': '–ö–į—ā—É—ą–ļ–į Okuma Epixor XT Spinning Reel 30', 'price': '11600'},
                         {'id': 85, 'name': '–ö–į—ā—É—ą–ļ–į Okuma ITX Carbon Spinning Reel 1000', 'price': '15200'},
                         {'id': 34, 'name': '–Ď–Ľ–Ķ—Ā–Ĺ–į –≤—Ä–į—Č–į—é—Č–į—Ź—Ā—Ź —Ā —Ä—č–Ī–ļ–ĺ–Ļ BLUE FOX Vibrax CHASER 2 —Ü–≤–Ķ—ā',
                          'price': '820'},
                         {'id': 35, 'name': '–Ď–Ľ–Ķ—Ā–Ĺ–į –≤—Ä–į—Č–į—é—Č–į—Ź—Ā—Ź —Ā —Ä—č–Ī–ļ–ĺ–Ļ BLUE FOX Vibrax CHASER 2 —Ü–≤–Ķ—ā OCW',
                          'price': '820'},
                         {'id': 33, 'name': '–Ď–Ľ–Ķ—Ā–Ĺ–į –≤—Ä–į—Č–į—é—Č–į—Ź—Ā—Ź BLUE FOX Northern Lights Vibrax 2 —Ü–≤–Ķ—ā BL',
                          'price': '510'},
                         {'id': 2, 'name': '–†–Ķ–ľ–ļ–ĺ–ľ–Ņ–Ľ–Ķ–ļ—ā –ī–Ľ—Ź –Ľ–ĺ–ī–ĺ–ļ –ü–í–•', 'price': '400'},
                         {'id': 1, 'name': '–ö–Ľ–Ķ–Ļ –ī–Ľ—Ź –Ľ–ĺ–ī–ĺ–ļ –ü–í–•', 'price': '150'}]

        return jsonify(get_collab_rec(data['login'], data['basketArray']))

    except SyntaxError:
        return_answer = {'answer': 'fail'}
        return jsonify(return_answer)


@app.route('/get_all_categories', methods=['GET'])
def get_all_categories():
    try:
        """
        [
            {
                'name': name,
                'id': id            
            },
            
            {
                'name': name,
                'id': id            
            },
        ]
        """
        # data = request.get_json()
        database_cursor.execute("select id, name from category")
        categories = []
        for el in database_cursor:
            categories.append({"id": el[0], "name": el[1]})

        return jsonify(categories)
    except IndexError:
        return jsonify({'answer': 'fail'})


@app.route('/get_all_subcategories', methods=['POST'])
def get_all_subcategories():
    try:

        """
        [
            {
                'name': name,
                'id': id            
            },

            {
                'name': name,
                'id': id            
            },
        ]
        """
        data = request.get_json()
        database_cursor.execute(f"select id, name from sub_category where category_id = {data['id']}")
        categories = []
        for el in database_cursor:
            categories.append({"id": el[0], "name": el[1]})

        return jsonify(categories)
    except IndexError:
        return jsonify({'answer': 'fail'})


@app.route('/get_all_goods_from_subcategory', methods=['POST'])
def get_all_goods_from_subcategory():
    try:
        """
                [
                    {
                        'name': name,
                        'id': id,
                        'price': price           
                    },

                    {
                        'name': name,
                        'id': id
                        'price': price            
                    }
                ]
        """
        data = request.get_json()
        database_cursor.execute(f"select id, name from goods where sub_category_id = '{data['sub_category_id']}'")
        goods = []
        for el in database_cursor:
            goods.append({"id": el[0], "name": el[1]})

        for good in goods:
            database_cursor.execute(f"select value from properties where name = '–¶–Ķ–Ĺ–į' and goods_id = {good['id']}")
            price = database_cursor.fetchall()[0][0]
            good.update({'price': price})

        return jsonify(goods)
    except IndexError:
        return jsonify({'answer': 'fail'})


@app.route('/fill_cart', methods=['POST'])
def fill_cart():
    try:
        """
        {
            'client': login
            'goods': [1,2,3,4,...]
        }
        """

        data = request.get_json()

        database_cursor.execute(
            f"insert into cart (client_login) values ('{data['client']}')")
        database.commit()

        database_cursor.execute(f"select id from cart where client_login = '{data['client']}' order by id desc LIMIT 1")
        cart_id = database_cursor.fetchall()[0][0]

        for good in data['goods']:
            database_cursor.execute(
                f"insert into goods_in_cart (goods_id, cart_id) values ({good}, {cart_id})")
            database.commit()
        return jsonify({'answer': 'success'})
    except KeyError:
        data = request.get_json()

        database_cursor.execute(
            "insert into cart (client_login) values (Null)")
        database.commit()
        database_cursor.execute("select max(id) from cart")
        cart_id = database_cursor.fetchall()[0][0]
        for good in data['goods']:
            database_cursor.execute(
                f"insert into goods_in_cart (goods_id, cart_id) values ({good}, {cart_id})")
            database.commit()
        return jsonify({'answer': 'success'})
    except IndexError:
        return jsonify({'answer': 'fail'})


@app.route('/get_goods_info', methods=['POST'])
def get_goods_info():
    try:
        """
                       {
                            'name': name,
                            'price': price,
                            'params': 
                                [   
                                    {'name': name, 'value': value},
                                    {'name': name, 'value': value},
                                    {'name': name, 'value': value},
                                ]            
                       }
        """
        data = request.get_json()
        database_cursor.execute(f"select name from goods where id = {data['id']}")

        name = database_cursor.fetchall()[0][0]
        database_cursor.execute(f"select value from properties where name = '–¶–Ķ–Ĺ–į' and goods_id = {data['id']}")
        price = database_cursor.fetchall()[0][0]

        goods_info = {'name': name, 'price': price, 'params': []}
        database_cursor.execute(f"select name, value from properties where goods_id = {data['id']} and name != '–¶–Ķ–Ĺ–į'")

        for row in database_cursor:
            goods_info['params'].append({'name': row[0], 'value': row[1]})

        return jsonify(goods_info)
    except IndexError:
        return jsonify({'answer': 'fail'})


if __name__ == "__main__":
    app.run(debug=True)
