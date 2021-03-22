from flask import Blueprint


emotion_blueprint = Blueprint('emotion_blueprint', __name__)

# 这一句必须放在Blueprint()之下，否则会出现ImportError: cannot import name 'xxx_blueprint' 的错误
from flask_module.emotion_blueprint import emotion_func
