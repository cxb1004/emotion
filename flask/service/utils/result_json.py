import json
class resultVo(object):
    # def __init__(self, message, data):
    #
    #     self.code = message.value[0]
    #     self.info = message.value[1]
    #     self.data = data


    def JSONResultVo(self, message, data):
        return_dict = {'code': message.value[0], 'info': message.value[1], 'data': data}
        return json.dumps(return_dict, ensure_ascii=False)

vo = resultVo()