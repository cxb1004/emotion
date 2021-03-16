import os
import sys

# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)
from common.log import Log
from emotionclassify import EmotionClassify
from config import Config

log = Log()
baseConfig = Config()

deploy_path = baseConfig.get_value('project', 'deploy_folder')
file_model = baseConfig.get_value('project', 'model_filename_t')
file_corpus_pos_53kf_txt = baseConfig.get_value('project', 'corpus_pos_53kf_filename')
file_corpus_neg_53kf_txt = baseConfig.get_value('project', 'corpus_neg_53kf_filename')

path_model = os.path.join(deploy_path, file_model)
path_53kf_pos_txt = os.path.join(deploy_path, file_corpus_pos_53kf_txt)
path_53kf_neg_txt = os.path.join(deploy_path, file_corpus_neg_53kf_txt)

ec = EmotionClassify(path_model, path_53kf_pos_txt, path_53kf_neg_txt)


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
