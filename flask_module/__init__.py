"""
创建Flask App对象，包含如下功能：
1、logging日志功能
2、session、threaded配置
3、数据库配置
4、redis / kafka配置
"""

from flask import Flask

from flask_module.emotionclassify import EmotionClassify
from flask_module.flask_config import FlaskConfig

proj_config = None


def init_log(_config):
    pass


def init_app(_config):
    """初始化创建Flask对象"""
    app = Flask(__name__)

    global proj_config
    proj_config = _config

    # TODO 使用配置文件里的数据，生成app的config对象
    app_config = FlaskConfig(_config)

    # TODO 直接从配置文件读取
    app.config.from_object(app_config)

    init_log(proj_config)


    return app

# def getEmotionClassifyData(_txt):
#     global emotionClassify
#     if emotionClassify is None:
#         global proj_config
#         init_emotion_classify(proj_config)
#
#     rtn_data = emotionClassify.classify(_txt)
#
#     return rtn_data
