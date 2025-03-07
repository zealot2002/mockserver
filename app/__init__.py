from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
api = Api(
    title='商家管理系统',
    description='商家管理系统API文档',
    version='1.0',
    doc='/docs'
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 简化 CORS 配置，允许所有源
    CORS(app)
    
    db.init_app(app)
    api.init_app(app)
    
    # 注册路由
    from app.routes import merchant_bp, batch_bp
    app.register_blueprint(merchant_bp)
    app.register_blueprint(batch_bp)
    
    return app 