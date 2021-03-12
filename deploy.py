"""
发布功能
一共有5个文件需要发布：
1、neg_53kf.txt/pos_53kf.txt
2、neg.txt / pos.txt
3、sentiment.marshal.3

发布流程：
1、检查上述文件是否存在
2、查询目标目录文件是否存在
3、对已发布的资源进行备份（按发布时间，新建目录备份文件）
4、移动文件
"""
import os
import sys

# 当前目录
basePath = os.path.abspath(os.path.dirname(__file__))
# 设置当前目录为执行运行目录
sys.path.append(basePath)

from config import Config
from common.log import Log
from common.utils import file_update_time_format, isFileExist, get_timestamp, copyFile

baseConfig = Config()
log = Log()

log.info('开始执行deploy.py')
log.info('开始发布前的检查工作...')

# 准备发布的文件的名称
model_filename_r = baseConfig.get_value('project', 'model_filename_r')
# 训练模型使用的正负向语料库
corpus_pos_filename = baseConfig.get_value('project', 'corpus_pos_filename')
corpus_neg_filename = baseConfig.get_value('project', 'corpus_neg_filename')
# 快服自定义正负向语料库
corpus_pos_53kf_filename = baseConfig.get_value('project', 'corpus_pos_53kf_filename')
corpus_neg_53kf_filename = baseConfig.get_value('project', 'corpus_neg_53kf_filename')

# 训练目录
train_folder = baseConfig.get_value('project', 'train_folder')
train_data_folder = baseConfig.get_value('project', 'train_data_folder')
# 发布目录
deploy_folder = baseConfig.get_value('project', 'deploy_folder')
# 备份目录
backup_folder = os.path.join(deploy_folder, get_timestamp('ymdhms'))
os.makedirs(backup_folder)

# 组装文件全路径
model_file_path_r = os.path.join(train_folder, model_filename_r)
corpus_pos_path = os.path.join(train_folder, corpus_pos_filename)
corpus_neg_path = os.path.join(train_folder, corpus_neg_filename)
corpus_pos_53kf_path = os.path.join(train_data_folder, corpus_pos_53kf_filename)
corpus_neg_53kf_path = os.path.join(train_data_folder, corpus_neg_53kf_filename)

if isFileExist(model_file_path_r):
    log.info('准备发布的文件:{}  更新时间：{}'.format(model_file_path_r, file_update_time_format(model_file_path_r)))
else:
    log.error('没有找到准备发布的文件：{}'.format(model_file_path_r))
    exit(999)

if isFileExist(corpus_pos_path):
    log.info('准备发布的文件:{}  更新时间：{}'.format(corpus_pos_path, file_update_time_format(corpus_pos_path)))
else:
    log.error('没有找到准备发布的文件：{}'.format(corpus_pos_path))
    exit(999)

if isFileExist(corpus_neg_path):
    log.info('准备发布的文件:{}  更新时间：{}'.format(corpus_neg_path, file_update_time_format(corpus_neg_path)))
else:
    log.error('没有找到准备发布的文件：{}'.format(corpus_neg_path))
    exit(999)

if isFileExist(corpus_pos_53kf_path):
    log.info('准备发布的文件:{}  更新时间：{}'.format(corpus_pos_53kf_path, file_update_time_format(corpus_pos_53kf_path)))
else:
    log.error('没有找到准备发布的文件：{}'.format(corpus_pos_53kf_path))
    exit(999)

if isFileExist(corpus_neg_53kf_path):
    log.info('准备发布的文件:{}  更新时间：{}'.format(corpus_neg_53kf_path, file_update_time_format(corpus_neg_53kf_path)))
else:
    log.error('没有找到准备发布的文件：{}'.format(corpus_neg_53kf_path))
    exit(999)

log.info('开始备份线上数据')
online_model_file_path = os.path.join(deploy_folder, model_filename_r)
online_corpus_pos_path = os.path.join(deploy_folder, corpus_pos_filename)
online_corpus_neg_path = os.path.join(deploy_folder, corpus_neg_filename)
online_corpus_pos_53kf_path = os.path.join(deploy_folder, corpus_pos_53kf_filename)
online_corpus_neg_53kf_path = os.path.join(deploy_folder, corpus_neg_53kf_filename)

if isFileExist(online_model_file_path):
    log.info('备份的文件:{}  更新时间：{}'.format(online_model_file_path, file_update_time_format(online_model_file_path)))
    copyFile(online_model_file_path, backup_folder)
else:
    log.warn('没找到准备备份的文件：{}'.format(online_model_file_path))

if isFileExist(online_corpus_pos_path):
    log.info('备份的文件:{}  更新时间：{}'.format(online_corpus_pos_path, file_update_time_format(online_corpus_pos_path)))
    copyFile(online_corpus_pos_path, backup_folder)
else:
    log.warn('没找到准备备份的文件：{}'.format(online_corpus_pos_path))

if isFileExist(online_corpus_neg_path):
    log.info('备份的文件:{}  更新时间：{}'.format(online_corpus_neg_path, file_update_time_format(online_corpus_neg_path)))
    copyFile(online_corpus_neg_path, backup_folder)
else:
    log.warn('没找到准备备份的文件：{}'.format(online_corpus_neg_path))

if isFileExist(online_corpus_pos_53kf_path):
    log.info(
        '备份的文件:{}  更新时间：{}'.format(online_corpus_pos_53kf_path, file_update_time_format(online_corpus_pos_53kf_path)))
    copyFile(online_corpus_pos_53kf_path, backup_folder)
else:
    log.warn('没找到准备备份的文件：{}'.format(online_corpus_pos_53kf_path))

if isFileExist(online_corpus_neg_53kf_path):
    log.info(
        '备份的文件:{}  更新时间：{}'.format(online_corpus_neg_53kf_path, file_update_time_format(online_corpus_neg_53kf_path)))
    copyFile(online_corpus_neg_53kf_path, backup_folder)
else:
    log.warn('没找到准备备份的文件：{}'.format(online_corpus_neg_53kf_path))

log.info('备份完成：{}'.format(backup_folder))

log.info('发布中...')
copyFile(model_file_path_r, deploy_folder, True)
log.info('   文件发布:{}'.format(model_filename_r))
copyFile(corpus_pos_path, deploy_folder, True)
log.info('   文件发布:{}'.format(corpus_pos_filename))
copyFile(corpus_neg_path, deploy_folder, True)
log.info('   文件发布:{}'.format(corpus_neg_filename))
copyFile(corpus_pos_53kf_path, deploy_folder, True)
log.info('   文件发布:{}'.format(corpus_pos_53kf_filename))
copyFile(corpus_neg_53kf_path, deploy_folder, True)
log.info('   文件发布:{}'.format(corpus_neg_53kf_filename))
log.info('发布完成，请在发布目录下查看最新的模型文件，并重启主应用：{}'.format(deploy_folder))

log.info('结束执行deploy.py')
