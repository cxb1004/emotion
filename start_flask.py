# 系统包类
import os
import logging
from flask_script import Manager

# 自定义的包类
# from flask_app import init_app, db, environment
from config import Config
from flask_module import init_app
from flask_module.result_json import jsonResultVo
from flask_module.emotionclassify import EmotionClassify

# 读入项目配置文件
baseConfig = Config()

emotionClassify = None

# 使用配置文件，提取必要的参数，创建Flask App对象
app = init_app(baseConfig)

# 使用终端脚本工具启动和管理flask
manager = Manager(app)


@app.route("/")
def index():
    return "flask server is running..."


emotionClassify = None


def init_emotion_classify(_p_config):
    global emotionClassify
    try:
        deploy_folder = _p_config.get_value('py-project', 'deploy_folder')
        file_model = _p_config.get_value('py-project', 'model_filename_t')
        file_53kf_pos = _p_config.get_value('py-project', 'corpus_pos_53kf_filename')
        file_53kf_neg = _p_config.get_value('py-project', 'corpus_neg_53kf_filename')
        sim_idx = _p_config.get_value('py-project', 'run_sim_idx')
        pos_idx = _p_config.get_value('py-project', 'run_pos_idx')
        neg_idx = _p_config.get_value('py-project', 'run_neg_idx')
        path_model = os.path.join(deploy_folder, file_model)
        path_53kf_pos = os.path.join(deploy_folder, file_53kf_pos)
        path_53kf_neg = os.path.join(deploy_folder, file_53kf_neg)
        # 创建情感分类器对象
        emotionClassify = EmotionClassify(path_model, path_53kf_pos, path_53kf_neg)
        # 设置情感分类器参数
        emotionClassify.setConfigValue(sim_idx, pos_idx, neg_idx)
        logging.info('初始化情感分析器完成...')
        print('初始化情感分析器完成...')
    except Exception as ex:
        raise Exception()


@app.route("/emotion")
def emotion():
    global emotionClassify
    if emotionClassify is None:
        init_emotion_classify(baseConfig)

    txt = '快服公司的机器人真是好用'
    rtn = None
    try:
        data = emotionClassify.classify(txt)
    except Exception as ex:
        return jsonResultVo(9, str(ex), '')
    return jsonResultVo(0, '', data)


if __name__ == '__main__':
    manager.run()
