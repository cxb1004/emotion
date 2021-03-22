import os

from flask import request

from flask_module.emotion_blueprint import emotion_blueprint
from flask_module.emotion_blueprint.emotionclassify import EmotionClassify
from config import ProjectConfig
from flask_module.flask_log import FlaskLog as log
from flask_module.result_json import return_fail, return_success

baseConfig = ProjectConfig()
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
        log.info('初始化情感分析器完成...')
    except Exception as ex:
        log.error_ex("情感分析器创建失败：", ex)
        raise Exception('情感分析器创建失败！')


@emotion_blueprint.route('/classify', methods=['POST'])
def classify():
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
            log.error_ex('情感分析操作失败：', ex)
            rtn = return_fail(str(ex))
        finally:
            log.info('请求完成：{}'.format(rtn))
            return rtn


@emotion_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return return_success('情感判断模块运行正常，请访问公共接口。')
