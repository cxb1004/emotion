"""
更新了训练数据之后，对情感判断的语料库重新进行训练，生成sentiment.marshal文件

"""
# 导入系统模块、第三方模块
import os
import sys

from snownlp import sentiment

# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)

# 导入自开发模块
from common.log import Log
from common.utils import removeFileIfExists

# chua
log = Log()

# 训练用的正向文件、负向文件、结果文件
train_negative_file = os.path.join(basePath, 'data/train/neg.txt')
train_positive_file = os.path.join(basePath, 'data/train/pos.txt')
train_marshal_file = os.path.join(basePath, 'data/train/sentiment.marshal')

if not os.path.isfile(train_negative_file) or not os.path.isfile(train_positive_file):
    log.error('无法读取文件，请确认neg.txt/pos.txt 文件存在：')
    log.error(train_negative_file)
    log.error(train_positive_file)

# 重新生成marshal文件
removeFileIfExists(train_marshal_file)

log.debug('开始训练语料库...')
sentiment.train(train_negative_file, train_positive_file)
log.debug('训练完成！')

log.debug('开始保存语料库...')
sentiment.save(train_marshal_file, iszip=True)
log.debug('保存完成！')

log.debug('开始载入语料库{}'.format(train_marshal_file))
sentiment.load(train_marshal_file, iszip=True)
log.debug('载入完成！')

log.info(sentiment.classify('这真的是太好了！'))
