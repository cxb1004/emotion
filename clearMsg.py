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
from common.utils import removeFileIfExists

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
            sentence = line_data[3]
        except:
            log.error('数据出错{}'.format(line_data))
        else:
            bs = BeautifulSoup(sentence, "html.parser")
            line = bs.text
            line = line.replace('\n', '')
            corpus_data.append(bs.text)

removeFileIfExists(out_corpus_file)
with open(out_corpus_file, 'w', encoding='utf-8') as out_corpus_file:
    out_corpus_file.writelines(corpus_data)

log.info('程序正常结束')
