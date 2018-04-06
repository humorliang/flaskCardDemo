from .__init__ import admin
from flask import render_template, redirect, request, flash, session, url_for
from .forms import LoginForm, AddNewsForm
from application.models import *
from functools import wraps


# 定义管理员登陆装饰器
def admin_login_decorate(fun):
    @wraps(fun)
    def check_session(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.index', next=request.url))
        return fun(*args, **kwargs)

    return check_session


# 登陆
@admin.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user = Admin.query.filter_by(username=data['username']).first()
            if not user.check_pwd(data['password']):
                flash('密码错误')
                return redirect(url_for('admin.index'))
            session['admin'] = data['username']
            return redirect(url_for('admin.news_list'))
    return render_template('admin/login.html', form=form)


# 银行信息
@admin.route('/newsList')
@admin_login_decorate
def news_list():
    return render_template('admin/new-info.html')


# 添加银行消息
@admin.route('/addNews', methods=['GET', 'POST'])
@admin_login_decorate
def add_news():
    form = AddNewsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            bankinfo = BankInfo(title=data['title'], posturl=data['url'], date=data['newsDate'])
            db.session.add(bankinfo)
            db.session.commit()
            return redirect(url_for('admin.news_list'))
    return render_template('admin/add-news.html', form=form)


# 删除银行消息
@admin.route('/delNews')
@admin_login_decorate
def del_news():
    pass
    return render_template('admin/new-info.html')


# 管理员信息
@admin.route('/adminInfo')
@admin_login_decorate
def admin_info():
    return render_template('admin/admin-info.html')


# 修改密码
@admin.route('/changePwd')
@admin_login_decorate
def change_pwd():
    return render_template('admin/change-pwd.html')


# 账户信息
@admin.route('/userInfo')
@admin_login_decorate
def user_info():
    return render_template('admin/account-info.html')


# 冻结账户
@admin.route('/freezeUser')
@admin_login_decorate
def freeze_user():
    return render_template('admin/account-info.html')


# 申请列表
@admin.route('/applyList')
@admin_login_decorate
def apply_list():
    return render_template('admin/apply-list.html')


# 添加信用卡
@admin.route('/addCredit')
@admin_login_decorate
def add_credit():
    return render_template('admin/add-credit.html')


# 账单信息
@admin.route('/dealInfo')
@admin_login_decorate
def deal_info():
    return render_template('admin/deal-info.html')


# 添加账单
@admin.route('/addDeal')
@admin_login_decorate
def add_deal():
    return render_template('admin/add-deal.html')


# 欠款信息
@admin.route('/debtInfo')
@admin_login_decorate
def debt_info():
    return render_template('admin/debt-info.html')


# 添加欠款信息
@admin.route('/addDebt')
@admin_login_decorate
def add_debt():
    return render_template('admin/add-debt.html')


# 消费信息
@admin.route('/consumeInfo')
@admin_login_decorate
def consume_info():
    return render_template('admin/consume-info.html')


# 添加消费信息
@admin.route('/addConsume')
@admin_login_decorate
def add_consume():
    return render_template('admin/add-consume.html')


# 退出
@admin.route('/loginOut')
@admin_login_decorate
def login_out():
    session.pop('admin', None)
    return redirect(url_for('admin.index'))
