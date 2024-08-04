from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
import redis
import os

app = Flask(__name__)
app.config.from_object('config.Config')  # 加载配置

db = SQLAlchemy(app)  # 初始化SQLAlchemy

redis_client = redis.StrictRedis.from_url(app.config['REDIS_URL'])  # 初始化Redis客户端


# 初始化Celery
def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery


celery = make_celery(app)

import celery_tasks  # 加载Celery任务模块


# 创建和提交视频生成请求的API
@app.route('/submit_request', methods=['POST'])
def submit_request():
    user_id = request.json['user_id']
    input_text = request.json.get('input_text')
    input_audio_url = request.json.get('input_audio_url')
    image = request.json.get('image', 'default_image')
    background = request.json.get('background', 'default_background')

    # 创建新的视频请求记录
    video_request = VideoRequest(
        user_id=user_id,
        input_text=input_text,
        input_audio_url=input_audio_url,
        image=image,
        background=background,
        video_status='pending'
    )

    db.session.add(video_request)
    db.session.commit()  # 提交记录

    # 将任务状态设置为'pending'，并存储在Redis中
    redis_client.set(f"request_{video_request.id}_status", "pending")

    # 提交异步任务到Celery
    celery_tasks.generate_video.apply_async((video_request.id,))
    return jsonify({'request_id': video_request.id}), 202


# 获取任务状态的API
@app.route('/status/<request_id>', methods=['GET'])
def status(request_id):
    status = redis_client.get(f"request_{request_id}_status")
    if status:
        return jsonify({'status': status.decode('utf-8')}), 200
    else:
        return jsonify({'status': 'unknown'}), 404


# 获取生成的视频URL的API
@app.route('/generated_video_url/<request_id>', methods=['GET'])
def generated_video_url(request_id):
    video_request = VideoRequest.query.get(request_id)
    return jsonify({'video_url': video_request.video_url}), 200


# 获取用户历史生成视频的API
@app.route('/history/<user_id>', methods=['GET'])
def history(user_id):
    history = GeneratedVideo.query.filter_by(user_id=user_id).all()
    return jsonify([{'video_url': video.video_url, 'created_at': video.created_at} for video in history]), 200


if __name__ == '__main__':
    app.run(debug=True)
