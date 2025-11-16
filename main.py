import os
import time
from tasks import process_video_task

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

    tasks_list = [process_video_task.delay(f) for f in file_paths]
    print('所有任务已提交')

    # 轮询每个任务是否完成
    unfinished_tasks = tasks_list.copy()
    while unfinished_tasks:
        for task in unfinished_tasks[:]:
            if task.ready():
                result = task.get()
                print(f'任务{task.id}已经完成，结果：{result}')
                unfinished_tasks.remove(task)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
