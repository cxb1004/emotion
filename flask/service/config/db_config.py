# coding: utf-8
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from utils.utils import iniUtils
from config.app_config import create_app
app = create_app()


class Config(object):
    print("Config is running")
    """配置参数"""
    config_path = rootPath + "/config.ini"
    ini_utils = iniUtils(config_path)
    host = ini_utils.get_param('Mysql-Database', 'host')
    user = ini_utils.get_param('Mysql-Database', 'user')
    password = ini_utils.get_param('Mysql-Database', 'password')
    database = ini_utils.get_param('Mysql-Database', 'database')


    print('mysql://%s:%s@%s/%s' % (user, password, host, database))

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (user, password, host, database)
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = False
    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False