from . import index_blu
from .model import CcsCompanyLabel
from application import db
from application import VoState
from application import resultVo
from application import utils

from flask import render_template,request
import uuid
import logging
import datetime



@index_blu.route("/")
def index():
    return "首页"


@index_blu.route("/index_test", methods=['GET'])
def test():
    logging.info("$$$$$$$$$$$$$$$")
    return "success"

"""按公司id查询"""
@index_blu.route("/selectComLabelByComId", methods=['POST'])
def selectComLabelByComId():
    """获取参数"""
    companyId = request.values.get("companyId")
    print("@@@@@@@@@@@@%s" %(companyId))

    if utils().str_isNull(companyId):
        return resultVo().JSONResultVo(VoState.PARAMETER_ERROR, None)
    query = CcsCompanyLabel.query.filter_by(company_id=companyId).all()

    info = utils().queryToDict(query)

    logging.info('index_blu_selectComLabelByComId_info:%s' %(info))
    return resultVo().JSONResultVo(VoState.SUCCESS,str(info))

    # return resultVo().JSONResultVo(VoState.SUCCESS,str(companyId))


"""插入数据"""
@index_blu.route("/insertComLabel", methods=['POST'])
def insertComLabel():
    """获取参数"""
    companyId = request.values.get("companyId")
    industryOne = request.values.get("industryOne")
    industryTwo = request.values.get("industryTwo")
    if utils().str_isNull(companyId):
        return resultVo().JSONResultVo(VoState.PARAMETER_ERROR, None)
    param_dict = dict()
    param_dict.setdefault('id', str(uuid.uuid1()).replace('-', ''))
    param_dict.setdefault('company_id', companyId)
    param_dict.setdefault('industry_one', industryOne)
    param_dict.setdefault('industry_two', industryTwo)
    param_dict.setdefault('update_time', datetime.datetime.now())
    logging.info("index_blu_insertComLabel_param_dict:%s" %(param_dict))

    len = db.session.bulk_insert_mappings(
        CcsCompanyLabel,
        [param_dict]
    )
    db.session.commit()

    return resultVo().JSONResultVo(VoState.SUCCESS, len)

"""根据id删除数据"""
@index_blu.route('/deleteById', methods=['POST'])
def deleteById():
    """获取参数"""
    id = request.values.get("id")
    logging.info("index_blu_deleteById_param_id:%s" %(id))

    if utils().str_isNull(id):
        return resultVo().JSONResultVo(VoState.PARAMETER_ERROR, None)
    d1 = CcsCompanyLabel.query.filter_by(id=id).delete()
    logging.info("index_blu_deleteById_param_d1:%s" %(d1))

    db.session.commit()

    return resultVo().JSONResultVo(VoState.SUCCESS, d1)


"""根据id修改数据"""
@index_blu.route('/updateById', methods=['POST'])
def updateById():
    """获取参数"""
    id = request.values.get("id")
    industryOne = request.values.get("industryOne")
    industryTwo = request.values.get("industryTwo")
    logging.info("index_blu_updateById_id:%s" % (id))

    if utils().str_isNull(id):
        return resultVo().JSONResultVo(VoState.PARAMETER_ERROR, None)
    param_dict = dict()
    param_dict.setdefault('industry_one', industryOne)
    param_dict.setdefault('industry_two', industryTwo)
    param_dict.setdefault('update_time', datetime.datetime.now())
    logging.info("index_blu_updateById_param_dict:%s" % (param_dict))


    p1 = CcsCompanyLabel.query.filter_by(id=id).update(param_dict)
    db.session.commit()

    return resultVo().JSONResultVo(VoState.SUCCESS, p1)
