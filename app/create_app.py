# -*- coding: utf-8 -*-
'''
-------------------------------------------------
    File name     create_app.py
    Description : 
    Author :      RGDZ 
    Date :   2019/02/20
-------------------------------------------------
    Version : 
    Contact :   rgdz.gzu@qq.com
    License :   (C)Copyright 2018-2019
-------------------------------------------------
'''

from flask import Flask
from app.config import Config
# from app.mail_config import mail
# from app.mail_config.config import MailConfig
from app.models import db


def register_blueprint(app):
    """ 注册蓝图 """
    from app.views.admin import admin
    from app.views.user import user
    app.register_blueprint(admin)
    app.register_blueprint(user)


def create_app():
    """ 组装app """
    app = Flask(__name__)
    app.config.from_object(Config)
    # app.config.from_object(MailConfig)
    db.init_app(app)
    # mail.init_app(app)
    register_blueprint(app)
    return app