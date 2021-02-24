"""
清洗msg.txt，生成corpus.txt
"""
# 导入系统模块、第三方模块
import os
import sys

from bs4 import BeautifulSoup

# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)

# 导入自开发模块
from common.log import Log
from common.utils import removeFileIfExists, remove53Emoji

log = Log()

input_msg_file = os.path.join(basePath, 'train/msg.txt')
out_corpus_file = os.path.join(basePath, 'train/corpus.txt')

if not os.path.isfile(input_msg_file):
    log.error('原始语料库文件不存在：{}'.format(input_msg_file))
    log.info('程序异常结束')
    exit(9)
corpus_data = []
with open(input_msg_file, 'r', encoding='utf-8') as inputFile:
    alllines = inputFile.readlines()
    for line in alllines[1:]:
        line_data = line.split('\t')
        try:
            # 如果文本里面遇到CR/LF字符，readlines就会截断文本，导致下一行数据下标越界的错误
            # 解决方案是升级代码，先缓存当前行数据并读取下一行数据，下行数据没问题，就处理当前行数据；
            # 如果下行数据出错（下标越界），就把下行文本和当前文本合并，再读取下下行的文本数据；
            sentence = str(line_data[3])
        except:
            # 存在出错的概率，如果聊天数据里面
            log.warn('数据出错{}'.format(line_data))
        else:
            bs = BeautifulSoup(sentence, "html.parser")
            line = bs.text
            # 去掉53表情符、中间的换行符、\t、以及特殊符号
            line = remove53Emoji(line.replace('\n', '').replace('\\t', '').replace('☞', ''))
            corpus_data.append(line + '\n')

log.debug('开始写入文件:{}'.format(out_corpus_file))
removeFileIfExists(out_corpus_file)
with open(out_corpus_file, 'w', encoding='utf-8') as outFile:
    outFile.writelines(corpus_data)
log.debug('文件写入完毕:{}'.format(out_corpus_file))
log.info('程序正常结束')
