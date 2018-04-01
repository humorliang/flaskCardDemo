from flask import Flask
# 导入蓝图,要具体到__init__
from application.admin.__init__ import admin as admin_blueprint
from application.home.__init__ import home as home_blueprint
from application.exts import db
import application.config as config

app = Flask(__name__)
# 导入配置文件
app.config.from_object(config)
db.init_app(app)

# 在app中注册蓝图
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')
