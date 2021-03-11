# coding: utf-8
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from config.app_config import create_app
from config.db_config import Config


from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
app = create_app()


# 读取配置

app.config.from_object(Config)
# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


class CcsCompanyLabel(db.Model):
    print("CcsCompanyLabel is running")
    __tablename__ = 'ccs_company_label'
    __table_args__ = (
        db.Index('comAndMonth', 'company_id', 'attribution_month'),
    )

    id = db.Column(db.String(36), primary_key=True)
    company_id = db.Column(db.Integer)
    industry_one = db.Column(db.Integer)
    industry_two = db.Column(db.Integer)
    uv = db.Column(db.Integer)
    uv_level = db.Column(db.Integer)
    uv_divide = db.Column(db.String(30))
    consult = db.Column(db.Integer)
    consult_level = db.Column(db.Integer)
    consult_divide = db.Column(db.String(30))
    count = db.Column(db.Integer)
    count_level = db.Column(db.Integer)
    count_divide = db.Column(db.String(30))
    talk_valid = db.Column(db.Integer)
    talk_valid_level = db.Column(db.Integer)
    talk_valid_divide = db.Column(db.String(30))
    chat_msg = db.Column(db.Integer)
    chat_msg_level = db.Column(db.Integer)
    chat_msg_divide = db.Column(db.String(30))
    robot_clew = db.Column(db.Integer)
    robot_clew_level = db.Column(db.Integer)
    robot_clew_divide = db.Column(db.String(30))
    all_clew = db.Column(db.Integer)
    all_clew_level = db.Column(db.Integer)
    all_clew_divide = db.Column(db.String(30))
    arg_responsetime = db.Column(db.Integer)
    arg_responsetime_level = db.Column(db.Integer)
    arg_responsetime_divide = db.Column(db.String(30))
    talk_num = db.Column(db.Integer)
    talk_num_level = db.Column(db.Integer)
    talk_num_divide = db.Column(db.String(30))
    seats_amount = db.Column(db.Integer)
    seats_amount_level = db.Column(db.Integer)
    seats_amount_divide = db.Column(db.String(30))
    pay_money = db.Column(db.Numeric(10, 2))
    pay_money_level = db.Column(db.Integer)
    pay_money_divide = db.Column(db.String(30))
    consult_conversion = db.Column(db.String(20))
    consult_conversion_level = db.Column(db.Integer)
    consult_conversion_divide = db.Column(db.String(30))
    clue_conversion = db.Column(db.String(20))
    clue_conversion_level = db.Column(db.Integer)
    clue_conversion_divide = db.Column(db.String(30))
    attribution_month = db.Column(db.Integer)
    update_time = db.Column(db.DateTime)
