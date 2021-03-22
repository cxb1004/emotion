import configparser
import os


class ProjectConfig:
    _cf = None

    def __init__(self):
        if ProjectConfig._cf is None:
            try:
                # 拼接获得config.ini路径
                __CONFIG_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
                __CONFIG_FILE_NAME = 'config.ini'
                # 读入配置文件
                ProjectConfig._cf = configparser.RawConfigParser()
                ProjectConfig._cf.read(os.path.join(__CONFIG_FILE_PATH, __CONFIG_FILE_NAME), encoding='utf-8')
                print(
                    '读入config.ini配置：\n配置文件路径:{}\n配置文件版本:{}'.format(os.path.join(__CONFIG_FILE_PATH, __CONFIG_FILE_NAME),
                                                                   ProjectConfig._cf.get('version', 'name')))
            except Exception as e:
                print("载入配置文件失败: " + os.path.join(__CONFIG_FILE_PATH, __CONFIG_FILE_NAME))
                print(e)

    def get_value(self, section, option):
        try:
            value = ProjectConfig._cf.get(section, option)
            return value
        except Exception as e:
            print("配置文件中没有该配置内容: section[" + section + "] option: " + option)
            raise e
