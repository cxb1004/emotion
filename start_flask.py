# 系统包类
import os

from flask import request
from flask_script import Manager

# 自定义的包类
# from flask_app import init_app, db, environment
from config import Config
from flask_module import init_app
from flask_module.emotionclassify import EmotionClassify
from flask_module.flask_log import FlaskLog as log
from flask_module.result_json import return_success, return_fail

# 初始化配置
baseConfig = Config()
# 读入项目配置文件
emotionClassify = None

# 使用配置文件，提取必要的参数，创建Flask App对象
app = init_app()

# 使用终端脚本工具启动和管理flask
manager = Manager(app)


@app.route("/", methods=['POST','GET'])
def index():
    app_config_info = 'Flask Web App is running...'
    return app_config_info


@app.route("/config", methods=['POST','GET'])
def config():
    app_config_info = 'Flask Web App configuration: '
    for key in app.config.keys():
        config_info = '\n  {} : {}'.format(key, app.config.get(key))
        app_config_info = app_config_info + config_info
    return app_config_info


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
        log.info('初始化情感分析器完成...')
    except Exception as ex:
        log.error(ex)
        raise Exception('情感分析器创建失败！')


@app.route("/emotion", methods=['POST'])
def emotion():
    txt = request.form.get("text")
    if txt is None or txt == '' or str(txt).strip() == '':
        log.error('参数缺失：{}'.format('text'))
        log.error('请求参数：{}'.format(request.data))
        return return_fail('参数缺失：{}'.format('text'))
    else:
        global emotionClassify
        if emotionClassify is None:
            init_emotion_classify(baseConfig)

        rtn = None

        log.info('请求接受：{}'.format(txt))
        try:
            data = emotionClassify.classify(txt)
            rtn = return_success(data)
        except Exception as ex:
            log.error(ex)
            rtn = return_fail(str(ex))
        finally:
            log.info('请求完成：{}'.format(rtn))
            return rtn


# 运行Flask Manager，启动web服务
if __name__ == '__main__':
    manager.run()
