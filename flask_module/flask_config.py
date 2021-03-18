class FlaskConfig():
    # 调试模式
    DEBUG = True
    # TODO 配置日志
    LOG_LEVEL = "DEBUG"

    # 设置密钥，可以通过 base64.b64encode(os.urandom(48)) 来生成一个指定长度的随机字符串
    # 开启session功能设置secret_key
    SECRET_KEY = "12345653KF654321"

    # flask_session的配置信息
    # SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    # SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    # SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=1)  # 使用 redis 的实例
    # PERMANENT_SESSION_LIFETIME = 24 * 60 * 60  # session 的有效期，单位是秒

    def __init__(self, _config):
        """项目配置核心类"""
        # 调试模式
        DEBUG = True

        # todo 配置日志
        LOG_LEVEL = "DEBUG"
        # pass

        # mysql数据库的配置信息

        # user = user
        # password = password
        # host = host
        # port = port
        # database = database
        # charset = charset

        # SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:%s/%s?charset=%s" % (user, password, host, port, database, charset)
        # # 动态追踪修改设置，如未设置只会提示警告
        # SQLALCHEMY_TRACK_MODIFICATIONS = False
        # # 查询时会显示原始SQL语句
        # SQLALCHEMY_ECHO = False

        # # 配置redis
        # REDIS_HOST = '127.0.0.1'  # 项目上线以后，这个地址就会被替换成真实IP地址，mysql也是
        # REDIS_PORT = 6379
