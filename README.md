# emotion

##第一期实现的功能


###【文件说明】

####1、clearMsg.py

主要功能：把数据源的数据集，做初步的数据清洗，形成corpus.txt，
这部分功能理论上是应该在业务系统导出数据的时候实现，这里只是做模拟实现。

输入文件：msg.txt

输出文件: corpus.txt

目前清洗的内容包括：

1)过滤掉非人工说的话（去除机器应答或是预设答案）

2)去掉html标签

3)去掉快服表情符

4)去掉回车、tab、以及特殊符号

5)去掉重复数据


####2、prapareTrainData.py
根据自定义的语料库corpus.txt和train/data下的正负词库，区分语料库里的正向、负向、中性句
然后和已发布的neg.txt/pos.txt进行整合，最终获得训练模型使用的文件

【主业务逻辑】

1)获取待合并的正负向语料库（要么是线上deploy的，要么是默认的_default）

2)如果train/data目录下的数据文件不存在，停止应用

3)按行对待训练的预料进行正负向判断

3.1) 使用模型进行正负向判断，如果结果是正向或是负向，就直接判断；如果是中性继续下面的判断

3.2) 使用自定义词库进行正负向判断。使用文本相似度算法，用正负向自定义语料库进行相似度比较

分别获得正负向语料库的最大相似度（相似度必须大于设定的阀值）

3.3) 使用正负向词库进行正负向判断，

使用jieba进行分词，匹配正负向词库的数量，数量多切超过阀值的正向/负向胜出

3.4) 判别结果分别写入tmm文件，该文件用于人工审阅自动正负向判别的结果

判断结果为正向，写入pos_add.tmp

判断结果为负向，写入neg_add.tmp

判断结果为中性，写入neu_add.tmp

4)结合步骤1中确定的待合并的语料库，把正负向语料分别进行合并，获得文件:

neg.txt = neg_add.tmp + neg_merge(线上neg.txt 或 默认 neg_default.txt)

pos.txt = pos_add.tmp + pos_merge(线上pos.txt 或 默认 pos_default.txt)

这两个文件将会用于模型训练


【输入文件】
deploy目录下：
    neg.txt / pos.txt / sentiment.marshal ：使用既有的模型，对原始语料进行正负向判断
    corpus.txt：
train/data目录下：
    neg_default.txt / pos_default.txt：在没有deploy的数据下，使用默认数据进行训练
    neg_53kf.txt / pos_53kf.txt：
    neg_words.txt / pos_words.txt：

【输出文件】
train目录下：
    neg_add.tmp / pos_add.tmp / neu_add.tmp
    neg.txt / pos.txt
    sentiment.marshal


####3、train.py
####4、verify.py
####5、deploy.py
####6、emotionclassify.py
####7、config.py

读取同目录下的config.ini内容，为项目提供配置信息

注意：config.ini必须在同一目录

##第二期计划
###1、把训练过程在saas后台管理界面中实现
###2、对正向进行二级细分：喜爱、愉快、感谢
###3、对负向进行二级细分：抱怨、愤怒、厌恶、恐惧、悲伤
###4、在原有正负向判断返回接口里面，加上二级分类