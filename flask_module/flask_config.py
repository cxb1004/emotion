class FlaskConfig():
    # 调试模式
    DEBUG = False
    # 配置日志
    LOG_LEVEL = "INFO"

    # 设置密钥，可以通过 base64.b64encode(os.urandom(48)) 来生成一个指定长度的随机字符串
    # 开启session功能设置secret_key
    SECRET_KEY = "12345653KF654321"