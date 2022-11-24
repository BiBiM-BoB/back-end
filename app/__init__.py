from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from logging.config import dictConfig
import os

from .models import db, ma

load_dotenv()
LOGGING_PATH = os.environ.get("LOGGING_PATH")

def create_app():
    # logging config
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': "/home/bibim/back-end/app/logs/bibim.app.log",
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
                'formatter': 'default',
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['file']
        }
    })

    # Flask app 시작
    app = Flask(__name__)

    # mysql
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://bibimbob:1q2w3e4r!@localhost:3306/devsecopsdb?charset=utf8mb4"
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    ma.init_app(app)

    db.app = app
    db.create_all()

    # mongodb
    # mongodb의 경우 service에서 class 형태로 연동함.

    # CORS
    CORS(app)

    # routing용 함수 만들기
    from .controllers import user, pipeline, security_result, test_render, jenkins, tool
    
    app.register_blueprint(test_render.bp)

    app.register_blueprint(user.bp)
    app.register_blueprint(pipeline.bp)
    app.register_blueprint(security_result.bp)
    # app.register_blueprint(jenkins.bp)
    app.register_blueprint(tool.bp)
    return app