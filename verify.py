"""
1、复制verify.xlsx到train目录下
2、载入模型
3、读取文件，对文本进行判断，
4、分数和正确与否写入文件，并计算准确率
"""
import os
import sys
import time

import openpyxl
from snownlp.sentiment import Sentiment

# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)

# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)

# 导入自开发模块
from common.log import Log

"""
全局变量
"""
log = Log()

POS_IDX = 0.6
NEG_IDX = 0.45

FLAG_NEG = -1
FLAG_POS = 1
FLAG_NUE = 0

t = time.time()

marshal_file = os.path.join(basePath, 'train/sentiment.marshal')
original_verify_file = os.path.join(basePath, 'train/data/verify.xlsx')
copy_verify_file = os.path.join(basePath, 'train/verify_' + str(int(t)) + '.xlsx')

senti = Sentiment()
senti.load(marshal_file)
log.info('模型载入成功：{}'.format(marshal_file))

# 读取原来的xlsx文件内容
original_verify_data = openpyxl.open(original_verify_file, read_only=False)
sheets = original_verify_data.get_sheet_names()
sheet_data = original_verify_data.get_sheet_by_name(sheets[0])
rows_data = list(sheet_data.rows)


def judge(text):
    s = senti.classify(text)
    if s >= POS_IDX:
        return s, FLAG_POS
    elif s <= NEG_IDX:
        return s, FLAG_NEG
    else:
        return s, FLAG_NUE


for row_data in rows_data[1:]:
    # print('{}\t{}\t{}\t{}\t{}\t\n'.format(row_data[0].value, row_data[1].value, row_data[2].value, row_data[3].value,row_data[4].value))
    cell_text = row_data[0]
    text = cell_text.value
    cell_expect = row_data[1]
    expect = cell_expect.value

    score, classify = judge(text)

    row_data[2].value = score
    row_data[3].value = classify
    if classify == expect:
        row_data[4].value = True
    else:
        row_data[4].value = False
        log.error('测试错误: 文本: {}    分值：{}'.format(text, score))

original_verify_data.save(copy_verify_file)

log.info("程序结束！")
