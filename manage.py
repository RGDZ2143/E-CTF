# -*- coding: utf-8 -*-
'''
-------------------------------------------------
    File name     manage.py
    Description : 
    Author :      RGDZ 
    Date :   2019/02/20
-------------------------------------------------
    Version : 
    Contact :   rgdz.gzu@qq.com
    License :   (C)Copyright 2018-2019
-------------------------------------------------
'''

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from app.models import *


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('app', MigrateCommand)


if __name__ == "__main__":
    manager.run()