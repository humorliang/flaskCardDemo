from .__init__ import admin
from flask import render_template


# 登陆
@admin.route('/')
def index():
    return render_template('admin/login.html')


# 银行信息
@admin.route('/newsList')
def news_list():
    return render_template('admin/new-info.html')


# 添加银行消息
@admin.route('/addNews')
def add_news():
    return render_template('admin/add-news.html')


# 删除银行消息
@admin.route('/delNews')
def del_news():
    pass
    return render_template('admin/new-info.html')


# 管理员信息
@admin.route('/adminInfo')
def admin_info():
    return render_template('admin/admin-info.html')


# 修改密码
@admin.route('/changePwd')
def change_pwd():
    return render_template('admin/change-pwd.html')


# 账户信息
@admin.route('/userInfo')
def user_info():
    return render_template('admin/account-info.html')


# 冻结账户
@admin.route('/freezeUser')
def freeze_user():
    return render_template('admin/account-info.html')


# 申请列表
@admin.route('/applyList')
def apply_list():
    return render_template('admin/apply-list.html')


# 添加信用卡
@admin.route('/addCredit')
def add_credit():
    return render_template('admin/add-credit.html')


# 账单信息
@admin.route('/dealInfo')
def deal_info():
    return render_template('admin/deal-info.html')


# 添加账单
@admin.route('/addDeal')
def add_deal():
    return render_template('admin/add-deal.html')


# 欠款信息
@admin.route('/debtInfo')
def debt_info():
    return render_template('admin/debt-info.html')


# 添加欠款信息
@admin.route('/addDebt')
def add_debt():
    return render_template('admin/add-debt.html')


# 消费信息
@admin.route('/consumeInfo')
def consume_info():
    return render_template('admin/consume-info.html')


# 添加消费信息
@admin.route('/addConsume')
def add_consume():
    return render_template('admin/add-consume.html')


# 退出
@admin.route('/loginOut')
def login_out():
    return render_template('admin/login.html')
