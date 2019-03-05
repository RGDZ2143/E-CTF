# -*- coding: utf-8 -*-
'''
-------------------------------------------------
    File name :     cs.py
    Description :     
    Author :    RGDZ
    Data :     2019/02/27
-------------------------------------------------
    Version :     
    Contact :     rgdz.gzu@qq.com
    License :    (C)Copyright 2018-2019
'''
from app.config import Config as CF
import json
from app.func import *
import os

# try:
#     with open(Cf.FLAG_PATH) as flags:
#         for flag in flags:
#             print(json.loads(flag))
# except FileNotFoundError:
#     print('文件未找到，请检查路径!')
# commnd = "python2 " + CF.INIT_PATH
# print(os.getcwd())
# os.chdir(CF.BASEPATH+'/pwn_deploy_chroot')
# os.system(commnd)
# print(os.getcwd())
# os.chdir
# print(os.getcwd())
exec_pwn_init(cmd_path=CF.CMD_PATH,file_path=CF.PWN_INIT_PATH,ret_path=CF.BASEPATH)
