from flask import Flask
from system.core.converter import *
from application.config import app as app_config, config
from application.controllers import Example

app = Flask(__name__)

app.url_map.converters['regex'] = RegexConverter

for key in app_config:
    app.config[key] = app_config[key]
   
app.register_blueprint(Example.bp)