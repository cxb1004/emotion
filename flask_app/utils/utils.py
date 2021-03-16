import os
import time
from datetime import datetime as cdatetime  # 有时候会返回datatime类型
from sqlalchemy import DateTime, Numeric, Date, Time  # 有时又是DateTime
from datetime import date as cdate, time as ctime
from flask_sqlalchemy import Model

class utils(object):

    """创建文件夹"""

    def make_dir(self, make_dir_path):
        path = make_dir_path.strip()
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    """判断字符是否为空"""
    def str_isNull(self, st):
        print('##############%s' %(st))
        if st == None or st == '':
            return True
        return False

    """集合化查询结果"""

    def queryToDict(self, models):
        if models is None:
            return ""
        if (isinstance(models, list)):
            if (len(models) == 0):
                return ""
            elif (isinstance(models[0], Model)):
                lst = []
                for model in models:
                    gen = self.__model_to_dict(model)
                    dit = dict((g[0], g[1]) for g in gen)
                    lst.append(dit)
                return lst
            else:
                res = self.__result_to_dict(models)
                return res
        else:
            if (isinstance(models, Model)):
                gen = self.__model_to_dict(models)
                dit = dict((g[0], g[1]) for g in gen)
                return dit
            else:
                res = dict(zip(models.keys(), models))
                self.__find_datetime(res)
                return res

    # 当结果为result对象列表时，result有key()方法
    def __result_to_dict(self, results):
        res = [dict(zip(r.keys(), r)) for r in results]
        # 这里r为一个字典，对象传递直接改变字典属性
        for r in res:
            self.__find_datetime(r)
        return res

    def __model_to_dict(self, model):  # 这段来自于参考资源
        for col in model.__table__.columns:
            if isinstance(col.type, DateTime):
                value = self.__convert_datetime(getattr(model, col.name))
            elif isinstance(col.type, Numeric):
                value = float(getattr(model, col.name))
            else:
                value = getattr(model, col.name)
            yield (col.name, value)

    def __find_datetime(self, value):
        for v in value:
            if (isinstance(value[v], cdatetime)):
                value[v] = self.__convert_datetime(value[v])  # 这里原理类似，修改的字典对象，不用返回即可修改

    def __convert_datetime(self, value):
        if value:
            if (isinstance(value, (cdatetime, DateTime))):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            elif (isinstance(value, (cdate, Date))):
                return value.strftime("%Y-%m-%d")
            elif (isinstance(value, (Time, time))):
                return value.strftime("%H:%M:%S")
        else:
            return ""





