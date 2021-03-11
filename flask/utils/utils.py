import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import logging
from logging import handlers
import time
import configparser

from datetime import datetime as cdatetime  # 有时候会返回datatime类型
# from datetime import date, time
from datetime import date as cdate, time as ctime
from flask_sqlalchemy import Model
from sqlalchemy import DateTime, Numeric, Date, Time  # 有时又是DateTime



class utils:

    """创建文件夹"""
    def make_dir(self, make_dir_path):
        path = make_dir_path.strip()
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    """判断字符是否为空"""
    def str_isNull(self,st):
        if st == None or st == '':
            return True
        return False



class dict_utils(object):

    def queryToDict(self, models):
        if models is None:
            return ""
        if (isinstance(models, list)):
            if (len(models) == 0):
                return ""
            elif (isinstance(models[0], Model)):
                lst = []
                for model in models:
                    gen = self.model_to_dict(model)
                    dit = dict((g[0], g[1]) for g in gen)
                    lst.append(dit)
                return lst
            else:
                res = self.result_to_dict(models)
                return res
        else:
            if (isinstance(models, Model)):
                gen = self.model_to_dict(models)
                dit = dict((g[0], g[1]) for g in gen)
                return dit
            else:
                res = dict(zip(models.keys(), models))
                self.find_datetime(res)
                return res

    # 当结果为result对象列表时，result有key()方法
    def result_to_dict(self, results):
        res = [dict(zip(r.keys(), r)) for r in results]
        # 这里r为一个字典，对象传递直接改变字典属性
        for r in res:
            self.find_datetime(r)
        return res

    def model_to_dict(self, model):  # 这段来自于参考资源
        for col in model.__table__.columns:
            if isinstance(col.type, DateTime):
                value = self.convert_datetime(getattr(model, col.name))
            elif isinstance(col.type, Numeric):
                value = float(getattr(model, col.name))
            else:
                value = getattr(model, col.name)
            yield (col.name, value)

    def find_datetime(self, value):
        for v in value:
            if (isinstance(value[v], cdatetime)):
                value[v] = self.convert_datetime(value[v])  # 这里原理类似，修改的字典对象，不用返回即可修改

    def convert_datetime(self, value):
        if value:
            if (isinstance(value, (cdatetime, DateTime))):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            elif (isinstance(value, (cdate, Date))):
                return value.strftime("%Y-%m-%d")
            elif (isinstance(value, (Time, time))):
                return value.strftime("%H:%M:%S")
        else:
            return ""


class iniUtils(object):
    def __init__(self, config_path):
        """"""
        self.config_path = config_path

    def get_param(self, key, value):
        """"""

        try:
            cf = configparser.ConfigParser()
            cf.read(self.config_path)
            value_ = cf.get(key, value)
            resout = value_
            return resout
        except Exception as e:
            print(e)
            return ""





"""flask日志"""
class Logger_flask(object):
    def make_dir(self, make_dir_path):
        path = make_dir_path.strip()
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_handler(self):
        log_dir_name = os.sep + "logs"
        log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
        log_file_folder = rootPath + log_dir_name
        print('######%s' %(log_file_folder))
        self.make_dir(log_file_folder)
        log_file_str = log_file_folder + os.sep + log_file_name
        log_level = logging.INFO

        handler = logging.FileHandler(log_file_str, encoding='UTF-8')
        handler.setLevel(log_level)
        logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
        handler.setFormatter(logging_format)
        return handler





# """之前日志"""
# class Logger(object):
#     level_relations = {
#         'debug': logging.DEBUG,
#         'info': logging.INFO,
#         'warning': logging.WARNING,
#         'error': logging.ERROR,
#         'crit': logging.CRITICAL
#     }  # 日志级别关系映射
#
#     def __init__(self, root_path, level='info', when='D', backCount=3,
#                  fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
#
#         log_file = ''
#         try:
#             config_path = rootPath + "/config.ini"
#             cf = configparser.ConfigParser()
#             cf.read(config_path)
#             log_file = cf.get("Logger-path", "log_file")
#         except Exception as e:
#             print(e)
#
#
#
#
#         log_date = time.strftime("%Y%m%d")
#         log_datetime = time.strftime("%Y%m%d_%H%M%S")
#         log_path = log_file + '/log/' + log_date
#         if not os.path.exists(log_path):
#             os.makedirs(log_path)
#
#         filename = log_path + '/log_' + log_datetime + '.log'
#         self.logger = logging.getLogger(filename)
#         format_str = logging.Formatter(fmt)  # 设置日志格式
#         self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
#         sh = logging.StreamHandler()  # 往屏幕上输出
#         sh.setFormatter(format_str)  # 设置屏幕上显示的格式
#         th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
#                                                encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
#         # 实例化TimedRotatingFileHandler
#         # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
#         # S 秒
#         # M 分
#         # H 小时、
#         # D 天、
#         # W 每星期（interval==0时代表星期一）
#         # midnight 每天凌晨
#         th.setFormatter(format_str)  # 设置文件里写入的格式
#         self.logger.addHandler(sh)  # 把对象加到logger里
#         self.logger.addHandler(th)



util = utils()