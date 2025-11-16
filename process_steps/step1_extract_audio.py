import os
from celery import shared_task
import subprocess

@shared_task
def extract_audio(config_dic):
    video_path = config_dic.get('video_path')
    output_dir = '../audio'
    os.makedirs(output_dir, exist_ok=True)
    output_audio = os.path.abspath(os.path.join('../audio', os.path.basename(video_path).rsplit('.', 1)[0] + ".wav"))
    config_dic['output_audio'] = output_audio
    print(f'开始提取音频，音频存放于:{output_audio}')
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  # 不要视频
        "-acodec", "pcm_s16le",  # 无损 wav
        "-ar", "16000",  # ASR 标准采样率
        "-ac", "1",  # 单声道（识别更稳）
        output_audio
    ]

    # 执行ffmpeg
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('提取音频完成')
    return config_dic

if __name__ == '__main__':
    config_dic = {
        'video_path': "E:\\Project\\video2xhsnote\\exam_video\\example.mp4"
    }
    result = extract_audio(config_dic)
    print(result)