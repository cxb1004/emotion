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

# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)

# 导入自开发模块
from common.log import Log
from emotionclassify import EmotionClassify
from config import Config

"""
全局变量
"""
log = Log()
baseConfig = Config()

train_folder = baseConfig.get_value('project', 'train_folder')
train_data_folder = baseConfig.get_value('project', 'train_data_folder')

FLAG_NEG = -1
FLAG_POS = 1
FLAG_NUE = 0

t = time.time()

marshal_file = os.path.join(train_folder, 'sentiment.marshal')
pos_53kf_corpus = os.path.join(train_data_folder, 'pos_53kf.txt')
neg_53kf_corpus = os.path.join(train_data_folder, 'neg_53kf.txt')

ec = EmotionClassify(modelPath=marshal_file, pos53kfPath=pos_53kf_corpus, neg53kfPath=neg_53kf_corpus)

# 以下代码是通过指定的excel测试文件进行测试，测试结果生成另一个excel文件
original_verify_file = os.path.join(basePath, 'train/data/verify.xlsx')
copy_verify_file = os.path.join(basePath, 'train/verify_' + str(int(t)) + '.xlsx')

# 读取原来的xlsx文件内容
original_verify_data = openpyxl.open(original_verify_file, read_only=False)
sheets = original_verify_data.get_sheet_names()
sheet_data = original_verify_data.get_sheet_by_name(sheets[0])
rows_data = list(sheet_data.rows)

for row_data in rows_data[1:]:
    cell_text = row_data[0]
    text = cell_text.value
    cell_expect = row_data[1]
    expect = cell_expect.value

    rtn = ec.classify(text)

    row_data[2].value = rtn.get(EmotionClassify.RTN_EMOTION_VALUE)
    row_data[3].value = rtn.get(EmotionClassify.RTN_EMOTION)
    if rtn.get(EmotionClassify.RTN_EMOTION) == expect:
        row_data[4].value = True
    else:
        row_data[4].value = False

original_verify_data.save(copy_verify_file)


# 以下代码是通过控制台输入进行判断：
ec.setConfigValue(None, 0.6, 0.4)


def menu():
    print('请输入要测试的内容：')
    inputTxt = input()
    if inputTxt == '0':
        print('成功退出')
        exit(0)
    rtn = ec.classify(inputTxt)
    print('测试结果：{}'.format(rtn))


print('资源已载入，请输入文本进行测试，退出请按0')

while 1 == 1:
    menu()
log.info("程序结束！")
