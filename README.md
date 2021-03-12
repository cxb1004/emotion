# emotion

##第一期实现的功能
###1、对外提供4个接口：train / test / deploy / run
train:根据放入的语料数据，结合train/data下的预置判别词文件，训练新的模型文件sentiment.marshal（sentiment.marshal.3 for python3.x）
test: 导入train生成的sentiment.marshal文件，进行结果测试
deploy: 把neg.txt/pos.txt/sentiment.marshal发布到线上目录，并对上一次的模型文件进行备份
run:启动服务，对外进行正负向的判断服务

【文件说明】

1、clearMsg.py

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


2、prapareTrainData.py

7、config.py

读取同目录下的config.ini内容，为项目提供配置信息
注意：config.ini必须在同一目录

##第二期计划
###1、把训练过程在saas后台管理界面中实现
###2、对正向进行二级细分：喜爱、愉快、感谢
###3、对负向进行二级细分：抱怨、愤怒、厌恶、恐惧、悲伤
###4、在原有正负向判断返回接口里面，加上二级分类