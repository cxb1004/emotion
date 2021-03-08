"""

"""
import os
import sys

from snownlp.sentiment import Sentiment

# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)

from common.log import Log
from common.utils import isFileExist

log = Log()


class EmotionTagUtils:
    DICT_TAG = {'positive': 1, 'negative': -1, 'neutral': 0}
    FLAG_POS = 1
    FLAG_NEG = -1
    FLAG_NEU = 0

    POS_VALUE = 0.65
    NEG_VALUE = 0.45

    # 默认模型文件路径
    __DEFAULT_MODEL_PATH = os.path.join(basePath, 'deploy/sentiment.marshal')
    # 默认自定义（53kf）的语料库文件
    __DEFAULT_POS_53KF_PATH = os.path.join(basePath, 'deploy/pos_53kf.txt')
    __DEFAULT_NEG_53KF_PATH = os.path.join(basePath, 'deploy/neg_53kf.txt')

    __senti = None
    __pos_53kf_list = None
    __neg_53kf_list = None

    def __init__(self, modelPath, pos53kfPath, neg53kfPath):
        global __DEFAULT_MODEL_PATH, __DEFAULT_POS_53KF_PATH, __DEFAULT_NEG_53KF_PATH

        if modelPath is None:
            modelPath = __DEFAULT_MODEL_PATH
        if pos53kfPath is None:
            pos53kfPath = __DEFAULT_POS_53KF_PATH
        if neg53kfPath is None:
            neg53kfPath = __DEFAULT_NEG_53KF_PATH

        self.loadResources(modelPath, pos53kfPath, neg53kfPath)

        if self.__senti is None:
            exit(999)

    def loadResources(self, modelPath, pos_corpus, neg_corpus):
        """
        载入资源：
            模型文件
            自定义正负向语料文件
        """
        self.__senti = Sentiment()
        try:
            self.__senti.load(modelPath)
        except:
            log.error("无法找到对应的模型文件：{}".format(modelPath))
            log.warn("如果是python 3.x以上版本，模块底层会查询以.3结尾的文件，请请检查文件命名是否正确")
            self.__senti = None

        if isFileExist(pos_corpus)

    def classify(self, text):
        """

        """
        pass
