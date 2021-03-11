from utils.result_json import vo
from utils.LoginStatus import VoState
from mapper.f_sqlAlchemy_mapper import fSqlAlchemyMapper

class f_sqlAlchemy_service(object):


    def selectComLabelByComId(self,companyId):
        print("service is running:{0}".format(companyId))
        return fSqlAlchemyMapper.selectComLabelByComId(companyId)

    def insertComLabel(self,param_dict):
        """"""
        len = fSqlAlchemyMapper.insertComLabel(param_dict)

        return vo.JSONResultVo(VoState.SUCCESS, None)


fSqlAlchemy_service = f_sqlAlchemy_service()