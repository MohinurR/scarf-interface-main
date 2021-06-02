import sqlite3 as sql
from app import app
from db_setup import init_db
from models import Scarf
from flask import Flask, flash, redirect, render_template, request, url_for

def init():
    con = sql.connect("cloth-shop.db")
    cur = con.cursor()
    cur.execute(
        """create table if not exists scarves(
        id integer primary key,
        material VARCHAR(255),
        manufacturer VARCAHAR(255), 
        price INTEGER,
        colour VARCHAR(100),
        width INTEGER,
        length INTEGER, 
        size DECIMAL(10,2)
        )""")
    cur.execute("delete from scarves;")
    con.commit()