"""
根据自定义的语料库corpus.txt和train/data下的正负词库，区分语料库里的正向、负向、中性句
然后和已发布的neg.txt/pos.txt进行整个，之后训练出sentiment.marshal


"""
# 导入系统模块、第三方模块
import os
import sys

from snownlp.sentiment import Sentiment


# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)

# 导入自开发模块
from common.log import Log
from common.utils import removeFileIfExists

"""
全局变量
"""
log = Log()


# ============================读入文件==================================
# 线上已经发布的模型
# neg.txt/pos.txt文件用于训练数据合并
# sentiment.marshal用于模型判断正负向功能
input_neg_deploy = os.path.join(basePath, 'deploy/neg.txt')
input_pos_deploy = os.path.join(basePath, 'deploy/pos.txt')
input_marshal_deploy = os.path.join(basePath, 'deploy/sentiment.marshal')

# 用于在没有_deploy资源的时候，和新增训练数据进行合并训练
# 默认数据是酒店评论数据，可能有偏差，但是总比没有基础数据、完全依靠运营设定要好
input_neg_default = os.path.join(basePath, 'train/data/neg_default.txt')
input_pos_default = os.path.join(basePath, 'train/data/pos_default.txt')

# 正负向词库
input_neg_words = os.path.join(basePath, 'train/data/neg_words.txt')
input_pos_words = os.path.join(basePath, 'train/data/pos_words.txt')

# 快服自定义正负向语料库
input_neg_53kf = os.path.join(basePath, 'train/data/neg_53kf.txt')
input_pos_53kf = os.path.join(basePath, 'train/data/pos_53kf.txt')

# 待训练的语料库（支持增量）
input_corpus = os.path.join(basePath, 'train/corpus.txt')

# ============================输出文件==================================
# 临时文件，用于查看新增数据的正负向准确性
output_neg_tmp = os.path.join(basePath, 'train/neg_add.tmp')
output_pos_tmp = os.path.join(basePath, 'train/pos_add.tmp')
output_neu_tmp = os.path.join(basePath, 'train/neu_add.tmp')

# neg.txt/pos.txt是集成以后的语料库，sentiment.marshal是生成的模型文件
output_neg_file = os.path.join(basePath, 'train/neg.txt')
output_pos_file = os.path.join(basePath, 'train/pos.txt')
output_marshal_file = os.path.join(basePath, 'train/sentiment.marshal')

log.info('开始训练模型...')
removeFileIfExists(output_marshal_file)
log.info('负向语料库：{} '.format(output_neg_file))
log.info('正向语料库：{} '.format(output_pos_file))
# 可以使用Sentiment()对象进行训练，但是要注意neg_docs/pos_docs是数据，而不是数据文件
train_Model = Sentiment()
neg_docs = []
pos_docs = []
with open(output_neg_file,'r', encoding='utf-8') as readFile:
    neg_docs = readFile.read().splitlines()
with open(output_pos_file,'r', encoding='utf-8') as readFile:
    pos_docs = readFile.read().splitlines()
train_Model.train(neg_docs=neg_docs, pos_docs=pos_docs)
log.info('模型训练完成')

log.info('开始生成模型文件...')
train_Model.save(output_marshal_file)
log.info('模型文件生成成功：{}'.format(output_marshal_file))

log.info('程序正常结束')
