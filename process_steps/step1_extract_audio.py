import os
from celery import shared_task
import subprocess

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
        "-vn",  # 不要视频
        "-acodec", "pcm_s16le",  # 无损 wav
        "-ar", "16000",  # ASR 标准采样率
        "-ac", "1",  # 单声道（识别更稳）
        audio_path
    ]

    # 执行ffmpeg
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f'提取 {video_path} 音频完成, ，音频存放于:{audio_path}')
    return config_dic

if __name__ == '__main__':
    config_dic = {
        'video_path': "E:\\Project\\video2xhsnote\\exam_video\\example.mp4"
    }
    result = extract_audio(config_dic)
    print(result)