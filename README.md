# emotion

##第一期实现的功能
###1、对外提供4个接口：train / test / deploy / run
train:根据放入的语料数据，结合train/data下的预置判别词文件，训练新的模型文件sentiment.marshal（sentiment.marshal.3 for python3.x）
test: 导入train生成的sentiment.marshal文件，进行结果测试
deploy: 把neg.txt/pos.txt/sentiment.marshal发布到线上目录，并对上一次的模型文件进行备份
run:启动服务，对外进行正负向的判断服务


##第二期计划
###1、把训练过程在saas后台管理界面中实现
###2、对正向进行二级细分：喜爱、愉快、感谢
###3、对负向进行二级细分：抱怨、愤怒、厌恶、恐惧、悲伤
###4、在原有正负向判断返回接口里面，加上二级分类