from app import db
from models import User, VideoRequest, GeneratedVideo

db.create_all()  # 创建表结构

# 添加测试用户
user = User(avatar='http://example.com/avatar.jpg', nickname='testuser', phone='1234567890')
db.session.add(user)
db.session.commit()

print("Database tables created and sample data added.")
