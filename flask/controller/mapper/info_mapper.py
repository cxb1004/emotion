from utils.db_utlis import db

class info_mapper(object):


    def selectComLabelByComId(self,companyId):
        print()
        sql = 'SELECT * FROM `ccs_company_label` WHERE company_id in (%s)'
        return db.fetchall(sql,companyId)

infoMapper = info_mapper()