from celery import Celery
import time

app = Celery(
    'video_tasks',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/1',
    result_expires=3600
)

@app.task
def process_video_task(file_path):
    print(f'开始处理视频:{file_path}')
    time.sleep(5)
    return f'完成处理:{file_path}'
