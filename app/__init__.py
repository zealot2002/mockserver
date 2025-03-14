from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
from config import Config

db = SQLAlchemy()

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

template = {
    "swagger": "2.0",
    "info": {
        "title": "宠物仓库管理系统",
        "description": "宠物仓库管理系统API文档",
        "version": "1.0.0",
        "contact": {
            "email": "support@example.com"
        }
    }
}

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 简化 CORS 配置，允许所有源
    CORS(app)
    
    db.init_app(app)
    Swagger(app, config=swagger_config, template=template)
    
    # 注册路由
    from app.routes import merchant_bp, batch_bp, task_bp
    app.register_blueprint(merchant_bp)
    app.register_blueprint(batch_bp)
    app.register_blueprint(task_bp)
    
    return app 