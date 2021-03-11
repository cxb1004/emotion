import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from config.app_config import create_app
from controller.info_controller import infoModule
from controller.test_controller import testModule
from controller.f_sqlAlchemy_controller import sqlAlchemyModule
from controller.send_request_test import sendRequestTestModule

app = create_app()

app.register_blueprint(infoModule, url_prefix='/infoModule')
app.register_blueprint(testModule, url_prefix='/testModule')
app.register_blueprint(sqlAlchemyModule, url_prefix='/sqlAlchemyModule')
app.register_blueprint(sendRequestTestModule, url_prefix='/sendRequestTestModule')


@app.route('/')
def hello_world():
    app.logger.info("#######flask_test_is_running!!")
    return 'flask_test is running!!'


if __name__ == '__main__':

    app.logger.info("flask_test_is_running!!")

    app.run(port=8088, host='0.0.0.0', debug=True, threaded=True, processes=2)
   # app.run(port=8088, host='0.0.0.0', debug=True)


    """
        命令行运行：
        flask run -p 9001
        python3 -m flask run -p 8088
        
        python app.py runserver 
        python app.py runserver -p port -h host 
    """



