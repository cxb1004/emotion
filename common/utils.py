import os
import re
import shutil
import time

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


def file_size_format(file):
    size = os.path.getsize(file)
    if size < 1000:
        return '%i' % size + 'size'
    elif 1000 <= size < 1000000:
        return '%.1f' % float(size / 1000) + 'KB'
    elif 1000000 <= size < 1000000000:
        return '%.1f' % float(size / 1000000) + 'MB'
    elif 1000000000 <= size < 1000000000000:
        return '%.1f' % float(size / 1000000000) + 'GB'
    elif 1000000000000 <= size:
        return '%.1f' % float(size / 1000000000000) + 'TB'


def file_update_time_format(file):
    mtime = os.stat(file).st_mtime
    file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
    return file_modify_time


def get_timestamp(format=None):
    t = time.time()
    if format is None:
        return t
    elif format == 's':
        # 返回秒级时间戳
        return int(t)
    elif format == 'ms':
        # 返回毫秒级时间戳
        return int(round(t * 1000))
    elif format == 'y-m-dhms':
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
    elif format == 'y-m-d':
        return time.strftime("%Y-%m-%d", time.localtime(t))
    elif format == 'ymd':
        return time.strftime("%Y%m%d", time.localtime(t))
    elif format == 'ymdhms':
        return time.strftime("%Y%m%d%H%M%S", time.localtime(t))


def copyFile(file=None, path=None, is_overwrite=False):
    # 检查待复制的文件是否存在
    if not isFileExist(file):
        raise Exception('待复制的文件不存在！')

    # 获得相同的文件名
    file_name = os.path.basename(file)
    target_file = os.path.join(path, file_name)

    # 判断目标文件是否存在
    if isFileExist(target_file):
        if not is_overwrite:
            # 如果允许覆盖，就执行覆盖操作（先删除，后复制）
            removeFileIfExists(target_file)
        else:
            # 如果不允许覆盖，就抛出异常
            raise Exception('目标目录该文件已经存在，无法复制！')

    shutil.copyfile(file, target_file)

# print(get_timestamp())
# print(get_timestamp('s'))
# print(get_timestamp('ms'))
# print(get_timestamp('ymdhms'))
# print(get_timestamp('y-m-d'))
# print(get_timestamp('ymd'))
