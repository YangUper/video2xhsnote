from celery import shared_task
import whisper

download_dir = "E:/Project/video2xhsnote/whisper_models"
audio2text_model = whisper.load_model('small', device='cuda', download_root=download_dir)

@shared_task
def audio2text(config_dic):
    audio_path = config_dic.get('audio_path')
    print(f'开始识别音频：{audio_path}')
    result = audio2text_model.transcribe(audio_path, language='zh')
    # print(result)
    segments = result.get('segments')
    # print(segments)
    text = ""
    for segment in segments:
        text += segment['text'] + '。'

    config_dic['text'] = text
    print('识别音频完成')
    return config_dic


if __name__ == '__main__':
    config_dic = {
        'video_path': 'E:\\Project\\video2xhsnote\\exam_video\\example.mp4',
        'audio_path': 'E:\\Project\\video2xhsnote\\audio\\example.wav'
    }
    result = audio2text(config_dic)
    print(result)