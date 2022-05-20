from flask import Flask, jsonify, request
from flask import send_from_directory
import psycopg2
import datetime
import pandas as pd
import numpy as np
from Content_recommendation import get_content_rec
app = Flask(__name__)

database = psycopg2.connect(database='Sobol', user='postgres', password=' ', host='127.0.0.1', port=5432)
database_cursor = database.cursor()


@app.route('/registration', methods=['POST'])
def registration():
    try:
        data = request.get_json()
        database_cursor.execute(
            "INSERT INTO Client (login, password, name, surname)"
            f"VALUES ('{data['login']}', {data['password']}', '{data['name']}',"
            f" '{data['surname']}', '{data['lastname']}')")
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
                        'id': id            
                    },

                    {
                        'name': name,
                        'id': id            
                    },
                ]
        """
        data = request.get_json()
        database_cursor.execute(f"select id, name from goods where sub_category = '{data['sub_category_id']}'")
        goods = []
        for el in database_cursor:
            goods.append({"id": el[0], "name": el[1]})

        return jsonify(goods)
    except IndexError:
        return jsonify({'answer': 'fail'})


@app.route('/get_goods_info', methods=['POST'])
def get_goods_info():
    try:
        """
                       {
                            'name': name,
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

        database_cursor.execute(f"select name, value from properties where goods_id = {data['id']}")

        goods_info = {'name': name, 'params': []}
        for row in database_cursor:
            goods_info['params'].append({'name': row[0], 'value': row[1]})

        return jsonify(goods_info)
    except IndexError:
        return jsonify({'answer': 'fail'})


if __name__ == "__main__":
    app.run(debug=True)
