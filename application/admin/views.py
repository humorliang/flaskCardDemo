from .__init__ import admin
from flask import render_template, redirect, request, flash, session, url_for
from .forms import LoginForm, DealForm, ConsumeForm, AddNewsForm, EditPwdForm, DebtForm, AddCreditForm
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
            return redirect(url_for('admin.news_list', page=1))
    return render_template('admin/login.html', form=form)


# 主页
@admin.route('/main')
def admin_main():
    return render_template('admin/main.html')


# 银行信息
@admin.route('/newsList/<int:page>/')
def news_list(page=None):
    if page is None:
        page = 1
    newsInfo = BankInfo.query.order_by(BankInfo.date.desc()).paginate(page=page, per_page=8)
    return render_template('admin/new-info.html', newsInfo=newsInfo)


# 添加银行消息
@admin.route('/addNews', methods=['GET', 'POST'])
def add_news():
    form = AddNewsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            print(data['newsDate'])
            bankinfo = BankInfo(title=data['title'], posturl=data['url'], date=data['newsDate'])
            db.session.add(bankinfo)
            db.session.commit()
            return redirect(url_for('admin.news_list', page=1))
    return render_template('admin/add-news.html', form=form)


# 删除银行消息
@admin.route('/delNews/<int:id>/')
def del_news(id=None):
    news = BankInfo.query.filter_by(id=id).first_or_404()
    db.session.delete(news)
    db.session.commit()
    return redirect(url_for('admin.news_list', page=1))


# 管理员信息
@admin.route('/adminInfo')
def admin_info():
    # 直接答应session['admin']会报错
    # print(session.get('admin'))
    admin_u = session.get('admin')
    admin_info = Admin.query.filter_by(username=admin_u).first_or_404()
    return render_template('admin/admin-info.html', admin_info=admin_info)


# 修改密码
@admin.route('/changePwd', methods=['GET', 'POST'])
def change_pwd():
    form = EditPwdForm()
    data = form.data
    if request.method == 'POST':
        if form.validate_on_submit():
            user = session.get('admin')
            # 1.更改数据的方法
            # admin_info = Admin.query.filter_by(username=user).first_or_404()
            # print(admin_info.password)# 只有数据模型返回过来才能使用此用法
            # admin_info.password = data['new_pwd']
            # ----------------------------------------------
            # 2.更改数据的方法
            # 参考https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information
            admin_info = Admin.query.filter_by(username=user).update(dict(password=data['new_pwd']))
            db.session.commit()
            return redirect(url_for('admin.admin_info'))
    return render_template('admin/change-pwd.html', form=form)


# 账户信用卡信息
@admin.route('/userInfo/<int:page>/')
def user_info(page=None):
    if page is None:
        page = 1
    credit_list = db.session.query(Debt, Credit).filter(Debt.credit_id == Credit.credit_id).paginate(page=page,
                                                                                                     per_page=2)
    return render_template('admin/account-info.html', credit_data=credit_list)


# 冻结账户
@admin.route('/freezeUser/<int:id>/')
def freeze_user(id=None):
    user_c = Credit.query.filter_by(id=id).update(dict(cdt_status=0))
    db.session.commit()
    return redirect(url_for('admin.user_info', page=1))


# 恢复账户
@admin.route('/recover/<int:id>')
def recover_user(id=None):
    user_c = Credit.query.filter_by(id=id).update(dict(cdt_status=1))
    db.session.commit()
    return redirect(url_for('admin.user_info', page=1))


# 申请列表
@admin.route('/applyList/<int:page>/')
def apply_list(page=None):
    if page is None:
        page = 1
    return render_template('admin/apply-list.html')


# 添加信用卡
@admin.route('/addCredit', methods=['GET', 'POST'])
def add_credit():
    form = AddCreditForm()
    if form.validate_on_submit():
        data = form.data
        credit = Credit(creditid=data['creditId'], creditname=data['name'],
                        limit=data['limit'], idcard=data['idCard'],
                        phone=data['phone'], email=data['email'],
                        vaildate=data['vailDate'], overmoney=data['limit'],
                        cdtstatus=1
                        )
        db.session.add(credit)
        db.session.commit()
        return redirect(url_for('admin.user_info', page=1))
    return render_template('admin/add-credit.html', form=form)


# 账单信息
@admin.route('/dealInfo/<int:page>/')
def deal_info(page=None):
    if page is None:
        page = 1
    deal = db.session.query(Deal, Credit).filter(
        Deal.credit_id == Credit.credit_id).order_by(
        Deal.deal_date.desc()).paginate(page=1, per_page=2)

    return render_template('admin/deal-info.html', deals=deal)


# 添加账单
@admin.route('/addDeal', methods=['GET', 'POST'])
def add_deal():
    form = DealForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            deals = Deal(credit_id=data['creditId'], deal_date=data['date'], deal_type='转账', sum_money=data['money'],
                         description=data['comment'])
            db.session.add(deals)
            db.session.commit()
            return redirect(url_for('admin.deal_info', page=1))
    return render_template('admin/add-deal.html', form=form)


# 欠款信息
@admin.route('/debtInfo/<int:page>/')
def debt_info(page=None):
    if page is None:
        page = 1
    # 多表查询
    debt = db.session.query(Debt.credit_id, Credit.creditName, Debt.debt_date, Debt.sum_money, Credit.id,
                            Credit.cdt_status).filter(
        Debt.credit_id == Credit.credit_id).order_by(
        Debt.debt_date.desc()).paginate(page=page, per_page=2)

    # items_list = debt.items
    # print(len(items_list))  # list
    #
    # print(type(items_list[0].id))
    return render_template('admin/debt-info.html', debt=debt)


# 添加欠款信息
@admin.route('/addDebt', methods=['GET', 'POST'])
def add_debt():
    form = DebtForm()
    if form.validate_on_submit():
        data = form.data
        debtInfo = Debt(credit_id=data['creditId'], debt_date=data['date'], sum_money=data['money'])
        db.session.add(debtInfo)
        db.session.commit()
        return redirect(url_for('admin.debt_info', page=1))
    return render_template('admin/add-debt.html', form=form)


# 消费信息
@admin.route('/consumeInfo/<int:page>/')
def consume_info(page=None):
    if page is None:
        page = 1
    consume = db.session.query(Consume, Credit).filter(Consume.credit_id == Credit.credit_id).order_by(
        Consume.consume_date.desc()).paginate(page=page, per_page=3)

    return render_template('admin/consume-info.html', consumeData=consume)


# 添加消费信息
@admin.route('/addConsume', methods=['GET', 'POST'])
def add_consume():
    form = ConsumeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            datas = form.data
            conInfo = Consume(credit_id=datas['creditId'], consume_date=datas['date'], sum_money=datas['money'],
                              Ctype=datas['selectType'])
            db.session.add(conInfo)
            db.session.commit()
            return redirect(url_for('admin.consume_info', page=1))
    return render_template('admin/add-consume.html', form=form)


# 退出
@admin.route('/loginOut')
def login_out():
    session.pop('admin', None)
    return redirect(url_for('admin.index'))
