from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField  # 添加字段
from wtforms.validators import DataRequired, EqualTo, ValidationError  # 导入验证器
from application.models import Admin


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
    title=StringField(
        
    )