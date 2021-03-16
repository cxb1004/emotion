# coding: utf-8
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath1 = os.path.split(curPath)[0]
rootPath2 = os.path.split(rootPath1)[0]
sys.path.append(rootPath2)

import configparser
import logging



try:
    config_path = rootPath2 + "/config.ini"
    cf = configparser.ConfigParser()
    cf.read(config_path)

    __user = cf.get('Mysql-Database', 'user'),
    __password = cf.get('Mysql-Database', 'password'),
    __host = cf.get('Mysql-Database', 'host'),
    __port = cf.get('Mysql-Database', 'port'),
    __database = cf.get('Mysql-Database', 'database'),
    __charset = cf.get('Mysql-Database', 'charset'),
    __log_path = cf.get('Logger-path', 'log_path'),
    __environment = cf.get('Run-environment', 'environment'),


    """Mysql"""
    user = __user[0]
    password = __password[0]
    host = __host[0]
    port = __port[0]
    database = __database[0]
    charset = __charset[0]

    """日志目录"""
    log_path = __log_path[0]

    """运行环境"""
    environment = __environment[0]

except Exception as e:
    logging.error('read_config_error:%s' % (e))
    sys.exit(1)





