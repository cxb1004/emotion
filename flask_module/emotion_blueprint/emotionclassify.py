import os
import sys

from snownlp.sentiment import Sentiment

# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)

from common.utils import isFileExist
from common.textSimilarity import CosSim
from config import ProjectConfig
from flask_module.flask_log import FlaskLog

log = FlaskLog()

class EmotionClassify:
    DICT_TAG = {'positive': 1, 'negative': -1, 'neutral': 0}
    DICT_TAG_S = {v: k for k, v in DICT_TAG.items()}
    FLAG_POS = 1
    FLAG_NEG = -1
    FLAG_NEU = 0

    _config = ProjectConfig()

    # 默认模型文件路径
    __DEPLOY_PATH = _config.get_value('py-project', 'deploy_folder')
    __FILENAME_MODEL = _config.get_value('py-project', 'model_filename_t')
    __FILENAME_POS_53KF_CORPUS = _config.get_value('py-project', 'corpus_pos_53kf_filename')
    __FILENAME_NEG_53KF_CORPUS = _config.get_value('py-project', 'corpus_neg_53kf_filename')

    __DEFAULT_MODEL_PATH = os.path.join(__DEPLOY_PATH, __FILENAME_MODEL)
    # 默认自定义（53kf）的语料库文件
    __DEFAULT_POS_53KF_PATH = os.path.join(__DEPLOY_PATH, __FILENAME_POS_53KF_CORPUS)
    __DEFAULT_NEG_53KF_PATH = os.path.join(__DEPLOY_PATH, __FILENAME_NEG_53KF_CORPUS)

    __senti = None
    __sim = None
    __pos_53kf_list = None
    __neg_53kf_list = None

    # 相似度阀值
    __VALUE_SIM = float(_config.get_value('py-project', 'run_sim_idx'))
    # 模型正向阀值
    __VALUE_POS = float(_config.get_value('py-project', 'run_pos_idx'))
    # 模型负向阀值
    __VALUE_NEG = float(_config.get_value('py-project', 'run_neg_idx'))

    RTN_EMOTION = 'emotion'
    RTN_EMOTION_TAG = 'emotion_tag'
    RTN_EMOTION_VALUE = 'emotion_value'
    RTN_CLASSIFY = 'classify'

    def __init__(self, modelPath=None, pos53kfPath=None, neg53kfPath=None):
        log.debug('开始实例化EmotionClassify')

        if modelPath is None:
            modelPath = self.__DEFAULT_MODEL_PATH
        if pos53kfPath is None:
            pos53kfPath = self.__DEFAULT_POS_53KF_PATH
        if neg53kfPath is None:
            neg53kfPath = self.__DEFAULT_NEG_53KF_PATH

        self.loadResources(modelPath=modelPath, posCorpusPath=pos53kfPath, negCorpusPath=neg53kfPath)

        if self.__senti is None:
            raise Exception("EmotionClassify实例化失败：内置模型对象加载失败！")

        self.__sim = CosSim()

        # 初始化参数
        self.setConfigValue(simValue=self.__VALUE_SIM, posValue=self.__VALUE_POS, negValue=self.__VALUE_NEG)

        log.debug('EmotionClassify实例化成功')

    def loadResources(self, modelPath=None, posCorpusPath=None, negCorpusPath=None):
        """
        载入资源：
            模型文件
            自定义正负向语料文件
        """
        # 导入模型数据
        if modelPath is not None:
            self.__senti = Sentiment()
            try:
                self.__senti.load(modelPath)
            except Exception as ex:
                log.error("无法找到对应的模型文件：{}".format(modelPath))
                log.warning("如果是python 3.x以上版本，模块底层会查询以.3结尾的文件，请请检查文件命名是否正确")
                log.error(ex)
                self.__senti = None

        # 读取正向自定义语料库
        if posCorpusPath is not None:
            if isFileExist(posCorpusPath):
                with open(posCorpusPath, 'r', encoding='utf-8') as readFile:
                    self.__pos_53kf_list = readFile.read().splitlines()
            else:
                self.__pos_53kf_list = None

        # 读取负向自定义语料库
        if negCorpusPath is not None:
            if isFileExist(negCorpusPath):
                with open(negCorpusPath, 'r', encoding='utf-8') as readFile:
                    self.__neg_53kf_list = readFile.read().splitlines()
            else:
                self.__neg_53kf_list = None

    def setConfigValue(self, simValue=None, posValue=None, negValue=None):
        # 相似度阀值
        if simValue is not None:
            self.__VALUE_SIM = float(simValue)
        # 模型正向阀值
        if posValue is not None:
            self.__VALUE_POS = float(posValue)
        # 模型负向阀值
        if negValue is not None:
            self.__VALUE_NEG = float(negValue)

    def classify(self, text):
        """
        分类接口：先用自定义语料库进行文本匹配，输出分类/分值
        返回一个字典：
        emotion: 1/-1/0
        emotion_tag = positive/negative/neutral
        emotion_value=相似值/模型判断值
        classify: CosSim/Model
        """
        # log.debug('预测文本：{}'.format(text))
        # emotion: 1/-1/0  emotion_tag = positive/negative/neutral  emotion_value=相似值/模型判断值  classify: CosSim/Model
        rtn_value = {'emotion': None, 'emotion_tag': None, 'emotion_value': None, 'classify': None}
        # 先根据自定义正负向语料库进行文本匹配计算
        pos_max_value = 0
        neg_max_value = 0
        for line in self.__pos_53kf_list:
            v = self.__sim.getSimilarityIndex(text, line)
            if v > pos_max_value and v >= self.__VALUE_POS:
                pos_max_value = v
        for line in self.__neg_53kf_list:
            v = self.__sim.getSimilarityIndex(text, line)
            if v > neg_max_value and v >= self.__VALUE_NEG:
                neg_max_value = v

        # 如果自定义正负向语料库有结果，就直接返回
        if pos_max_value > neg_max_value:
            rtn_value['emotion'] = self.FLAG_POS
            rtn_value['emotion_tag'] = self.DICT_TAG_S.get(self.FLAG_POS)
            rtn_value['emotion_value'] = pos_max_value
            rtn_value['classify'] = 'CosSim'
        elif neg_max_value > pos_max_value:
            rtn_value['emotion'] = self.FLAG_NEG
            rtn_value['emotion_tag'] = self.DICT_TAG_S.get(self.FLAG_NEG)
            rtn_value['emotion_value'] = neg_max_value
            rtn_value['classify'] = 'CosSim'
        else:
            # 如果自定义正负向语料库没有结果，使用模型进行判断
            v = self.__senti.classify(text)
            if v >= self.__VALUE_POS:
                rtn_value['emotion'] = self.FLAG_POS
                rtn_value['emotion_tag'] = self.DICT_TAG_S.get(self.FLAG_POS)
                rtn_value['emotion_value'] = v
                rtn_value['classify'] = 'Model'
                return rtn_value
            elif v <= self.__VALUE_NEG:
                rtn_value['emotion'] = self.FLAG_NEG
                rtn_value['emotion_tag'] = self.DICT_TAG_S.get(self.FLAG_NEG)
                rtn_value['emotion_value'] = v
                rtn_value['classify'] = 'Model'
            else:
                rtn_value['emotion'] = self.FLAG_NEU
                rtn_value['emotion_tag'] = self.DICT_TAG_S.get(self.FLAG_NEU)
                rtn_value['emotion_value'] = v
                rtn_value['classify'] = 'Model'
        # log.debug('预测结果{}'.format(rtn_value))
        return rtn_value
