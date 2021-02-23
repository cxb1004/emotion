"""
根据自定义的语料库corpus.txt和train/data下的正负词库，区分语料库里的正向、负向、中性句
然后和已发布的neg.txt/pos.txt进行整个，之后训练出sentiment.marshal
1、读取语料库corpus.txt，出错就停止
2、读取已发布的neg.txt/pos.txt，如果出错，就读取原始基础正负向语料库neg_original.txt/pos_original.txt,出错就停止
3、读取正负向的词库neg_words.txt/pos_words.txt，出错就停止
4、读取自定义的正负向语料库neg_53kf.txt/pos_53kf.txt，文件必须存在，数据可以为空，文件不存在就出错

5、循环读入corpus.txt的每一行：
5.1 查询语句是否存在于已发布的语料库里面，如果存在，跳过之后的步骤，直接进入下一行
5.2 查询


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

# 读入文件
input_neg_deploy = os.path.join(basePath, 'deploy/neg.txt')
input_pos_deploy = os.path.join(basePath, 'deploy/pos.txt')
input_neg_original = os.path.join(basePath, 'train/data/neg_original.txt')
input_pos_original = os.path.join(basePath, 'train/data/pos_original.txt')
input_neg_words = os.path.join(basePath, 'train/data/neg_words.txt')
input_pos_words = os.path.join(basePath, 'train/data/pos_words.txt')
input_neg_53kf = os.path.join(basePath, 'train/data/neg_53kf.txt')
input_pos_53kf = os.path.join(basePath, 'train/data/pos_53kf.txt')
input_corpus = os.path.join(basePath,'train/data/corpus.txt')

# 输出文件：neg.txt/pos.txt是集成以后的语料库，sentiment.marshal是生成的模型文件
output_neg_file = os.path.join(basePath, 'train/data/neg.txt')
output_pos_file = os.path.join(basePath, 'train/data/pos.txt')
output_neu_file = os.path.join(basePath, 'train/data/neu.txt')
output_marshal_file = os.path.join(basePath, 'train/data/sentiment.marshal')

# 相似度指数设定
SIM_IDX = 0.8


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
