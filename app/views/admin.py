# -*- coding: utf-8 -*-
'''
-------------------------------------------------
    File name     admin.py
    Description : 
    Author :      RGDZ 
    Date :   2019/02/21
-------------------------------------------------
    Version : 
    Contact :   rgdz.gzu@qq.com
    License :   (C)Copyright 2018-2019
-------------------------------------------------
'''

from flask import Blueprint, request, redirect, render_template, flash, url_for, jsonify
from werkzeug.utils import secure_filename
from app.models import db, Role, User, InviteCode, Notice, Challenge
from app.config import Config as CF
from app.func import *

import os
import base64
import shutil


admin = Blueprint('admin', __name__)



@admin.route('/setup/',methods=['GET','POST'])
def setup():
    """ 设置安装路由 """   
    if request.method == 'POST':
        admin_name = request.form.get('username')
        admin_email = request.form.get('email')
        admin_pass = request.form.get('password')
        admin_msg = User(username=admin_name, email=admin_email, set_password=admin_pass)
        admin_msg.role = Role.query.filter_by(name='ADMIN').first()
        db.session.add(admin_msg)
        db.session.commit()
        return redirect(url_for('user.login'))
    Role.insert_roles()
    return render_template('admin/setup.html')

@admin.route('/control/')
@limit_admin
def control():
    """ 后台管理页面路由 """
    return render_template('admin/control.html')


@admin.route('/control/create_invitecode', methods=['GET'])
@limit_admin
def create_invitecode():
    """ 生成邀请码 """
    if request.method == 'GET':
        new_code = base64.b64encode(os.urandom(128))
        new_invitecode = InviteCode(invitecode=new_code)
        db.session.add(new_invitecode)
        db.session.commit()
        return redirect(url_for('admin.control'))

@admin.route('/announce/', methods=['GET', 'POST'])
@limit_admin
def announce():
    """ 发布公告 """
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        if title == "":
            title = "最新公告"
        new_notice = Notice(title=title, body=body)
        db.session.add(new_notice)
        db.session.commit()
        return redirect(url_for('user.index'))
    return render_template('admin/announce.html')

@admin.app_context_processor
def notices():
    """ 声名公告变量 """
    notices = Notice.query.order_by(Notice.create_time.desc())
    if notices != None:
        return {'notices': notices}
    return {}


@admin.app_context_processor
def ret_invitecode():
    """ 返回邀请码数据 """
    invitecodes = InviteCode.query.order_by(InviteCode.id.desc())
    if invitecodes != None:
        return {'invitecodes': invitecodes}
    return {}


@admin.route('/control/user_msg/',methods=['GET','POST'])
@limit_admin
def user_msg():
    """ 用户信息console """
    if request.method == 'POST':
        pass
    return render_template('admin/user_msg.html')


@admin.app_context_processor
def ret_user_msg():
    """ 返回用户信息数据 """
    user_msgs = User.query.order_by()
    if user_msgs != None:
        role_msgs = Role.query.order_by()
        return {'user_msgs':user_msgs,'role_msgs':role_msgs}
    return {}


@admin.route('/control/challenge_msg',methods=['GET','POST'])
@limit_admin
def challenge_msg():
    """ 题目信息及上传题目文件 """          # TODO：后期改写为上传改写为ajax
    if request.method == 'POST':
        file = request.files['file']
        basepath = os.getcwd()
        upload_path = CF.UPLOAD_PATH + secure_filename(file.filename)
        download_path = CF.DOWNLOAD_PATH + secure_filename(file.filename)
        file.save(upload_path)
        shutil.copy(upload_path,download_path)
        return redirect(url_for('admin.challenge_msg'))
    return render_template('admin/challenge_msg.html')

@admin.route('/control/update_challenges',methods=['GET'])
@limit_admin
def update_challenges():
    """ 更新题目信息数据 """
    if request.method == 'GET':
        if exec_pwn_init(cmd_path=CF.CMD_PATH,file_path=CF.PWN_INIT_PATH,ret_path=CF.BASEPATH) == 0:
            msgs = deal_flags(CF.FLAG_PATH)
            if msgs:
                for msg in msgs:
                    flag = msg.get('flag')
                    port = msg.get('port')
                    name = msg.get('filename')
                    print(name)
                    challenge_old = Challenge.query.filter(Challenge.name == name).first()
                    print(challenge_old)
                    if challenge_old == None:
                        print(challenge_old)
                        addr = CF.IP_V6 + ': ' + str(port)
                        new_challenge = Challenge(name=name,flag=flag,address=addr)
                        db.session.add(new_challenge)
                        db.session.commit()
                return redirect(url_for('admin.challenge_msg'))
        return 500


@admin.app_context_processor
def ret_challenge_msg():
    """ 返回题目信息数据 """
    su_chall_user_num = {}
    challenges_msg = Challenge.query.order_by(Challenge.score.desc()).all()
    if challenges_msg:
        for challenge in challenges_msg:
            su_chall_user_num[challenge.id] = len(challenge.user.all()) 
        return {'challenges_msg':challenges_msg,'su_chall_user_num':su_chall_user_num}
    return {}


""" Ajax验证数据 """
@admin.route('/control/invitecodevalidate/invitecode', methods=['POST'])
@limit_admin
def check_invitecode():
    """ 检查邀请码数据 """
    if request.method == 'POST':
        query_code_id = request.get_json(force=True).get('input-invitecode')
        invitecode = InviteCode.query.filter(InviteCode.id == query_code_id).first()
        if invitecode != None:
            if invitecode.user_id != None:
                """ 带着user返回到前端 """
                invite_user = User.query.filter(User.id == invitecode.user_id).first()
                return jsonify({'user': invite_user.username, 'result': invitecode.invitecode})
            else:
                """ 返回invitecode到前端 """
                return jsonify({'user': None, 'result': invitecode.invitecode})
        else:
            return jsonify(False)



