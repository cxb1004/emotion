"""
根据自定义的语料库corpus.txt和train/data下的正负词库，区分语料库里的正向、负向、中性句
然后和已发布的neg.txt/pos.txt进行整合，最终获得训练模型使用的文件

主业务逻辑：
1、获取待合并的正负向语料库（要么是线上deploy的，要么是默认的_default）
2、如果train/data目录下的数据文件不存在，停止应用
3、按行对待训练的预料进行正负向判断
3.1 使用模型进行正负向判断，如果结果是正向或是负向，就直接判断；如果是中性继续下面的判断
3.2 使用自定义词库进行正负向判断。使用文本相似度算法，用正负向自定义语料库进行相似度比较
分别获得正负向语料库的最大相似度（相似度必须大于设定的阀值）
3.3 使用正负向词库进行正负向判断，
使用jieba进行分词，匹配正负向词库的数量，数量多切超过阀值的正向/负向胜出
3.4 判别结果分别写入tmm文件，该文件用于人工审阅自动正负向判别的结果
判断结果为正向，写入pos_add.tmp
判断结果为负向，写入neg_add.tmp
判断结果为中性，写入neu_add.tmp
4、结合步骤1中确定的待合并的语料库，把正负向语料分别进行合并，获得文件:
neg.txt = neg_add.tmp + neg_merge(线上neg.txt 或 默认 neg_default.txt)
pos.txt = pos_add.tmp + pos_merge(线上pos.txt 或 默认 pos_default.txt)
这两个文件将会用于模型训练

输入文件：
deploy目录下：
    neg.txt / pos.txt / sentiment.marshal ：使用既有的模型，对原始语料进行正负向判断
    corpus.txt：
train/data目录下：
    neg_default.txt / pos_default.txt：在没有deploy的数据下，使用默认数据进行训练
    neg_53kf.txt / pos_53kf.txt：
    neg_words.txt / pos_words.txt：

输出文件：
train目录下：
    neg_add.tmp / pos_add.tmp / neu_add.tmp
    neg.txt / pos.txt
    sentiment.marshal

"""
# 导入系统模块、第三方模块
import os
import sys

import jieba
from snownlp.sentiment import Sentiment

# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)

# 导入自开发模块
from common.log import Log
from common.utils import isFileExist, removeFileIfExists
from common.textSimilarity import CosSim
from config import Config

"""
全局变量
"""
log = Log()
baseConfig = Config()
train_folder = baseConfig.get_value('py-project', 'train_folder')
train_data_folder = baseConfig.get_value('py-project', 'train_data_folder')
deploy_folder = baseConfig.get_value('py-project', 'deploy_folder')

filename_corpus_txt = baseConfig.get_value('py-project', 'train_corpus_txt')
filename_model = baseConfig.get_value('py-project', 'model_filename_t')
filename_neg_txt = baseConfig.get_value('py-project', 'corpus_neg_filename')
filename_pos_txt = baseConfig.get_value('py-project', 'corpus_pos_filename')
filename_pos_default_txt = baseConfig.get_value('py-project', 'corpus_pos_default_filename')
filename_neg_default_txt = baseConfig.get_value('py-project', 'corpus_neg_default_filename')
filename_pos_words_txt = baseConfig.get_value('py-project', 'words_pos_filename')
filename_neg_words_txt = baseConfig.get_value('py-project', 'words_neg_filename')
filename_pos_53kf_txt = baseConfig.get_value('py-project', 'corpus_pos_53kf_filename')
filename_neg_53kf_txt = baseConfig.get_value('py-project', 'corpus_neg_53kf_filename')

# ============================读入文件==================================
# 线上已经发布的模型
# neg.txt/pos.txt文件用于训练数据合并
# sentiment.marshal用于模型判断正负向功能
input_neg_deploy = os.path.join(deploy_folder, filename_neg_txt)
input_pos_deploy = os.path.join(deploy_folder, filename_pos_txt)
input_marshal_deploy = os.path.join(deploy_folder, filename_model)

# 用于在没有_deploy资源的时候，和新增训练数据进行合并训练
# 默认数据是酒店评论数据，可能有偏差，但是总比没有基础数据、完全依靠运营设定要好
input_neg_default = os.path.join(train_data_folder, filename_neg_default_txt)
input_pos_default = os.path.join(train_data_folder, filename_pos_default_txt)

# 正负向词库
input_neg_words = os.path.join(train_data_folder, filename_neg_words_txt)
input_pos_words = os.path.join(train_data_folder, filename_pos_words_txt)

# 快服自定义正负向语料库
input_neg_53kf = os.path.join(train_data_folder, filename_neg_53kf_txt)
input_pos_53kf = os.path.join(train_data_folder, filename_pos_53kf_txt)

# 待训练的语料库（支持增量）
input_corpus = os.path.join(train_folder, filename_corpus_txt)

# ============================输出文件==================================
# 临时文件，用于查看新增数据的正负向准确性
output_neg_tmp = os.path.join(train_folder, 'neg_add.tmp')
output_pos_tmp = os.path.join(train_folder, 'pos_add.tmp')
output_neu_tmp = os.path.join(train_folder, 'neu_add.tmp')

# neg.txt/pos.txt是集成以后的语料库，sentiment.marshal是生成的模型文件
output_neg_file = os.path.join(train_folder, filename_neg_txt)
output_pos_file = os.path.join(train_folder, filename_pos_txt)

# 文本相似度阀值设定
SIM_IDX = float(baseConfig.get_value('py-project', 'train_sim_idx'))

# 模型判断正负向阀值设定
POS_IDX = float(baseConfig.get_value('py-project', 'train_pos_idx'))
NEG_IDX = float(baseConfig.get_value('py-project', 'train_neg_idx'))

# 正负向词语命中数量
WORDS_MATCH_LIMIT = int(baseConfig.get_value('py-project', 'train_words_match_limit'))

FLAG_NEG = -1
FLAG_POS = 1
FLAG_NUE = 0

# 用于数据整合的正负向语料库，要么是默认的，要么是线上已发布的
neg_merge = None
pos_merge = None

# 正负向词库转化为dict
# 注意：后续要做是要查询待判语句有多少个词语在词库中，所以转化成字典最为方便
# 如果忽略重复词，可以直接使用 aSet & bSet 获取数据
# 如果需要计算重复词，那么循环判断句的分词，使用字典查询存在是最快的
dict_neg_words = None
dict_pos_words = None
# 自定义语料需要循环进行文本比较，因此使用list
list_neg_53kf = None
list_pos_53kf = None

test_Model = None
train_Model = None

simUtils = None

"""
函数
"""


def sentiment_judge(sentence):
    log.debug('开始判断正负向:{}'.format(sentence))
    """
    判断sentence的正负向属性
    1、用模型来判断，如果正负向值大于阀值，就直接得出结果
    2、用自定义的正负向语料库语句进行相似度比较，相近度大于阀值，
    3、和正负向词库进行匹配，获得正向词数量和负向词数量，值大者胜出（必须大于2）
    """
    if test_Model is not None:
        rtn = judge_by_model(sentence, POS_IDX, NEG_IDX)
        # 如果模型已经判断出正负向，直接返回（中性的话进行下一步判断）
        log.debug('     模型判断结果:{}'.format(rtn))
        if rtn == FLAG_POS or rtn == FLAG_NEG:
            return rtn

    rtn = judge_by_53kf_corpus(sentence)
    log.debug('     自定义语料库判断结果：{}'.format(rtn))
    if rtn == FLAG_POS or rtn == FLAG_NEG:
        return rtn

    rtn = judge_by_sentiment_words(sentence)
    log.debug('     正负向词库判断结果：{}'.format(rtn))
    if rtn == FLAG_POS or rtn == FLAG_NEG:
        return rtn
    else:
        return FLAG_NUE


def judge_by_model(_sentence, pos_value, neg_value):
    """
    使用模型进行正负向计算
    结果值大于等于正向阀值，判断为正向
    结果值小于等于负向阀值，判断为负向
    其他结果值，判断为中性
    """
    idx = test_Model.classifier(_sentence)
    log.debug('模型判断值:{}'.format(idx))
    if idx >= pos_value:
        return FLAG_POS
    elif idx <= neg_value:
        return FLAG_NEG
    else:
        return FLAG_NUE


def judge_by_53kf_corpus(_sentence):
    """
    对自定义语料库进行文本相似度判断，相似度最高，且高于SIM_IDX，得到此时的正负向max值
    然后比较正负向max值，最终判定正负向属性
    """
    if list_neg_53kf is None or list_neg_53kf is None:
        log.error('53kf的自定义语料数据为空，请检查文件是否读取成功：\n{}\n{}'.format(input_neg_53kf, input_pos_53kf))
        log.error('程序异常结束！')
        exit(999)

    # 计算出负向最大值
    neg_max = 0
    for neg_sentence in list_neg_53kf:
        sim = simUtils.getSimilarityIndex(_sentence, neg_sentence)
        if sim >= SIM_IDX and sim > neg_max:
            neg_max = sim

    # 计算出正向最大值
    pos_max = 0
    for pos_sentence in list_pos_53kf:
        sim = simUtils.getSimilarityIndex(_sentence, pos_sentence)
        if sim >= SIM_IDX and sim > pos_max:
            pos_max = sim

    # 这里是关键的判断策略：以值大的来决定正负向，如果相等就
    # 【建议】
    if pos_max > 0 and neg_max == 0:
        # 正向特征明显
        return FLAG_POS
    elif neg_max > 0 and pos_max == 0:
        # 负向特征明显
        return FLAG_NEG
    elif neg_max > 0 and pos_max > 0:
        # 正负向特征模糊
        return FLAG_NUE
    elif neg_max == 0 and pos_max == 0:
        # 正负向特征不明显
        return FLAG_NUE


def judge_by_sentiment_words(_sentence):
    """
    把待判断句子分词，然后看下多少词在正负向词库中，以数量决定正负向属性
    """
    if dict_neg_words is None or dict_pos_words is None:
        log.error('正负向词典数据为空，请检查文件是否读取成功：\n{}\n{}'.format(input_neg_words, input_pos_words))
        log.error('程序异常结束！')
        exit(999)
    set_data = set(jieba.lcut(_sentence))
    # 命中次数
    count_pos = len(set_data & dict_pos_words.keys())
    count_neg = len(set_data & dict_neg_words.keys())

    if count_pos > count_neg and count_pos > WORDS_MATCH_LIMIT:
        return FLAG_POS
    elif count_neg > count_pos and count_neg > WORDS_MATCH_LIMIT:
        return FLAG_NEG
    else:
        return FLAG_NUE


def fileToList(filePath):
    """
    读取文件，把文件行数据变成list
    """
    with open(filePath, 'r', encoding='utf-8') as readFile:
        return readFile.read().splitlines()


def fileToDict(filePath):
    """
    读取文件，把文件行数据变成字典
    """
    with open(filePath, 'r', encoding='utf-8') as readFile:
        linelist = readFile.read().splitlines()
        return dict(zip(linelist, list(range(len(linelist)))))


"""
主程序
"""
# # 待训练的语料数据文件是否存在
if not isFileExist(input_corpus):
    log.error('无法读取待训练的语料库文件，请确认文件存在：{}'.format(input_corpus))
    log.error('程序异常终止！')
    exit(999)

# 检查要合并的语料库文件
if not isFileExist(input_neg_deploy) or not isFileExist(input_pos_deploy):
    # 如果读取不到已发布的语料文件，暂时先抛出警告
    log.warn('无法读取已发布模型的语料库，将无法和之前的语料合并:\n{}\n{}'.format(input_neg_deploy, input_pos_deploy))

    if not isFileExist(input_neg_default) or not isFileExist(input_pos_default):
        # 如果没有基础语料库（SnowNPL自带的，或是线上已发布的），意味着有问题了，抛错
        log.error('无法读取SnowNPL默认的语料库: \n{}\n{}'.format(input_neg_default, input_pos_default))
        log.error('程序异常终止！')
        exit(999)
    else:
        # 如果没有已发布的语料库，就是用SnowNPL模块默认自带的语料（已经经过人工审阅，但由于行业不同，可能导致判断不精确）
        neg_merge = input_neg_default
        pos_merge = input_pos_default
        log.info('使用SnowNLP默认的预料数据：\n{}\n{}'.format(neg_merge, pos_merge))
else:
    neg_merge = input_neg_deploy
    pos_merge = input_pos_deploy
    log.info('使用已发布的预料数据：\n{}\n{}'.format(neg_merge, pos_merge))

# 检查模型文件
if not isFileExist(input_marshal_deploy):
    log.warn('无法读取已发布的情感判断模型，部分判断策略将失效')
    test_Model = None
else:
    log.info('开始载入已有情感判断模型')
    test_Model = Sentiment()
    test_Model.load(input_marshal_deploy)
    log.info('完成载入已有情感判断模型')

# 检查自定义的语料库和正负向词库
if not isFileExist(input_neg_words) \
        or not isFileExist(input_pos_words) \
        or not isFileExist(input_neg_53kf) \
        or not isFileExist(input_pos_53kf):
    log.error('无法读取以下文件之一，请确认文件存在：\n{}\n{}\n{}\n{}'.format( \
        input_neg_words, input_pos_words, input_neg_53kf, input_pos_53kf))
    exit(999)
else:
    # 读取文件，把自定义语料库，转化为列表
    list_pos_53kf = fileToList(input_pos_53kf)
    list_neg_53kf = fileToList(input_neg_53kf)
    # 初始化文本相似度计算工具
    simUtils = CosSim()
    # 读取文件，把正负向词库，转化为字典
    dict_pos_words = fileToDict(input_pos_words)
    dict_neg_words = fileToDict(input_neg_words)

# 先删除存在的临时文件
removeFileIfExists(output_neg_tmp)
removeFileIfExists(output_pos_tmp)
removeFileIfExists(output_neu_tmp)

cnt_all = 0
cnt_neg = 0
cnt_pos = 0
cnt_neu = 0
log.info('开始分析数据...')

with open(input_corpus, 'r', encoding='utf-8') as input_corpus_file, \
        open(output_neg_tmp, 'w', encoding='utf-8') as output_neg_tmp_file, \
        open(output_pos_tmp, 'w', encoding='utf-8') as output_pos_tmp_file, \
        open(output_neu_tmp, 'w', encoding='utf-8') as output_neu_tmp_file:
    all_sentences = input_corpus_file.read().splitlines()
    cnt_all = len(all_sentences)
    for sentence in all_sentences:
        # 对当前句进行正负向判别
        sentiment_idx = sentiment_judge(sentence)
        if sentiment_idx == FLAG_NEG:
            # 如果判断是
            output_neg_tmp_file.write(sentence + '\n')
            cnt_neg = cnt_neg + 1
        elif sentiment_idx == FLAG_POS:
            output_pos_tmp_file.write(sentence + '\n')
            cnt_pos = cnt_pos + 1
        else:
            output_neu_tmp_file.write(sentence + '\n')
            cnt_neu = cnt_neu + 1
log.info('数据分析完成：一共{}条数据，其中正向数据{}条，负向数据{}条，中性数据{}条'.format(cnt_all, cnt_pos, cnt_neg, cnt_neu))

# 备注：如果用户希望先预览一下判断结果，以下代码可以分出去单独执行，让用户查看tmp文件
log.info('开始合并数据...')
removeFileIfExists(output_pos_file)
removeFileIfExists(output_neg_file)

log.info('开始合并正向语料库数据：{} + {} -> {}'.format(output_pos_tmp, pos_merge, output_pos_file))
pos_docs = []
with open(pos_merge, 'r', encoding='utf-8') as baseFile, \
        open(output_pos_tmp, 'r', encoding='utf-8') as mergeFile, \
        open(output_pos_file, 'w', encoding='utf-8') as resultFile:
    baseList = baseFile.read().splitlines()
    log.debug('baseList数量{}'.format(len(baseList)))
    mergeList = mergeFile.read().splitlines()
    log.debug('mergeList数量{}'.format(len(mergeList)))
    pos_docs = baseList + mergeList
    log.debug('合并以后的数量{}'.format(len(pos_docs)))
    pos_docs = list(set(pos_docs))
    log.debug('去重以后的数量{}'.format(len(pos_docs)))
    # 增加自定义语料库的权重，即把自定义的语料库翻倍加入待训练数据
    pos_docs = pos_docs + list(set(list_pos_53kf)) * 100
    log.debug('增加自定义语料权重之后数量{}'.format(len(pos_docs)))
    pos_docs = list(item + '\n' for item in pos_docs)
    resultFile.writelines(pos_docs)
    log.info('正向语料写入完毕：{} 条'.format(len(pos_docs)))

log.info('开始合并负向语料库数据：{} + {} -> {}'.format(output_neg_tmp, neg_merge, output_neg_file))
neg_docs = []
with open(neg_merge, 'r', encoding='utf-8') as baseFile, \
        open(output_neg_tmp, 'r', encoding='utf-8') as mergeFile, \
        open(output_neg_file, 'w', encoding='utf-8') as resultFile:
    baseList = baseFile.read().splitlines()
    log.debug('baseList数量{}'.format(len(baseList)))
    mergeList = mergeFile.read().splitlines()
    log.debug('mergeList数量{}'.format(len(mergeList)))
    neg_docs = baseList + mergeList
    log.debug('合并以后的数量{}'.format(len(neg_docs)))
    neg_docs = list(set(neg_docs))
    log.debug('去重以后的数量{}'.format(len(neg_docs)))
    # 增加自定义语料库的权重，即把自定义的语料库翻倍加入待训练数据
    neg_docs = neg_docs + list(set(list_neg_53kf)) * 100
    log.debug('增加自定义语料权重之后数量{}'.format(len(neg_docs)))
    neg_docs = list(item + '\n' for item in neg_docs)
    resultFile.writelines(neg_docs)
    log.info('负向语料写入完毕：{} 条'.format(len(neg_docs)))

log.info('程序正常结束')
