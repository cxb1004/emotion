"""
根据自定义的语料库corpus.txt和train/data下的正负词库，区分语料库里的正向、负向、中性句
然后和已发布的neg.txt/pos.txt进行整个，之后训练出sentiment.marshal
1、读取语料库corpus.txt，出错就停止
2、读取已发布的neg.txt/pos.txt，如果出错，就读取原始基础正负向语料库neg_original.txt/pos_original.txt,出错就停止
3、读取正负向的词库neg_words.txt/pos_words.txt，出错就停止
4、读取自定义的正负向语料库neg_53kf.txt/pos_53kf.txt，文件必须存在，数据可以为空，文件不存在就出错

5、循环读入corpus.txt的每一行line_data：
5.1 查询语句是否存在于已发布的语料库里面，如果存在，跳过之后的步骤，直接进入下一行
5.2 根据判别策略，确定line_data的正负向，分别写入临时文件
5.3 和线上语料库集成，最终形成neg.txt pos.txt 并训练模型文件

判断策略有3个：
a. 根据已有的模型进行正负向判断
b. 对自定义语料库进行文本相似度进行判断，相似度在SIM_IDX以上，则属于该类
c. 根据正负向词汇表进行判断，匹配的词汇数量>1且数量大优先，不满足条件为0
优先级 a>b>c
判别返回参数： 1 正向  -1 负向  0 中性

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
from common.utils import isFileExist

"""
全局变量
"""
log = Log()

# 读入文件
input_neg_deploy = os.path.join(basePath, 'deploy/neg.txt')
input_pos_deploy = os.path.join(basePath, 'deploy/pos.txt')
input_marshal_deploy = os.path.join(basePath, 'deploy/sentiment.marshal')

input_neg_original = os.path.join(basePath, 'train/data/neg_original.txt')
input_pos_original = os.path.join(basePath, 'train/data/pos_original.txt')

input_neg_words = os.path.join(basePath, 'train/data/neg_words.txt')
input_pos_words = os.path.join(basePath, 'train/data/pos_words.txt')
input_neg_53kf = os.path.join(basePath, 'train/data/neg_53kf.txt')
input_pos_53kf = os.path.join(basePath, 'train/data/pos_53kf.txt')

input_corpus = os.path.join(basePath, 'train/data/corpus.txt')

# 输出文件：neg.txt/pos.txt是集成以后的语料库，sentiment.marshal是生成的模型文件
output_neg_add = os.path.join(basePath, 'train/data/neg_add.tmp')
output_pos_add = os.path.join(basePath, 'train/data/pos_add.tmp')
output_neu_add = os.path.join(basePath, 'train/data/neu_add.tmp')
output_neg_file = os.path.join(basePath, 'train/data/neg.txt')
output_pos_file = os.path.join(basePath, 'train/data/pos.txt')
output_neu_file = os.path.join(basePath, 'train/data/neu.txt')
output_marshal_file = os.path.join(basePath, 'train/data/sentiment.marshal')

# 文本相似度阀值设定
SIM_IDX = 0.8

# 模型判断正负向阀值设定
SIM_IDX = 0.8

FLAG_NEG = -1
FLAG_POS = 1
FLAG_NUE = 0

sentimentModel = None

neg_merge = None
pos_merge = None
dict_neg_words = None
dict_pos_words = None
dict_neg_53kf = None
dict_pos_53kf = None

"""
函数
"""


def judge_by_deploy_model(self):
    return FLAG_NUE


def judge_by_53kf_corpus(self):
    return FLAG_NUE


def judge_by_common_corpus(self):
    return FLAG_NUE


"""
主程序
"""
# 检查待分类语料库是否存在
if not isFileExist(input_corpus):
    log.error('无法读取待训练的语料库文件，请确认文件存在：{}'.format(input_corpus))
    log.error('程序异常终止！')
    exit(999)

# 检查要合并的语料库文件
if not isFileExist(input_neg_deploy) or not isFileExist(input_pos_deploy):
    # 如果读取不到已发布的语料文件，暂时先抛出警告
    log.warn('无法读取已发布模型或语料库，将无法和之前的语料合并:\n{}\n{}'.format(input_neg_deploy, input_pos_deploy))

    if not isFileExist(input_neg_original) or not isFileExist(input_pos_original):
        # 如果没有基础语料库（SnowNPL自带的，或是线上已发布的），意味着有问题了，抛错
        log.error('无法读取SnowNPL默认的语料库: \n{}\n{}'.format(input_neg_original, input_pos_original))
        log.error('程序异常终止！')
        exit(999)
    else:
        # 如果没有已发布的语料库，就是用SnowNPL模块默认自带的语料（酒店评论，可能会不精准）
        neg_merge = input_neg_original
        pos_merge = input_pos_original
        log.info('使用SnowNLP默认的预料数据：\n{}\n{}'.format(neg_merge, pos_merge))
else:
    neg_merge = input_neg_deploy
    pos_merge = input_pos_deploy
    log.info('使用已发布的预料数据：\n{}\n{}'.format(neg_merge, pos_merge))

# 检查模型文件
if not isFileExist(input_marshal_deploy):
    log.warn('无法读取已发布的情感判断模型，部分判断策略将失效：{}')
    sentimentModel = None
else:
    log.info('开始载入已有情感判断模型')
    sentimentModel = sentiment.load(input_marshal_deploy)
    log.info('完成载入已有情感判断模型')

# 检查自定义的语料库和正负向词库
if not isFileExist(input_neg_words) \
        or not isFileExist(input_pos_words) \
        or not isFileExist(input_neg_53kf) \
        or not isFileExist(input_pos_53kf):
    log.error('无法读取以下文件之一，请确认文件存在：\n{}\n{}\n{}\n{}'.format(input_neg_words,
                                                           input_pos_words, input_neg_53kf, input_pos_53kf))

# 把正负向词库转化为字典
dict_neg_words = fileToDict(input_neg_words)
dict_pos_words = fileToDict(input_pos_words)
dict_neg_53kf = fileToDict(input_neg_53kf)
dict_pos_53kf = fileToDict(input_pos_53kf)


#
#
# if not os.path.isfile(train_negative_file) or not os.path.isfile(train_positive_file):
#     log.error('无法读取文件，请确认neg.txt/pos.txt 文件存在：')
#     log.error(train_negative_file)
#     log.error(train_positive_file)
#
# # 重新生成marshal文件
# removeFileIfExists(train_marshal_file)
#
# log.info('开始训练数据...')
# sentiment.train(neg_file=train_negative_file, pos_file=train_positive_file)
# log.info('数据训练完毕')
#
# log.info('保持训练结果文件...')
# sentiment.save(train_marshal_file, iszip=False)
# log.info('训练文件保存完毕')
#
# log.info('导入训练结果文件...')
# sentiment.load(train_marshal_file)
# log.info('导入训练结果文件完成:{}'.format(sentiment.data_path))
#
# text = '这真的是太舒服了，我太喜欢了'
# score = sentiment.classify(text)
# print('预测文本：{}\n预测结果：{}'.format(text, score))
