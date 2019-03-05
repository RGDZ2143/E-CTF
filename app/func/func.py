# -*- coding: utf-8 -*-
'''
-------------------------------------------------
    File name     func.py
    Description : 
    Author :      RGDZ 
    Date :   2019/02/21
-------------------------------------------------
    Version : 
    Contact :   rgdz.gzu@qq.com
    License :   (C)Copyright 2018-2019
-------------------------------------------------
'''
import re
import os
import json
import requests

from flask import redirect, url_for, flash, session
from app.models import User, Role
from functools import wraps





def limit_setup(func):
    """ 限制安装 """
    @wraps(func)
    def wrapper(*args, **kwargs):
        admin = User.query.filter(User.id == 1).first()
        if admin != None:
            return func(*args, **kwargs)
        elif admin == None:
            return redirect(url_for('admin.setup'))
    return wrapper

def limit_admin(func):
    """ admin限制"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user.id')
        user_msg = User.query.filter_by(id=user_id).first()
        if user_msg:
            # 检查是否未管理员
            if user_msg.is_administrator():
                return func(*args, **kwargs)
            else:
                return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.login'))
            
    return wrapper

def limit_user(func):
    """ user限制 """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user.id')
        if user_id == None:
            return redirect(url_for('user.login'))
        elif user_id != None:
            return func(*args, **kwargs)
    return wrapper



def check_mail(str):
    """ 正则表达验证函数 """
    mail = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    if re.match(mail, str):
        return True
    else:
        return False


def exec_pwn_init(cmd_path,file_path,ret_path):
    """ 
    调用系统命令执行INIT_doploy的py文件 
    """
    try:
        commnd = "python2 "+file_path       #initialize.py 属于py-2版本 TODO:有时间改写为py-3
        os.chdir(cmd_path)
        ret_msg = os.system(commnd)
        os.chdir(ret_path)
    except:
        return False
    if ret_msg:
        return ret_msg
    return False
    
    

def deal_flags(file_path):
    """ 
    处理flags.txt 
    返回执行结果 msgs/False
    """
    msgs = []
    try:
        with open(file_path) as flags:
            for flag in flags:
                msgs.append(json.loads(flag))
    except FileNotFoundError:
        print('文件未找到，请检查路径!')
    if msgs == []:
        return False
    return msgs

def get_server_ip():
    """ 获取本机公网IP """
    try:
        ip = json.loads(requests.get('http://httpbin.org/ip').text).get('origin')[:15]
        if ip:
            return ip
    except:
        return None