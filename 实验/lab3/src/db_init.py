# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/29 14:20
@Author  : 和泳毅
@FileName: db_init.py
@SoftWare: PyCharm
"""

from flask_sqlalchemy import SQLAlchemy
import mysql.connector

db = SQLAlchemy()

db2 = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='1234',
    database='bank'
)
