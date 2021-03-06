"""
【主要业务逻辑】
根据自定义的语料库corpus.txt和train/data下的正负词库，区分语料库里的正向、负向、中性句
然后和已发布的neg.txt/pos.txt进行整个，之后训练出sentiment.marshal

【输入文件】
neg.txt / pos.txt: 训练用的正负向语料库

【输出文件】
sentiment.marshal：训练产生的文件，python3是sentiment.marshal.3

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
from config import ProjectConfig

"""
全局变量
"""
log = Log()
baseConfig = ProjectConfig()

train_folder = baseConfig.get_value('py-project', 'train_folder')
model_file = baseConfig.get_value('py-project', 'model_filename_t')
pos_txt_file = baseConfig.get_value('py-project', 'corpus_pos_filename')
neg_txt_file = baseConfig.get_value('py-project', 'corpus_neg_filename')


# ============================读入文件==================================
# neg.txt/pos.txt是集成以后的语料库，sentiment.marshal是生成的模型文件
output_neg_file = os.path.join(train_folder, neg_txt_file)
output_pos_file = os.path.join(train_folder, pos_txt_file)
output_marshal_file = os.path.join(train_folder, model_file)

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
train_Model.save(output_marshal_file, iszip=True)
log.info('模型文件生成成功：{}'.format(output_marshal_file))

log.info('程序正常结束')
