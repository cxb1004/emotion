from flask import current_app

from flask_module.config_blueprint import config_blueprint


@config_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return 'the flask server is running normally...'


@config_blueprint.route('/detail', methods=['GET', 'POST'])
def detail():
    app_config_info = 'Flask Web App configuration: '
    for key in current_app.config.keys():
        config_info = '\n  {} : {}'.format(key, current_app.config.get(key))
        app_config_info = app_config_info + config_info
    return app_config_info
