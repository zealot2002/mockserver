class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/mock'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    
    # 添加这些配置
    HOST = '0.0.0.0'
    PORT = 5001 