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
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import os
import base64
import datetime


db = SQLAlchemy()


registrations = db.Table('registrations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenges.id'))
)

class Permission:
    """ 权限值 """
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    """ 建立角色数据模型 """
    __tablename__ = "roles"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10))
    default = db.Column(db.Boolean,default=False,index=True) # 只设置给一个用户，其他用户都是False，因为app 会去搜索这个值，因此设置为 index 方便查找
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __init__(self,**kw):
        super(Role,self).__init__(**kw)
        if self.permissions is None:
            self.permissions = 0

    # 判断是否含有权限  
    def has_permission(self,perm):
        return self.permissions & perm == perm

    # 添加权限
    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permissions += perm
    # 移除权限
    def remove_permission(self,perm):
        if self.has_permission(perm):
            self.permissions -= perm

    # 重置权限
    def reset_permission(self):
        self.permissions = 0    
    
   
    # 插入角色
    @staticmethod
    def insert_roles():
        roles = {
            "User":[
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
            ],
            "Moderator":[
                Permission.MODERATE
            ],
            "Admin":[
                Permission.FOLLOW,
                Permission.COMMENT,
                Permission.WRITE,
                Permission.MODERATE,  
                Permission.ADMIN,          
            ]
        }
        # 默认角色是用户
        default_role = 'User'
        for r in roles:
            # 搜索三种角色，在数据库表的存在
            role = Role.query.filter_by(name=r).first()
            # 如果不存在这种角色，马上添加进去，方便以后拓展
            if role is None:
                role = Role(name=r)
            
            # 重置权限
            role.reset_permission()
            for perm in roles[r]:
                # 权限重新一个个加进去
                role.add_permission(perm)
            
            # 将默认用户写进数据库
            role.default = (role.name == default_role)
            db.session.add(role)
        
        db.session.commit()


class User(db.Model):
    """ 用户数据模型 """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    score = db.Column(db.Integer)
    invitecode = db.relationship('InviteCode', backref='user', uselist=False)
    challenges = db.relationship('Challenge', secondary=registrations,
                        backref=db.backref('user', lazy='dynamic'),
                        lazy='dynamic')
                        
    def __init__(self, **kw):
        super(User, self).__init__(**kw)
        # 如果用户的角色不存在者分配未默认user
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()
    
    def check_permists(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.check_permists(Permission.ADMIN)
    
    @property
    def password(self):
        raise AttributeError("password is not readable attribute")

    ####密码安全处理####
    @password.setter
    def set_password(self, password):
        """ hash处理密码 """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """ 查询密码 """
        return check_password_hash(self.password_hash, password)



class Challenge(db.Model):
    """ 题目数据模型 """
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50),nullable=True)
    address = db.Column(db.String(200))
    flag = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)


class InviteCode(db.Model):
    """ 邀请码数据 """
    __tablename__ = 'invitecodes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invitecode = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    

    @property
    def code(self):
        raise AttributeError("code is not readable attribute")

    @code.setter
    def create_code(self):
        self.invitecode = base64.b64decode(os.urandom(128))
    

class Notice(db.Model):
    """ 公告数据模型 """
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(500), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)