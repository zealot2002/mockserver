# 导入所有路由蓝图
from app.routes.merchant_routes import bp as merchant_bp
from app.routes.batch_routes import bp as batch_bp

# 导出蓝图供 app/__init__.py 使用
__all__ = ['merchant_bp', 'batch_bp'] 