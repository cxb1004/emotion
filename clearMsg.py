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

"""
对话资料type说明：
type	   含义	            客服	    访客      说明
a	    快问快答（答）        ✔	            用预设回复对访客的提问进行快捷回答
b	    繁忙提示语	        ✔	            当客服繁忙没有应答的时候给出的自动回复
g	    访客消息                      ✔      访客说话
h	    接通提示语	        ✔	            接通客服的默认问候及提问
j   	智能引导	            ✔	            
k	    快捷提问		                 ✔      访客在预设问题范围内进行快捷提问
l	    访客留言		                 ✔      访客说话
m	    场景引导	            ✔	            
o	    退出挽留		                 ✔      当访客退出的时候，自动弹出的消息
p	    客服消息	            ✔	            客服说话
q	    快问快答（问）	             ✔
r	    客服留言	            ✔	            客服说话
u	    机器人	            ✔	
w	    微信预约消息	        ✔	
z	    访客填写快捷表单	             ✔      访客填写的表单数据及
"""
# 第一次训练的时候，把所有的数据都分析进去
# 第二次之后，可以把非人为数据过滤掉
# filter_talk_tag = {'e': 'e', 'a': 'a', 'b': 'b', 'h': 'h', 'j': 'j', 'k': 'k', 'm': 'm', 'o': 'o', 'q': 'q', 'u': 'u', 'w': 'w' }
filter_talk_tag = {'e': 'e'}

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
            tag = str(line_data[1])
            # 过滤掉非人为数据
            if filter_talk_tag.get(tag) is not None:
                continue
            sentence = str(line_data[3])
        except:
            log.warn('数据出错{}'.format(line_data))
            continue
        else:
            bs = BeautifulSoup(sentence, "html.parser")
            line = bs.text
            # 去掉53表情符、中间的换行符、\t、以及特殊符号
            line = remove53Emoji(line.replace('\n', '').replace('\\t', '').replace('☞', ''))
            corpus_data.append(line + '\n')
# 去重
log.debug('去重前数据量为{}'.format(len(corpus_data)))
corpus_data = list(set(corpus_data))
log.debug('去重后数据量为{}'.format(len(corpus_data)))

log.debug('开始写入文件:{}'.format(out_corpus_file))
removeFileIfExists(out_corpus_file)
with open(out_corpus_file, 'w', encoding='utf-8') as outFile:
    outFile.writelines(corpus_data)
log.debug('文件写入完毕:{}'.format(out_corpus_file))
log.info('程序正常结束')
