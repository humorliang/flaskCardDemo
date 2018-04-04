# coding:utf-8
from application.exts import db


# 创建表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


    def __init__(self, id=None, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password
        print('create table user')

