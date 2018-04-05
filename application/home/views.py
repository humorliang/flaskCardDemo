# coding:utf-8
# 导入home蓝图
# 同级目录必须使用模块名引入
from .__init__ import home
from flask import render_template
from application.models import *
from application.exts import db


# 登陆视图
@home.route('/')
def login():
    # # 1.用户表
    # user = User(username='老王', password='123456', phone='18894259425')
    # db.session.add(user)
    # db.session.commit()
    # info = Info(name='张三', age=28, phone='18894259425', sex=1, email='163@123.com', job='python',
    #             idcard='342422199611185836')
    # db.session.add(info)
    # db.session.commit()
    # # 2信用卡表
    # credit = Credit(creditid='62280004', limit=1000, overmoney=1000, creditname='张三', phone='18894259425',
    #                 vaildate='2018-02-03', cdtstatus='1', idcard='3424231888')
    # db.session.add(credit)
    # db.session.commit()
    #
    # # 还款表
    # debt = Debt(credit_id='62280004', debt_date='2018-03-02', sum_money=100)
    # consume = Consume(credit_id='62280004', consume_date='2018-03-03', sum_money=1000)
    # deal = Deal(credit_id='62280004', sum_money=100, deal_date='2018-3-20', deal_type='购物', description='买个手机')
    #
    # db.session.add_all([deal, debt, consume])
    # db.session.commit()
    return render_template('home/login.html')


# 千万不要使用蓝图名定义视图函数，否则蓝图会被覆盖
# 用户主页
@home.route('/main')
def main():
    return render_template('home/index.html')


# 用户信息视图
@home.route('/userInfo')
def user_info():
    return render_template('home/user-info.html')


# 修改信息视图
@home.route('/editInfo')
def edit_info():
    return render_template('home/edit-info.html')


# 修改密码
@home.route('/editPwd')
def edit_pwd():
    return render_template('home/edit-pwd.html')


# 我的信用卡
@home.route('/myCredit')
def my_credit():
    return render_template('home/my-credit.html')


# 信用卡申请
@home.route('/applyCredit')
def apply_credit():

    return render_template('home/apply-credit.html')


# 账单信息
@home.route('/dealInfo')
def deal_info():
    return render_template('home/deal-info.html')


# 欠款信息
@home.route('/debtInfo')
def debt_info():
    return render_template('home/debt-info.html')


# 消费信息
@home.route('/consumeInfo')
def consume_info():
    return render_template('home/consume-info.html')

