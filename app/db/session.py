from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging
import os
from logging.handlers import TimedRotatingFileHandler

# 创建日志目录
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'log')
os.makedirs(log_dir, exist_ok=True)

# 配置 SQLAlchemy 日志
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.INFO)

# 创建文件处理器
log_file = os.path.join(log_dir, 'sql.log')
file_handler = TimedRotatingFileHandler(
    log_file,
    when='H',
    interval=1,
    backupCount=24
)
file_handler.setLevel(logging.INFO)

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 添加处理器到日志记录器
logger.addHandler(file_handler)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
