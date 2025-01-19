import pytest
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取测试环境的API URL
API_URL = os.getenv("TEST_API_URL", "http://localhost:8000")
