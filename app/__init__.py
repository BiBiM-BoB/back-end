from flask import Flask
from .models import db, ma

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://bibimbob:1q2w3e4r!@localhost:3306/devsecopsdb?charset=utf8mb4"
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    ma.init_app(app)

    db.app = app
    db.create_all()

    # routing
    from .controllers import user, pipeline, security_result
    
    app.register_blueprint(user.bp)
    app.register_blueprint(pipeline.bp)
    app.register_blueprint(security_result.bp)
    return app