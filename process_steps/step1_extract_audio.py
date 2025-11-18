import os
from celery import shared_task
from gevent.subprocess import Popen, PIPE  # ← 关键：改成 gevent 的 subprocess

@shared_task
def extract_audio(config_dic):
    video_path = config_dic.get('video_path')
    audio_dir = config_dic.get('audio_dir')
    os.makedirs(audio_dir, exist_ok=True)
    audio_path = os.path.abspath(os.path.join(audio_dir, os.path.basename(video_path).rsplit('.', 1)[0] + ".wav"))
    config_dic['audio_path'] = audio_path

    print(f'开始提取音频 {video_path}')

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ]

    # 🔥 使用 gevent-friendly Popen，不会阻塞 gevent 线程
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()  # 必须调用，不然 pipe 会阻塞

    if process.returncode != 0:
        raise RuntimeError(f"FFmpeg 提取音频失败：{stderr.decode('utf-8', 'ignore')}")

    print(f'提取 {video_path} 音频完成，音频存放于: {audio_path}')

    return config_dic


if __name__ == '__main__':
    config_dic = {
        'video_path': "E:\\Project\\video2xhsnote\\exam_video\\example.mp4",
        'audio_dir': "E:\\Project\\video2xhsnote\\exam_audio"
    }
    result = extract_audio(config_dic)
    print(result)
