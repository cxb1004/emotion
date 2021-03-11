# import sys
# import os
# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
from flask import Blueprint,render_template,request
import uuid
import datetime


from utils.result_json import vo
from utils.LoginStatus import VoState
from utils.utils import util
from service.f_sqlAlchemy_service import fSqlAlchemy_service
from config.app_config import create_app

"""sqlAlchemy接口demo"""


app = create_app()
sqlAlchemyModule = Blueprint('sqlAlchemyModule', __name__)

"""按公司id查询"""
@sqlAlchemyModule.route("/selectComLabelByComId", methods=['POST'])
def selectComLabelByComId():
    """获取参数"""
    companyId = request.values.get("companyId")
    if util.str_isNull(companyId):
        return vo.JSONResultVo(VoState.PARAMETER_ERROR, None)
    info = fSqlAlchemy_service.selectComLabelByComId(companyId)
    print('f_sqlAlchemy_controller_selectComLabelByComId_info:%s'(info))

    return vo.JSONResultVo(VoState.SUCCESS,str(info))

"""插入数据"""
@sqlAlchemyModule.route("/insertComLabel", methods=['POST'])
def insertComLabel():
    """获取参数"""
    companyId = request.values.get("companyId")
    industryOne = request.values.get("industryOne")
    industryTwo = request.values.get("industryTwo")
    if util.str_isNull(companyId):
        return vo.JSONResultVo(VoState.PARAMETER_ERROR, None)
    param_dict = dict()
    param_dict.setdefault('id', str(uuid.uuid1()).replace('-', ''))

    param_dict.setdefault('company_id', companyId)
    param_dict.setdefault('industry_one', industryOne)
    param_dict.setdefault('industry_two', industryTwo)
    param_dict.setdefault('update_time', datetime.datetime.now())
    print("insertComLabel_param_dict:%s" %(param_dict))
    app.logger.info("f_sqlAlchemy_controller_insertComLabel_param_dict:%s" %(param_dict))


    resout = fSqlAlchemy_service.insertComLabel(param_dict)


    return resout







