# 导入蓝图
from flask import Blueprint
import application.admin.views

admin = Blueprint('admin', __name__)  # 定义个人信息蓝图
