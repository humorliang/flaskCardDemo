from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField  # 添加字段
from wtforms.validators import DataRequired, EqualTo, ValidationError  # 导入验证器
from application.models import User
import re


# 定义注册表单
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
