from mapper.f_sqlAlchemy_mapper import fSqlAlchemyMapper
import time

class send_request_test_service(object):

    def post_test1(self,id,name,stop_time):
        time.sleep(int(stop_time))
        companyId = ''
        if name =='send1':
            companyId = '72080513'
        elif name == 'send2':
            companyId = '72151635'
        elif name == 'send3':
            companyId = '72210373'

        return fSqlAlchemyMapper.selectComLabelByComId(companyId)



send_request_test_service = send_request_test_service()