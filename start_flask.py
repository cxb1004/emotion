# 系统包类

from flask_script import Manager

# 自定义的包类
# from flask_app import init_app, db, environment
from config import KFConfig
from flask_module import init_app

# 初始化配置
baseConfig = KFConfig()

# 使用配置文件，提取必要的参数，创建Flask App对象
app = init_app()

# 使用终端脚本工具启动和管理flask
manager = Manager(app)

# 运行Flask Manager，启动web服务
if __name__ == '__main__':
    manager.run()
