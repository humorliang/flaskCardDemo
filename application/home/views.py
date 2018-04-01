# coding:utf-8
# 导入home蓝图
# 同级目录必须使用模块名引入
from .__init__ import home
from flask import render_template
from application.models import *
from application.exts import db


@home.route('/')
def index():
    user = User(username='limin', password='12345')
    # db.create_all()
    db.session.add(user)
    db.session.commit()
    return render_template('home/index.html')
