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