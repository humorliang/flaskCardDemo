from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, PasswordField, SubmitField  # 添加字段
from wtforms.validators import DataRequired, URL, Email, NumberRange, ValidationError, EqualTo, Length  # 导入验证器
from application.models import Admin, User, Credit
from flask import session
import re


# 信用卡验证器
def validate_credit(form, field):
    data = field.data
    credit_info = Credit.query.filter_by(credit_id=data).count()
    credit_status = Credit.query.filter_by(credit_id=data, cdt_status=1).count()
    if credit_info == 0:
        raise ValidationError('此卡不存在')
    elif credit_status == 0:
        raise ValidationError('此卡被冻结')


# 数字验证器
def validate_is_num(form, field):
    data = field.data
    if re.match(r'[0-9]+$', data) is None:
        raise ValidationError('请输入正确的金额')


# 定义登陆表单
class LoginForm(FlaskForm):
    username = StringField(
        validators=[
            DataRequired('请输入用户名')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入用户名'
        }
    )
    password = PasswordField(
        validators=[
            DataRequired('请输入密码')
        ],
        description='密码',
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入密码'
        }
    )
    submit = SubmitField(
        label='登陆',
        description='登陆',
        render_kw={
            'class': 'btn btn-primary',
            'style': "width:150px;"
        }
    )

    def validate_username(self, field):
        username = field.data
        user = Admin.query.filter_by(username=username).count()
        if user == 0:
            raise ValidationError('用户名不存在')


# 银行信息表单
class AddNewsForm(FlaskForm):
    title = StringField(
        label='文章标题',
        validators=[
            DataRequired('请输入文章标题')
        ],
        render_kw={
            'class': "col-xs-6",
            'placeholder': "输入文章标题"
        }
    )
    url = StringField(
        label='文章链接',
        validators=[
            URL('请输入正确地址')
        ],
        render_kw={
            'class': "col-xs-6",
            'placeholder': "输入文章链接"
        }
    )
    newsDate = DateField(
        label='输入时间',
        validators=[
            DataRequired('请输入正确时间')
        ],
        render_kw={
            'class': "col-xs-6",
            'placeholder': "格式年-月-日'"
        }
    )
    submit = SubmitField(
        label='添加',
        description='添加',
        render_kw={
            'class': "btn btn-primary btn-width-margin"
        }
    )


# 修改密码
class EditPwdForm(FlaskForm):
    name = StringField(
        label='用户名',
        validators=[
            DataRequired('请输入用户名')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入用户名'
        }
    )
    old_pwd = PasswordField(
        validators=[
            DataRequired('请输入密码')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入旧密码'
        }
    )
    new_pwd = PasswordField(
        validators=[
            DataRequired('请输入新密码')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入新密码'
        }
    )
    new_pwd2 = PasswordField(
        validators=[
            DataRequired('请输入新密码'),
            EqualTo('new_pwd', message='两次密码不一致')

        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入新密码'
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': "btn btn-primary btn-width-margin"
        }
    )

    def validate_name(self, field):
        data = field.data
        user = Admin.query.filter_by(username=data).count()
        if user == 0:
            raise ValidationError('用户名不存在')

    def validate_old_pwd(self, field):
        data = field.data
        user = session.get('admin')
        a_user = Admin.query.filter_by(username=user).first()
        if not a_user.check_pwd(data):
            raise ValidationError('您输入的旧密码不正确')


# 信用卡表单
class AddCreditForm(FlaskForm):
    name = StringField(
        label='持卡人',
        validators=[
            DataRequired('请输入持卡人')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '持卡人'
        }
    )
    creditId = StringField(
        label='卡号',
        validators=[
            DataRequired('请输入卡号'),
            Length(min=19, max=19, message='请输入19位卡号')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入卡号'
        }
    )
    limit = StringField(
        label='额度',
        validators=[
            DataRequired('请输入额度'),
            Length(min=1, max=12, message='请输入1~12位')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入额度'
        }
    )
    idCard = StringField(
        label='身份证号',
        validators=[
            DataRequired('请输入身份证'),
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入身份证'
        }
    )
    phone = StringField(
        label='手机号',
        validators=[
            DataRequired('请输入手机号'),
            Length(min=11, max=11, message='请输入11位手机号')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入手机号'
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱'),
            Email('请输入正确的邮箱')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入邮箱'
        }
    )
    vailDate = DateField(
        label='有效期',
        validators=[
            DataRequired('请输入正确的日期'),
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '年-月-日'
        }
    )
    submit = SubmitField(
        label='添加',
        render_kw={
            'class': 'btn btn-primary btn-width-margin'
        }
    )

    # 手机号码验证器
    def validate_phone(self, field):
        phone = field.data
        ph = User.query.filter_by(phone=phone).count()
        if re.match(r'^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$', phone) is None:
            raise ValidationError('请输入正确的手机号')
        if ph == 0:
            raise ValidationError('此手机号码用户不存在')

    # 身份证验证器
    def validate_idCard(self, field):
        idCard = field.data
        if re.match(r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$', idCard) is None:
            raise ValidationError('请输入正确的身份证号')


# 欠款表单
class DebtForm(FlaskForm):
    creditId = StringField(
        label='卡号',
        validators=[
            DataRequired('请输入卡号'),
            validate_credit
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入卡号'
        }
    )
    money = StringField(
        validators=[
            DataRequired('请输入金额'),
            validate_is_num
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入金额'
        }
    )
    date = DateField(
        validators=[
            DataRequired('请输入正确的日期')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '格式年-月-日'
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': 'btn btn-primary btn-width-margin'
        }
    )


# 消费表单
class ConsumeForm(FlaskForm):
    creditId = StringField(
        label='卡号',
        validators=[
            DataRequired('请输入卡号'),
            validate_credit
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入卡号'
        }
    )
    money = StringField(
        validators=[
            DataRequired('请输入金额'),
            validate_is_num
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入金额'
        }
    )
    date = DateField(
        validators=[
            DataRequired('请输入正确的日期')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '格式年-月-日'
        }
    )
    selectType = SelectField(
        label='类型',
        choices=[
            ('购物', '购物'),
            ('交通', '交通'),
            ('旅游', '旅游'),
            ('其他', '其他'),
        ],
        render_kw={
            'class': 'col-xs-4'
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': 'btn btn-primary btn-width-margin'
        }
    )


# 账单表单
class DealForm(FlaskForm):
    creditId = StringField(
        label='卡号',
        validators=[
            DataRequired('请输入卡号'),
            validate_credit
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入卡号'
        }
    )
    money = StringField(
        validators=[
            DataRequired('请输入金额'),
            validate_is_num
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入金额'
        }
    )
    date = DateField(
        validators=[
            DataRequired('请输入日期')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '格式年-月-日'
        }
    )
    comment = StringField(
        validators=[
            DataRequired('请输入日期'),
            Length(max=15, message='请控制在10字之内')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '备注'
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': 'btn btn-primary btn-width-margin'
        }
    )
