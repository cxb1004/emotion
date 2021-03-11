import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from flask import Blueprint,render_template,request


from utils.result_json import vo
from utils.LoginStatus import VoState
from utils.db_utlis import db
from service.info_service import infoService
from utils.utils import util

"""传统dbUtils接口demo"""


infoModule = Blueprint('infoModule',__name__)

@infoModule.route("/selectComLabelByComId", methods=['POST'])
def selectComLabelByComId():
    """获取参数"""
    companyId = request.values.get("companyId")
    if util.str_isNull(companyId):
        return vo.JSONResultVo(VoState.PARAMETER_ERROR, None)

    info = infoService.selectComLabelByComId(companyId)
    print(info)

    return vo.JSONResultVo(VoState.SUCCESS,str(info))



@infoModule.route("/register", methods=["POST"])
def register():
    sql = 'SELECT * FROM `ccs_company_label` LIMIT 5'
    result = db.fetchall(sql)
    # print(result)
    for map in result:
        print(map.get('company_id'))

    return str(result)


