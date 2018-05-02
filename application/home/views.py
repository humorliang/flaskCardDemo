# coding:utf-8
# 导入home蓝图
# 同级目录必须使用模块名引入

from .__init__ import home
from flask import render_template, session, flash, redirect, url_for, request
from application.models import *
from application.exts import db
from .forms import RegisterForm, LoginForm, ApplyForm, AddInfoForm, EditPwdForm
from functools import wraps


# d定义登陆装饰器
def user_login_decorate(fun):
    @wraps(fun)
    def check_session(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login', next=request.url))
        return fun(*args, **kwargs)

    return check_session


# 定义一个


# 用户主页
@home.route('/main/<int:page>/')
@user_login_decorate
def main(page=None):
    if page is None:
        page = 1
    newsInfo = BankInfo.query.order_by(BankInfo.date.desc()).paginate(page=page, per_page=8)
    return render_template('home/index.html', newsInfo=newsInfo)


#
@home.route('/')
@user_login_decorate
def user_main():
    return redirect(url_for('home.main', page=1))


# 登陆视图
@home.route('/login', methods=['GET', "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user = User.query.filter_by(username=data['username']).first()
            if not user.check_pwd(data['password']):
                flash('密码错误')
                return redirect(url_for('home.login'))
            session['user'] = data['username']
            # # 设置session过期时间
            # print(data['remember']) # 返回值为True
            if data['remember']:
                session.permanent = True  # 设置浏览器关闭还保存session
            return redirect(url_for('home.main', page=1))
    return render_template('home/login.html', form=form)


# 退出登陆
@home.route('/loginOut')
@user_login_decorate
def login_out():
    session.pop('user', None)
    return redirect(url_for('home.login'))


# 注册视图
@home.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            date = form.data
            user = User(username=date['username'], password=date['password'], phone=date['phone'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home.login'))
    return render_template('home/register.html', form=form)


# 用户信息视图
@home.route('/userInfo')
@user_login_decorate
def user_info():
    username = session.get('user')
    user_ = User.query.filter_by(username=username).first()
    return render_template('home/user-info.html', user=user_)


# 编辑简介
@home.route('/addInfo', methods=['GET', 'POST'])
@user_login_decorate
def add_user_info():
    form = AddInfoForm()
    if form.validate_on_submit():
        data = form.data
        username = session.get('user')
        infos = User.query.filter_by(username=username).update(
            dict(name=data['name'], sex=int(data['sex']),
                 age=data['age'], email=data['email'],
                 job=data['job'], idCard=data['IDCard'],
                 address=data['address']))
        db.session.commit()
        return redirect(url_for('home.user_info'))
    return render_template('home/add-info.html', form=form)


# 修改密码
@home.route('/editPwd', methods=['GET', 'POST'])
@user_login_decorate
def edit_pwd():
    form = EditPwdForm()
    if form.validate_on_submit():
        data = form.data
        user = session.get('user')
        user_pwd = User.query.filter_by(username=user).update(dict(password=data['new_pwd']))
        db.session.commit()
        return redirect(url_for('home.login'))
    return render_template('home/edit-pwd.html', form=form)


# 我的信用卡
@home.route('/myCredit')
@user_login_decorate
def my_credit():
    username = session.get('user')
    user = User.query.filter_by(username=username).first()
    credit = Credit.query.filter(user.phone == Credit.phone).first()
    return render_template('home/my-credit.html', credit=credit)


# 挂失
@home.route('/freeze/<int:id>/')
@user_login_decorate
def freeze_user(id=None):
    credit = Credit.query.filter_by(id=id).update(dict(cdt_status=0))
    db.session.commit()
    return redirect(url_for('home.my_credit'))


# 信用卡申请
@home.route('/applyCredit', methods=['GET', 'POST'])
@user_login_decorate
def apply_credit():
    form = ApplyForm()
    if form.validate_on_submit():
        data = form.data
        applys = ApplyCard(name=data['name'], limit=data['limit'], idcard=data['idCard'], phone=data['phone'])
        db.session.add(applys)
        db.session.commit()
        return redirect(url_for('home.main', page=1))
    return render_template('home/apply-credit.html', form=form)


# 账单信息
@home.route('/dealInfo/<int:page>/')
@user_login_decorate
def deal_info(page=None):
    if page is None:
        page = 1
    deals = None
    try:
        user = session.get('user')
        user_ = User.query.filter_by(username=user).first()
        credit = Credit.query.filter_by(phone=user_.phone).first()
        print(credit.credit_id)
        deals = db.session.query(Deal, Credit).filter(
            Deal.credit_id == credit.credit_id,
            Credit.credit_id == credit.credit_id
        ).paginate(page=page, per_page=3)
        return render_template('home/deal-info.html', deals=deals)
    except Exception as e:
        return render_template('home/deal-info.html', deals=deals)


# 欠款信息
@home.route('/debtInfo/<int:page>/')
@user_login_decorate
def debt_info(page=None):
    if page is None:
        page = 1
    debts = None
    try:
        user = session.get('user')
        user_ = User.query.filter_by(username=user).first()
        credit = Credit.query.filter_by(phone=user_.phone).first()
        debts = db.session.query(Debt, Credit).filter(
            Debt.credit_id == credit.credit_id,
            Credit.credit_id == credit.credit_id
        ).paginate(page=page, per_page=3)
        return render_template('home/debt-info.html', debts=debts)
    except Exception as e:
        return render_template('home/debt-info.html', debts=debts)


# 消费信息
@home.route('/consumeInfo/<int:page>/')
@user_login_decorate
def consume_info(page=None):
    if page is None:
        page = 1
    consumes = None
    try:
        user = session.get('user')
        user_ = User.query.filter_by(username=user).first()
        credit = Credit.query.filter_by(phone=user_.phone).first()
        consumes = db.session.query(Consume, Credit).filter(
            Consume.credit_id == credit.credit_id,
            Credit.credit_id == credit.credit_id
        ).paginate(page=page, per_page=3)
        return render_template('home/consume-info.html', consumes=consumes)
    except Exception as e:
        return render_template('home/consume-info.html', consumes=consumes)
