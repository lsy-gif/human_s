from app import db
from datetime import datetime


# 用户表模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(255))
    nickname = db.Column(db.String(50))
    phone = db.Column(db.String(20), unique=True)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)


# 视频请求表模型
class VideoRequest(db.Model):
    __tablename__ = 'video_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)  # 添加索引
    input_text = db.Column(db.Text)
    input_audio_url = db.Column(db.String(255), nullable=True)
    video_status = db.Column(db.String(50), default='pending', index=True)  # 添加索引
    video_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# 生成视频表模型
class GeneratedVideo(db.Model):
    __tablename__ = 'generated_videos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)  # 添加索引
    video_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
