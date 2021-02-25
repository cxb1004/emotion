"""
使用SnowNLP
"""
from snownlp import SnowNLP
from snownlp import sentiment
import os
import sys
# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)

input = "行了，别来烦我了"

print('文本：{} '.format(input))

words = SnowNLP(input).words
print('\n分词结果为[{}]'.format(words))

sentences = SnowNLP(input).sentences
print('\n分句结果为[{}]'.format(sentences))

score = SnowNLP(input).sentiments
print('\n情感打分结果为[{}]'.format(score))

input1 = '中華人民共和國'
han = SnowNLP(input1).han
print('\n繁体文本：{} \n简繁转换结果为[{}]'.format(input1, han))

pinyin = SnowNLP(input).pinyin
print('\n拼音转换结果为[{}]'.format(pinyin))

tags = SnowNLP(input).tags
print('\n词性标注结果为[{}]'.format(list(tags)))

# 相似度算法有点问题，慎用。得出的结果还需要自己重新进行分析。
input1 = '别烦'
sim = SnowNLP(input).sim(input1)
print('\n文本[{}] \n文本2[{}] \n相似度结果为[{}]'.format(input, input1, sim))

input = u'''自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。
它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。
自然语言处理是一门融语言学、计算机科学、数学于一体的科学。
因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，
所以它与语言学的研究有着密切的联系，但又有重要的区别。
自然语言处理并不是一般地研究自然语言，
而在于研制能有效地实现自然语言通信的计算机系统，
特别是其中的软件系统。因而它是计算机科学的一部分'''

tf = SnowNLP(input).tf
print('\n字频结果为[{}]'.format(tf))

idf = SnowNLP(input).idf
print('\n逆文本频率指数结果为[{}]'.format(idf))

summary = SnowNLP(input).summary(limit=3)
print('\n文本概括结果为[{}]'.format(summary))

keywords = SnowNLP(input).keywords(limit=4)
print('\n关键词结果为[{}]'.format(keywords))



# from snownlp.sentiment import Sentiment
#
# s1 = Sentiment()
# s2 = Sentiment()
# s1.load(os.path.join(basePath,'train/sentiment1.marshal'))
# s2.load(os.path.join(basePath,'train/sentiment2.marshal'))
# print(s1)
# print(s2)