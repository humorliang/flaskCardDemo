# coding:utf-8
# 管理器
# 导入app,这里的app是Flask对象创建的,这里必须要用__init__导入模块
from application.__init__ import app
# 导入flask脚本管理器
from flask_script import Manager
# 导入数据库迁移
from flask_migrate import Migrate, MigrateCommand
# 导入db对象
from application.exts import db

# 将app导入到db中
db.init_app(app)
# 迁徙管理器app与db绑定
migrate = Migrate(app, db)

# flask 脚本命令
manger = Manager(app)
manger.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # 1.初始化 manage.py db init
    # 2.数据库迁徙 manage.py db migrate
    # 3.数据库更新 manage.py db upgrade
    manger.run()
