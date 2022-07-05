import os
from flask import Flask
from system.core.Converter import *
from application.config import app as config, log
from application.controllers import Example

app = Flask(__name__)

app.url_map.converters['regex'] = RegexConverter

for key in config:
    app.config[key] = config[key]
   
app.register_blueprint(Example.bp)

if not app.debug:
    from logging import FileHandler

    if not os.path.exists(log['LOG_PATH']):
        os.makedirs(log['LOG_PATH'])

    file_handler = FileHandler(filename=os.path.join(log['LOG_PATH'], log['LOG_NAME']))
    file_handler.setFormatter(log['LOG_FORMAT'])

    app.logger.setLevel(log['LOG_LEVEL'])
    app.logger.addHandler(file_handler)