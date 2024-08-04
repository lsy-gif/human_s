from app import celery, redis_client, db
from utils import generate_audio_from_text, generate_video_via_api
from models import VideoRequest


@celery.task(bind=True)
def generate_video(self, request_id):
    try:
        request = VideoRequest.query.get(request_id)
        if request.input_text:
            request.input_audio_url = generate_audio_from_text(request.input_text)

        # 更新状态为 'processing'
        redis_client.set(f"request_{request_id}_status", "processing")
        request.video_status = 'processing'
        db.session.commit()

        # 调用生成视频的逻辑
        video_url = generate_video_via_api(request.input_audio_url, request.image, request.background)

        if request.input_audio_url:
            os.remove(request.input_audio_url)

        # 更新状态为 'completed'
        request.video_url = video_url
        request.video_status = 'completed'
        db.session.commit()

        redis_client.set(f"request_{request_id}_status", "completed")

    except Exception as e:
        # 任务出错，状态设置为 'error'
        request.video_status = 'error'
        db.session.commit()
        redis_client.set(f"request_{request_id}_status", "error")
        raise e
