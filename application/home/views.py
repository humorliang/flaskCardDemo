# coding:utf-8
# 导入home蓝图
# 同级目录必须使用模块名引入
from .__init__ import home
from flask import render_template
from application.models import *
from application.exts import db


@home.route('/')
def index():
    # user = User(username='limin', password='12345')
    # db.session.add(user)
    # db.session.commit()

    # admin = Admin(username='老王', password='123456')
    # debt = Debt(credit_id='5656565', debt_date='2018-02-16', sum_money='100', cdid=1)
    # consume = Consume(credit_id='3636565', consume_date='2018-02-16', sum_money='100')
    # deal = Deal(credit_id='64585', sum_money='1000', deal_date='2018-03-06', deal_type='正常', description='转账')
    # user = User(username='老李', password='256112', phone='188888888')
    # info = Info(name="张三", age=20, phone='16699999998', sex=0, email='15369@163.com', job='程序员',
    #              idcard='34242218620526568')
    # credit = Credit(creditid='654238', limit='12000', overmoney='12000', creditname='老梁', vaildate='2018-2-13',
    #                 cdtstatus=0,idcard='3425689595583')
    # db.session.add_all([admin, debt, consume, deal, user, info, credit])
    #
    #
    #
    # db.session.add(admin)
    # db.session.add(debt)
    # db.session.commit()
    user = User(name='老王', phone='123456789')
    user2 = User(name='老李', phone='123456')
    phone = Phone(name='老王手机', uid=0)
    phone2 = Phone(name='老李手机', uid=1)
    # db.session.add_all([user, user2, phone, phone2])
    db.session.add(phone2)
    db.session.commit()
    return render_template('home/index.html')
