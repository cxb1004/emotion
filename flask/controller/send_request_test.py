import json
import datetime
import logging

from flask import Blueprint,url_for,request,render_template,session,redirect
import time

from utils import logger
send_log = logger.send_log
from service.send_request_test_service import send_request_test_service


"""GET、POST请求及参数获取demo"""

# 创建了一个蓝图对象
sendRequestTestModule = Blueprint('sendRequestTestModule',__name__)

"""
    POST请求，带参数
"""
@sendRequestTestModule.route("/sendPost", methods=["POST"])
def post_test1():
    #默认返回内容
    return_dict = {'return_code':'200','return_info':'处理成功','result':None}
    id = request.values.get('id')
    name = request.values.get('name')
    stop_time = request.values.get('stop_time')

    # send_log.info({'name':name,'id':id,'new_time':time.time(),'stop_time':stop_time,'info':'start'})

    info = send_request_test_service.post_test1(id,name,stop_time)
    # send_log.info({'name':name,'id':id,'new_time':time.time(),'stop_time':stop_time,'info':'stop'})
    if int(id) == 0 or int(id) == 4999 or int(id) == 9999:
        send_log.info({'name':name,'id':id,'new_time':time.time()})

    # 对参数进行操作
    return_dict['result'] = str(info)
    logging.info(return_dict)
    return json.dumps(return_dict,ensure_ascii=False)
