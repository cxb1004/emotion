from enum import Enum, unique

@unique
class VoState(Enum):
    SUCCESS = (200, "成功")
    FAILURE = (500, "失败"),
    UNKNOWN_EXCEPTION = (501, "未知错误")
    USER_NO_ACCESS = (502, "用户无权访问")
    PARAMETER_ERROR = (503, "参数错误")
    NO_COMPANY_FOUND = (504, "未查询到该公司")

if __name__ == '__main__':
    print(VoState['SUCCESS'].value[0])
    print(VoState['SUCCESS'].value[1])
