# coding:utf-8
from application.__init__ import app
from datetime import timedelta
# 入口函数设置session过期时间
app.permanent_session_lifetime=timedelta(days=3)
if __name__ == '__main__':
    app.run()
