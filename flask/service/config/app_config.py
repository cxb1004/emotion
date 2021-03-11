import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import CSRFProtect
import logging
import logging
import time

# 数据库
# db = SQLAlchemy()

app = Flask(__name__)
app.config["SQLALCHEMY_ECHO"] = False



# # 为flask补充csrf防护
# csrf = CSRFProtect()
# # 初始化
# csrf.init_app(app)

# """log"""
#
#
# # log配置，实现日志自动按日期生成日志文件
# def make_dir(make_dir_path):
#     path = make_dir_path.strip()
#     if not os.path.exists(path):
#         os.makedirs(path)
#     return path
#
#
# log_dir_name = "logs"
# log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
# log_file_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + os.sep + log_dir_name
# make_dir(log_file_folder)
# log_file_str = log_file_folder + os.sep + log_file_name
# log_level = logging.INFO
#
# handler = logging.FileHandler(log_file_str, encoding='UTF-8')
# handler.setLevel(log_level)
# logging_format = logging.Formatter(
#     '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
# handler.setFormatter(logging_format)
# app.logger.addHandler(handler)

logs_file_folder = rootPath + os.sep + "logs"
if not os.path.exists(logs_file_folder):
    os.makedirs(logs_file_folder)
logs_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
logs_file_str = logs_file_folder + os.sep + logs_file_name

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                        filename=logs_file_str,  # 将日志写入log_new.log文件中
                        filemode='w',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        # a是追加模式，默认如果不写的话，就是追加模式
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        # 日志格式
                        )

"""对外提供app"""
def create_app():

    return app

    # # 根据配置模式的名字获取配置参数类
    # config_class = config_map.get(config_name)
    # app.config.from_object(config_class)

    # # 使用app初始化db
    # db.init_app(app)
    # # 为flask补充csrf防护
    # csrf = CSRFProtect()



    # # 初始化
    # csrf.init_app(app)

    # from apps.cart import app_cart
    # from apps.order import app_order
    # from apps.goods import app_goods
    # from apps.user import app_user
    #
    # app.register_blueprint(app_cart, url_prefix='/cart')
    # app.register_blueprint(app_goods, url_prefix='/')
    # app.register_blueprint(app_order, url_prefix='/order')
    # app.register_blueprint(app_user, url_prefix='/user')




