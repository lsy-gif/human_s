# 配置文件，用于全局项目配置
class Config:
    SECRET_KEY = 'your-secret-key'  # Flask应用的密钥
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/dbname'  # 数据库连接字符串
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭SQLAlchemy的事件系统

    # Celery配置信息
    CELERY_BROKER_URL = 'pyamqp://guest@localhost//'  # 消息代理（使用RabbitMQ）
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # 任务结果存储（使用Redis）

    # Redis配置
    REDIS_URL = 'redis://localhost:6379/0'  # Redis连接字符串
