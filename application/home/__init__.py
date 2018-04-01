# 导入蓝图
from flask import Blueprint
import application.home.views

home = Blueprint('home', __name__)  # 定义个人信息蓝图
