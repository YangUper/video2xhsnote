import os
from celery import group, chain
from process_steps import extract_audio, audio2text, vision_comprehension, generate_note

from celery import Celery

app = Celery(
    'video_tasks',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/1',
    result_expires=3600
)

def main():
    file_paths = []

    file_path = input('请输入需要处理视频的完整路径（结束请输入"ok"）:')

    while file_path.strip() != "ok":
        if not os.path.exists(file_path):
            print('视频文件路径错误，视频不存在!')
            file_path = input('请输入需要处理视频的路径（结束请输入"ok"）:')
            continue

        file_paths.append(file_path)
        file_path = input('请输入需要处理视频的完整路径（结束请输入"ok"）:')

    # 提交任务组并等待结果
    tasks_group = group(
        chain(
            extract_audio.s({'video_path': f, 'vision_prompt': '描述这张图片', 'output_dir': './notes'}),
            audio2text.s(),
            vision_comprehension.s(),
            generate_note.s()
        ) for f in file_paths
    )

    result = tasks_group.apply_async()  # 使用apply_async提交任务组
    print('所有任务已提交')

    # 等待所有任务完成
    result.join()
    print('所有任务已完成')


if __name__ == '__main__':
    main()
