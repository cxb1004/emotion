import json


def jsonResultVo(code, message, data):
    return_dict = {'code': code, 'info': message, 'data': data}
    return json.dumps(return_dict, ensure_ascii=False)
