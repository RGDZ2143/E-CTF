# -*- coding: utf-8 -*-
'''
-------------------------------------------------
    File name     user.py
    Description : 
    Author :      RGDZ 
    Date :   2019/02/20
-------------------------------------------------
    Version : 
    Contact :   rgdz.gzu@qq.com
    License :   (C)Copyright 2018-2019
-------------------------------------------------
'''

from flask import Blueprint, redirect, render_template
from flask import request, jsonify, flash, url_for, session
from flask import send_file, send_from_directory
from app.models import db, User, InviteCode, Challenge
from app.config import Config as CF
from app.func import *
import os


user = Blueprint('user', __name__)


@user.route('/')
@user.route('/index/')
@limit_setup
def index():
    """ 主页路由 """
    return render_template('user/index.html')


@user.route('/login/', methods=['GET', 'POST'])
@limit_setup
def login():
    """ 登录页面路由 """
    if request.method == 'POST':
        username = request.form.get('username')
        userpass = request.form.get('userpass')
        user_msg = User.query.filter(User.username == username).first()
        if user_msg:
            if user_msg.check_password(userpass):
                session['user.id'] = user_msg.id
                session.permanent = True
                if user_msg.id == 1:
                    return redirect(url_for('admin.control'))
                return redirect(url_for('user.index'))  #TODO: 来自哪里跳回哪里
            else:
                return redirect(url_for('user.fuck'))        # TODO: 不要试图玩小动作
        else:
            return redirect(url_for('user.fuck'))        # TODO: 不要试图玩小动作
    return render_template('user/login.html')


@user.app_context_processor
def check_login():
    """ 检查登录session """
    user_id = session.get('user.id')
    if user_id == None:
        return {}
    else:
        user_msg = User.query.filter(User.id == user_id).first()
        return {'user_msg': user_msg}


@user.route('/poweroff/')
@limit_setup
def poweroff():
    """ 注销功能 """
    session.clear()
    return redirect(url_for('user.login'))


@user.route('/control/')
@limit_setup
def control():
    """ 用户面板 """
    user_id = session.get('user.id')
    if user_id != 1:
        return render_template('user/control.html')
    elif user_id == 1:
        return redirect(url_for('admin.control'))


@user.route('/register/', methods=['GET', 'POST'])
@limit_setup
def register():
    """ 注册页面路由 """
    if request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        useremail = request.form.get('email')
        userpass = request.form.get('password')
        code = request.form.get('invitecode')
        # 新建用户数据
        new_user = User(username=username, email=useremail, set_password=userpass)
        new_user.role = Role.query.filter_by(name='User').first()
        invitecode = InviteCode.query.filter(InviteCode.invitecode == code).first()
        new_user.invitecode = invitecode
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.login'))
    return render_template('user/register.html')


@user.route('/challenge/',methods=['GET'])
@limit_user
def challenges_page():
    """ 挑战页面路由 """
    if request.method == 'GET':
        return render_template('user/challenge.html')


@user.app_context_processor
def ret_challenge():
    """ 返回题目数据 """
    challenges = Challenge.query.filter().all()
    if challenges:
        challenge_num = len(tuple(challenges))
        return {'challenges':challenges, 'challenge_num':challenge_num}
    return {}


# @user.route("/download/",methods=['GET'])
# def download_file():
#     """ 下载文件 """
#     if request.method == 'GET':
#         filename = request.args.get('file')
#         directory = CF.DOWNLOAD_PATH
#         return  send_from_directory(directory, filename, as_attachment=True)


@user.route('/fuck/')
def error_fuck():
    return render_template('error/fuck.html')


@user.app_errorhandler(404)
def error_404(error):
    return render_template('error/404.html')

@user.app_errorhandler(500)
def error_505(error):
    return render_template('error/500.html')



""" Ajax注册验证 """
@user.route('/register/registervalidate/username',methods = ['POST'])
def va_re_username():
    """ 注册页面用户名验证 """
    #TODO: 检查输入的合法性
    if request.method == 'POST':
        username = request.get_json(force=True).get('username')
        if username:
            if User.query.filter(User.username == username).first():
                return jsonify(False)
            else:
                return jsonify(True)
        else:
            return jsonify(False)
    else:
        return jsonify(False)


@user.route('/register/registervalidate/email',methods=['POST'])
def va_re_email():
    """ 注册页面邮箱验证 """
    #TODO: 检查输入的合法性
    if request.method == 'POST':
        email = request.get_json(force=True).get('email')
        if check_mail(email):
            if User.query.filter(User.email == email ).first():
                return jsonify(False)
            else:
                return jsonify(True)
        else:
            return jsonify(False)
    else:
        return jsonify(False)



@user.route('/register/registervalidate/password-2',methods=['POST'])
def va_re_pass():
    """ 注册页面密码验证 """
    #TODO: 检查输入的合法性
    if request.method == 'POST':
        password_1 = request.get_json(force=True).get('password-1')
        password_2 = request.get_json(force=True).get('password-2')
        if password_1 != password_2:
            return jsonify(False)
        else:
            return jsonify(True)
    else:
        return jsonify(False)



@user.route('/register/registervalidate/invitecode',methods=['POST'])
def va_re_invitecode():
    """ 注册页面邀请码验证 """
    #TODO: 检查输入的合法性
    if request.method == 'POST':
        invitecode = request.get_json(force=True).get('invitecode')
        code = InviteCode.query.filter(InviteCode.invitecode == invitecode).first()
        if code != None:
            if code.user_id != None:
                return jsonify(False)
            else:
                return jsonify(True)
        else:
            return jsonify(False)
    else:
        return jsonify(False)

@user.route("/login/loginvalidate/username",methods=['POST'])
def va_lo_username():
    """ 登录页面用户名验证 """
    #TODO: 检查输入的合法性
    if request.method == 'POST':
        username = request.get_json(force=True).get('username')
        user_msg = User.query.filter(User.username == username).first()
        if user_msg != None:
            return jsonify(True)
        else:
            return jsonify(False)
    else:
        return jsonify(False)


@user.route('/login/loginvalidate/userpass',methods=['POST'])
def va_lo_userpass():
    """ 登录页面密码验证 """
    if request.method == 'POST':
        data = request.get_json(force=True)
        username = data.get('username')
        userpass = data.get('userpass')
        user_msg = User.query.filter(User.username == username).first()
        if user_msg != None:
            if user_msg.check_password(userpass):
                return jsonify(True)
            else:
                return jsonify(False)
        else:
            return jsonify(False)
    else:
        return jsonify(False)