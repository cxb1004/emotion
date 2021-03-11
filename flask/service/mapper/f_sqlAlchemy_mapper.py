from utils.utils import dict_utils
from model.model import *

class f_sqlAlchemy_mapper(object):

    def selectComLabelByComId(self,companyId):
        # print("mapper is running....")
        # #条件查询
        u2 = CcsCompanyLabel.query.filter_by(company_id=companyId).all()

        return dict_utils().queryToDict(u2)
        # return "{name:12}";

    def insertComLabel(self,param_dict):
        """"""
        len = db.session.bulk_insert_mappings(
            CcsCompanyLabel,
            [param_dict]
        )
        db.session.commit()
        app.logger.info("f_sqlAlchemy_mapper_insertComLabel_len:%s" %(len))
        return len



fSqlAlchemyMapper = f_sqlAlchemy_mapper()