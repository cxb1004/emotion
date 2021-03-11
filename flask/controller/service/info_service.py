from mapper.info_mapper import infoMapper
class info_service(object):
    def __init__(self):
        print()

    def selectComLabelByComId(self,companyId):

        return infoMapper.selectComLabelByComId(companyId)

infoService = info_service()