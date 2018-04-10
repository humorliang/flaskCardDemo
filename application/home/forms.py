from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField, PasswordField, SubmitField  # 添加字段
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError  # 导入验证器
from application.models import User, ApplyCard
from flask import session
import re


# 自定义验证
# 数字验证器
def validate_is_num(form, field):
    data = field.data
    if re.match(r'[0-9]+$', data) is None:
        raise ValidationError('请填写数字')


# 手机号码验证器
def validate_is_phone(form, field):
    phone = field.data
    if re.match(r'^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$', phone) is None:
        raise ValidationError('请输入正确的手机号')


# 身份证验证器
def validate_is_idCard(form, field):
    idCard = field.data
    if re.match(r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$', idCard) is None:
        raise ValidationError('请输入正确的身份证号')


# 定义用户注册表单
class RegisterForm(FlaskForm):
    '''用户注册表单'''
    username = StringField(
        validators=[
            DataRequired('请请输入用户名')
        ],
        description='用户名',  # 表单可接受的值
        render_kw={
            'placeholder': "输入用户名",
            'class': 'col-xs-6'
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
    password2 = PasswordField(
        validators=[
            DataRequired('请输入密码'),
            EqualTo('password', message='两次密码不同')
        ],
        description='密码',
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '请输入密码'
        }
    )
    phone = StringField(
        validators=[
            DataRequired('请输入正确的手机号')
        ],
        description='手机号',
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '输入手机号',
            'min-length': '11',
            'max-length': '11'
        },

    )
    submit = SubmitField(
        label='注册',  # 相当于value属性
        render_kw={
            'class': 'btn btn-primary btn-width-margin'
        }
    )

    # 自定义验证器：格式validate_fieldName
    # class 内部定义不需要在字段内的validators声明
    # class外部定义需要在字段内部的validators声明

    def validate_username(self, field):
        username = field.data
        user = User.query.filter_by(username=username).count()
        if user != 0:
            raise ValidationError('用户名已存在')

    # 手机号码验证器
    def validate_phone(self, field):
        phone = field.data
        ph = User.query.filter_by(phone=phone).count()
        print(type(phone))
        if re.match(r'^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$', phone) is None:
            raise ValidationError('请输入正确的手机号')
        if ph != 0:
            raise ValidationError('此手机号码已注册')


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
    remember = BooleanField(
        label='记住密码',
        description='三天免登陆',
    )
    submit = SubmitField(
        label='登陆',
        description='登陆',
        render_kw={
            'class': 'btn btn-primary'
        }
    )

    def validate_username(self, field):
        username = field.data
        user = User.query.filter_by(username=username).count()
        if user == 0:
            raise ValidationError('用户名不存在')


# 个人信息
class AddInfoForm(FlaskForm):
    name = StringField(
        validators=[
            DataRequired('请填写姓名')
        ],
        render_kw={
            'placeholder': '姓名'
        }
    )
    sex = SelectField(
        choices=[
            ('0', '女'),
            ('1', '男')
        ]
    )
    age = StringField(
        validators=[
            DataRequired('请填写年龄'),
            validate_is_num,
            Length(max=3, message='请填写正确的年龄')
        ],
        render_kw={
            'placeholder': '年龄'
        }
    )
    email = StringField(
        validators=[
            DataRequired('请填写正确邮箱'),
            Email(message='请填写正确邮箱')
        ],
        render_kw={
            'placeholder': '邮箱'
        }
    )
    job = StringField(
        validators=[
            DataRequired('请填写职业')
        ],
        render_kw={
            'placeholder': '职业'
        }
    )
    IDCard = StringField(
        validators=[
            DataRequired('请填写身份证'),
            validate_is_idCard
        ],
        render_kw={
            'placeholder': '身份证'
        }
    )
    phone = StringField(
        validators=[
            DataRequired('请填写手机'),
            validate_is_phone
        ],
        render_kw={
            'placeholder': '手机号'
        }
    )
    address = StringField(
        validators=[
            DataRequired('请填写地址')
        ],
        render_kw={
            'placeholder': '地址'
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': 'btn btn-primary col-xs-offset-10'
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
            'placeholder': '请确认新密码'
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
        user = User.query.filter_by(username=data).count()
        if user == 0:
            raise ValidationError('用户名不存在')

    def validate_old_pwd(self, field):
        data = field.data
        user = session.get('user')
        a_user = User.query.filter_by(username=user).first()
        if not a_user.check_pwd(data):
            raise ValidationError('您输入的旧密码不正确')


# 申请表单
class ApplyForm(FlaskForm):
    name = StringField(
        validators=[
            DataRequired('请填写申请人')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '申请人'
        }
    )
    limit = StringField(
        validators=[
            DataRequired('请填写额度'),
            validate_is_num
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '额度'
        }
    )
    idCard = StringField(
        validators=[
            DataRequired('请填写身份证号'),
            validate_is_idCard
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '身份证号'
        }
    )
    phone = StringField(
        validators=[
            DataRequired('请填写手机号')
        ],
        render_kw={
            'class': 'col-xs-6',
            'placeholder': '手机号'
        }
    )
    submit = SubmitField(
        label='提交',
        render_kw={
            'class': "btn btn-primary btn-width-margin"
        }
    )

    def validate_phone(self, field):
        phone = field.data
        ph = User.query.filter_by(phone=phone).count()
        if re.match(r'^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$', phone) is None:
            raise ValidationError('请输入正确的手机号')
        if ph == 0:
            raise ValidationError('请输入在用户注册时手机号')

    def validate_idCard(self, filed):
        id_card = filed.data
        num = ApplyCard.query.filter_by(idcard=id_card).count()
        if num == 3:
            raise ValidationError('此身份证已达申请上限3次')
