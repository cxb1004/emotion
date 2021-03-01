import os
import re

from common.log import Log

log = Log()


def removeFileIfExists(filePath):
    """
    如果文件已经存在，就删除文件
    :param filePath:
    :return:
    """
    if os.path.isfile(filePath):
        os.remove(filePath)
        log.debug('删除已经存在的文件{}'.format(filePath))


def replaceMutiSpace(str):
    """
    多个空格替换成单个空格
    :param str:
    :return:
    """
    str = re.sub(' +', ' ', str)
    return str


def remove53Emoji(str):
    """
    移除53自定义的表情符号
    :param str:
    :return:
    """
    patten = re.compile('{53b#\d*#}')
    str = re.sub(patten, '', str)
    return str


def isFileExist(file):
    """
    判断文件是否存在
    :param file:
    :return:
    """
    if os.path.isfile(file):
        return True
    return False

# txt = 'Hi~您好呀亲，我这边是官网小编，您是想拍婚纱照吗？{53b#32#}拍婚纱'
# print(removeEmoji(txt))
