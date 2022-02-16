""" 接口文件设置"""
from flask import Flask


def  create_app():
    app = Flask(__name__)
    app.config['ERROR_404_HELP'] = False
    return app


app = create_app()

from CookiePool.api.cookies import *