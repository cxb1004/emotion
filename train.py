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

log.info('开始训练数据...')
sentiment.train(neg_file=train_negative_file, pos_file=train_positive_file)
log.info('数据训练完毕')

log.info('保持训练结果文件...')
sentiment.save(train_marshal_file, iszip=False)
log.info('训练文件保存完毕')

log.info('导入训练结果文件...')
sentiment.load(train_marshal_file)
log.info('导入训练结果文件完成:{}'.format(sentiment.data_path))


text = '这真的是太舒服了，我太喜欢了'
score = sentiment.classify(text)
print('预测文本：{}\n预测结果：{}'.format(text,score))
