#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as sql
import requests as req

from flask_sqlalchemy import SQLAlchemy

from db_setup import init_db
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mymusic.db'
app.secret_key = "flask rocks!"

db = SQLAlchemy(app)

init_db()


@app.route('/')
def index():
    con = sql.connect("cloth-shop.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from scarves")

    rows = cur.fetchall()

    return render_template(
        'index.html',
        price_options=[{'name': None, 'id': 0},
                       {'name': u'Не дорогой', 'id': 1},
                       {'name': u'Средней цены', 'id': 2},
                       {'name': u'Дорогой', 'id': 3}],
        length_options=[{'name': None, 'id': 0},
                        {'name': u'Длинный', 'id': 1},
                        {'name': u'Средний', 'id': 2},
                        {'name': u'Короткий', 'id': 3}],
        width_options=[{'name': None, 'id': 0},
                       {'name': 'Широкий', 'id': 1},
                       {'name': 'Средний', 'id': 2},
                       {'name': 'Узкий', 'id': 3}],
        color_options=[{'name': None, 'id': 0},
                       {'name': 'Цветастый', 'id': 1},
                       {'name': 'Средний', 'id': 2},
                       {'name': 'Однотонный', 'id': 3}],
        rows=rows)


@app.route('/personalization')
def personalization():
    return render_template('personalization.html')


@app.route('/concepts')
def concepts():
    return render_template('concepts.html')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# TODO should be added fuzzy c-means cluster algorithm
@app.route("/search", methods=['GET'])
def search():
    filters = []
    price_option = request.args.get('price')
    length_option = request.args.get('length')
    width_option = request.args.get('width')
    # color_option = request.form.get('color')
    if price_option != "None":
        value = "min"
        if price_option == "Средней цены":
            value = "avg"
        elif price_option == "Дорогой":
            value = "max"
        filters.append({"name": "price", "value": value})
    if str(length_option) != "None":
        value = "min"
        if length_option == "Длинный":
            value = "max"
        elif length_option == "Средний":
            value = "avg"
        filters.append({"name": "length", "value": value})

    if str(width_option) != "None":
        value = "min"
        if width_option == "Широкий":
            value = "max"
        elif width_option == "Средний":
            value = "avg"
        filters.append({"name": "width", "value": value})

    # if str(color_option) != "None":

    con = sql.connect("cloth-shop.db")
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute("select * from scarves")

    rows = cur.fetchall()

    if rows is None:
        return render_template("result.html", msg="Sorry! No scarves left")

    if len(filters) < 1:
        return render_template("list.html", rows=rows)

    data = {
        "scarves": rows,
        "filters": filters,
    }

    resp = req.post("http://localhost:8080/search", json=data)

    return render_template("list.html", rows=resp.json()["scarves"])


@app.route('/list')
def list_scarves():
    con = sql.connect("cloth-shop.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from scarves")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


@app.route('/scarf')
def new_scarf():
    return render_template('scarf.html')


@app.route('/scarf', methods=['POST', 'GET'])
def add_scarf():
    if request.method == 'POST':
        try:
            material = request.form['material']
            manufacturer = request.form['manufacturer']
            price = int(request.form['price'])
            color = request.form['color']
            width = int(request.form['width'])
            length = int(request.form['length'])

            with sql.connect("cloth-shop.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO scarves(material,manufacturer,price,colour,width,length, size) VALUES(?, ?, ?, ?, ?, ?, ?)",
                    (material, manufacturer, price, color, width, length, int(width / length)))

                con.commit()
                msg = "Record successfully added"

        except Exception as e:
            con.rollback()
            print(e)
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


if __name__ == '__main__':
    app.run()
