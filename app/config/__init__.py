# -*- coding: utf-8 -*-
'''
-------------------------------------------------
    File name     __init__.py
    Description : 
    Author :      RGDZ 
    Date :   2019/02/20
-------------------------------------------------
    Version : 
    Contact :   rgdz.gzu@qq.com
    License :   (C)Copyright 2018-2019
-------------------------------------------------
'''

import os
from app.func import get_server_ip


class Config:
    """ 基本配置 """
    DEBUG = True

    """ 本机公网IP """
    IP_V6 = get_server_ip()

    """ session配置  """
    SECRET_KEY = os.urandom(24)
    PERMANENT_SESSION_LIFETIME = 604800 #过期时间一个星期

    """ 数据库配置 """
    HOST = 'localhost'
    PORT = '3306'
    DATABASE = 'ectf'
    USERNAME = 'root'
    PASSWORD = 'root'
    DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """ 上传下载文件夹路径配置 """
    BASEPATH = os.getcwd()
    DOWNLOAD_PATH = BASEPATH + '/download/challenge/'
    UPLOAD_PATH = BASEPATH + '/pwn_deploy_chroot/bin/'

    """ initialize.py文件路径 """
    CMD_PATH = BASEPATH+'/pwn_deploy_chroot'             #针对initialize.py
    PWN_INIT_PATH = BASEPATH + '/pwn_deploy_chroot/initialize.py'

    """ flags.txt 文件路径 """
    FLAG_PATH = BASEPATH+'/pwn_deploy_chroot/flags.txt'
    