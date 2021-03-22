# emotion

##第一期实现的功能


###【文件说明】

####1、clearMsg.py

#####【主要业务逻辑】
把数据源的数据集，做初步的数据清洗，形成corpus.txt，
这部分功能理论上是应该在业务系统导出数据的时候实现，这里只是做模拟实现。

目前清洗的内容包括：

1)过滤掉非人工说的话（去除机器应答或是预设答案）

2)去掉html标签

3)去掉快服表情符

4)去掉回车、tab、以及特殊符号

5)去掉重复数据

#####【输入文件】
msg.txt

#####【输出文件】
corpus.txt

####2、prapareTrainData.py
根据自定义的语料库corpus.txt和train/data下的正负词库，区分语料库里的正向、负向、中性句
然后和已发布的neg.txt/pos.txt进行整合，最终获得训练模型使用的文件

#####【主业务逻辑】

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

#####【输入文件】

deploy目录下：

    neg.txt / pos.txt / sentiment.marshal ：使用既有的模型，对原始语料进行正负向判断
    corpus.txt：
    
train/data目录下：

    neg_default.txt / pos_default.txt：在没有deploy的数据下，使用默认数据进行训练
    neg_53kf.txt / pos_53kf.txt：
    neg_words.txt / pos_words.txt：

#####【输出文件】

train目录下：

    neg_add.tmp / pos_add.tmp / neu_add.tmp
    neg.txt / pos.txt
    sentiment.marshal


####3、train.py
#####【主要业务逻辑】
根据自定义的语料库corpus.txt和train/data下的正负词库，区分语料库里的正向、负向、中性句
然后和已发布的neg.txt/pos.txt进行整个，之后训练出sentiment.marshal

#####【输入文件】
neg.txt / pos.txt: 训练用的正负向语料库

#####【输出文件】
sentiment.marshal：训练产生的文件，python3是sentiment.marshal.3 

####4、verify.py
#####【主要业务逻辑】
有两个业务逻辑：

1、读入train/data/verify.xlsx，对文件里面的数据进行正负向判断，对结果按时间生成另一个excel文件，方便验证
(这个功能暂时注释掉，随时可以启用)

2、在命令行生成操作界面，输入内容进行判断，输入0退出

#####【输入文件】
/train/data/verify.xlsx

#####【输出文件】

/train/data/verify_<时间戳>.xlsx

####5、deploy.py
#####【主要业务逻辑】

发布流程：

1)检查上述文件是否存在

2)查询目标目录文件是否存在

3)对已发布的资源进行备份（按发布时间，新建目录备份文件）

4)移动文件

#####【输入文件】
1)train/data目录下：neg_53kf.txt/pos_53kf.txt

2)train目录下：neg.txt / pos.txt

3)train目录下：sentiment.marshal.3

#####【输出文件】
把上述5个文件复制到deploy目录下

####6、emotionclassify.py
情感分析的主类
具体的调用方法可以参见verify.py
#####【举例】
from emotionclassify import EmotionClassify
ec = EmotionClassify(modelPath=marshal_file, pos53kfPath=pos_53kf_corpus, neg53kfPath=neg_53kf_corpus)
ec.setConfigValue(None, 0.6, 0.4)
rtn = ec.classify(inputTxt)

#####【主要逻辑】
1) 创建对象的时候，需要输入3个参数：
modelPath：模型文件位置，其中模型文件名应该是sentiment.marshal，系统自动会判断python3加上.3后缀
pos53kfPath / neg53kfPath：自定义的正负向语料库，用于文本相似度判别
2) 设置参数setConfigValue(simValue=None, posValue=None, negValue=None)
simValue：文本相似度的阀值，大于等于该值以上被认为是相似度达标
posValue：模型判断的正向判定阀值。大于等于该值的是正向
negValue：模型判断的负向判定阀值。小于等于该值的是负向
3) 返回参数
返回示例：{'emotion': 1, 'emotion_tag': 'positive', 'emotion_value': 0.9021792448075795, 'classify': 'Model'}
emotion：情感分类ID    1=正向  -1=负向  0=中性
emotion_tag：情感分类标签    positive/negative/neutral
classify：分类的工具   Model：是通过模型判断   CosSim：文本相似度算法判断
emotion_value:情感判断的值
当Model：是指模型计算的情感值，小数，值越大越是正向，越小越是负向
当CosSim：文本相似度，是指正向/负向文本相似度的最大值


####7、config.py
#####【主要业务逻辑】
读取同目录下的config.ini内容，为项目提供配置信息

注意：config.ini必须在同一目录

##Flask 部署说明
###文件结构

---
 - start_flask.py
 - flask_module
 
   |- __init__.py：启动Flask App应用，包括注册各个业务模块
   
   |- flask_config.py：使用Config对象创建Flask app对象
   
   |- flask_log.py：Flask Web App使用的日志
   
   |- result_json: http返回json格式的数据 
   
   |- config_blueprint：配置模块
      
        |- __init__.py: 创建config_blueprint模块
       
        |- config_info.py: 提供两个对外的功能，一个是根目录信息，一个是Flask Web App的所有配置参数
   
   |- emotion_blueprint：情感分析模块
   
        |- __init__.py：创建emotion_blueprint模块
        
        |- emotion_func.py: 情感分析模块对外的web接口
        
        |- emotionclassify.py：情感分析业务类
        
###使用说明
#### 初始化创建
1、按结构复制文件目录：
 
 -  start_flask.py
 -  /flask_module/__init__.py
 -  /flask_module/flask_config.py
 -  /flask_module/flask_log.py
 -  /flask_module/result_json.py
 -  /flask_module/config_blueprint/__init__.py
 -  /flask_module/config_blueprint/config_info.py

复制之后启动start_flask可以启动应用

#### 新增业务模块
1、新建业务模块目录xxx

2、在业务模块目录下新建__init__.py，并添加代码

    from flask import Blueprint
    
    emotion_blueprint = Blueprint('emotion_blueprint', __name__)

    # 这一句必须放在Blueprint()之下，否则会出现ImportError: cannot import name 'xxx_blueprint' 的错误
    from flask_module.emotion_blueprint import emotion_func
    
3、在业务模块目录下建立业务接口代码文件emotion_func （和上面的import一致）

里面建立各种接口的域名映射和业务代码，也可以引入其他业务代码

4、在flask_module/__init__.py里面，把建好的blueprint注册到app里面

    app.register_blueprint(emotion_blueprint, url_prefix='/emotion')
      


##第二期计划
###1、把训练过程在saas后台管理界面中实现
###2、对正向进行二级细分：喜爱、愉快、感谢
###3、对负向进行二级细分：抱怨、愤怒、厌恶、恐惧、悲伤
###4、在原有正负向判断返回接口里面，加上二级分类