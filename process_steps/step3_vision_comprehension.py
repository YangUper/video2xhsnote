from celery import shared_task
import ollama
import base64
import cv2


def frame2base64(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')


def extract_frames(video_path, interval=500):
    cap = cv2.VideoCapture(video_path)
    count = 0
    frames_b64 = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval == 0:
            frames_b64.append(frame2base64(frame))
        count += 1
    cap.release()
    return frames_b64


def vision_inference(image_b64, vision_prompt):
    res = ollama.chat(
        model="qwen3-vl:2b",
        messages=[
            {
                "role": "user",
                "content": vision_prompt,
                "images": [image_b64]
            }
        ]
    )
    return res['message']['content']


@shared_task
def vision_comprehension(config_dic):
    video_path = config_dic.get('video_path')
    vision_prompt = config_dic.get('vision_prompt')

    # 抽帧
    frames_b64 = extract_frames(video_path)

    results = []
    # 每一帧送入模型
    for idx, img_b64 in enumerate(frames_b64):
        print(f"Processing frame {idx + 1}/{len(frames_b64)}")
        desc = vision_inference(img_b64, vision_prompt)
        results.append({
            'frame_index': idx,
            'description': desc
        })
        print(desc)
    config_dic['vision_desc'] = results
    # print(results)
    return config_dic


if __name__ == '__main__':
    config_dic = {
        'video_path': 'E:\\Project\\video2xhsnote\\exam_video\\example.mp4',
        'audio_path': 'E:\\Project\\video2xhsnote\\audio\\example.wav',
        'text': '好的 比赛开始。苏秉天卸转业现在处在极投并技的状态。处在领先的还是苏秉天。在30米过后他有着非常明显的领先优势。最后80米过后。苏秉天放掉了这一枪。顺利的晋级决赛。苏秉天成绩10秒05。最后20米放成这样还能跑到10秒05。而今年苏秉天的状态极其的出色。如果全力压线的话。这一枪很有可能跑进10秒。',
        'vision_prompt': '描述这张图片。'
    }
    result = vision_comprehension(config_dic)
    print(result)