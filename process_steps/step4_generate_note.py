from celery import shared_task
import ollama
import os

def save_note_as_md(config_dic):
    print(f'开始保存 {config_dic["video_path"]} 的笔记')
    output_dir = config_dic.get('output_dir')
    os.makedirs(output_dir, exist_ok=True)

    # 生成文件名：使用视频名
    video_name = os.path.basename(config_dic['video_path']).rsplit('.', 1)[0]
    md_path = os.path.join(output_dir, f"{video_name}.md")

    # 写入内容
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(config_dic['note'])

    print(f"已保存笔记到 {md_path}")

@shared_task
def generate_note(config_dic):
    print(f'开始生成 {config_dic["video_path"]} 的小红书文案')
    text = config_dic.get('text')
    vision_desc = config_dic.get('vision_desc')
    vision_desc_processed = ['第' + str(i['frame_index']) + '帧画面:' + i['description'] for i in vision_desc]
    vision_desc_final = '\n'.join(vision_desc_processed)
    # print(vision_desc_final)

    prompt = f"""
    你是一名专业的小红书文案创作者，我现在给你一个视频中抽取音频的文字信息以及对视频中按时间顺序抽帧画面的描述，你需要根据我给你的音频文字和对画面的描述进行创作，撰写出合适的小红书笔记。

    以下是视频的视觉理解内容（多帧模型描述）：
    {vision_desc_final}

    以下是音频识别出的事件内容：
    {text}

    请你将以上内容融合，给我一个标题，并且生成一篇符合音频和视频内容的小红书笔记。

    要求：
    1. 使用口语化、自然、有代入感的风格。
    2. 不要逐帧描述，要融合成一个完整事件。
    3. 文风治愈、有画面感、有情绪。
    4. 适当加点主观感受，让内容更生动。
    """

    res = ollama.chat(
        model='deepseek-r1:8b',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    note = res['message']['content']
    config_dic['note'] = note
    # print(note)
    print(f'完成 {config_dic["video_path"]} 的小红书文案')
    save_note_as_md(config_dic)
    return config_dic



if __name__ == '__main__':
    config_dic = {
        'video_path': 'E:\\Project\\video2xhsnote\\exam_video\\example.mp4',
        'audio_path': 'E:\\Project\\video2xhsnote\\audio\\example.wav',
        'text': '好的 比赛开始。苏秉天卸转业现在处在极投并技的状态。处在领先的还是苏秉天。在30米过后他有着非常明显的领先优势。最后80米过后。苏秉天放掉了这一枪。顺利的晋级决赛。苏秉天成绩10秒05。最后20米放成这样还能跑到10秒05。而今年苏秉天的状态极其的出色。如果全力压线的话。这一枪很有可能跑进10秒。',
        'vision_prompt': '描述这张图片。',
        'vision_desc': [{'frame_index': 0,
                         'description': '这张图片展示了**2021年西安安全运会男子100米比赛**中的一个场景，画面聚焦于田径赛场上的运动员苏炳添。  \n\n### 主体细节：  \n- **场景与环境**：背景是红色塑胶跑道，带有白色分道线，典型的田径赛场环境。  \n- **运动员形象**：  \n  - 画面中心是**苏炳添**，他身穿**红色无袖运动背心**，背心正面印有“广东”字样（左侧）和耐克标志（右侧），胸前佩戴的赛事号码布上清晰标注了“2021西安安全运会男100米比赛”等信息。  \n  - 号码布下方的文字说明点明了比赛背景与成绩预期：“苏炳添半决赛跑出10秒06晋级决赛”，以及黄色字幕“这一枪很有可能跑进10秒”，直观传达了比赛的竞技状态和成绩目标。  \n- **动态姿态**：苏炳添站在跑道上，双臂自然张开，呈现出比赛中的姿态；画面右侧还可见另一位运动员的部分身体（穿着蓝色运动服，手臂向前伸出，疑似在示意或庆祝）。  \n\n### 画面信息与风格：  \n- 图片采用动态场景拍摄，突出竞技体育的紧张感与专业性。  \n- 文字信息（如赛事名称、成绩预测）以中文字幕形式叠加在画面上，清晰传递了赛事背景与关键数据，增强了画面的叙事性和信息传递效率。  \n\n整体而言，这张图片生动呈现了田径赛场上的关键赛事瞬间，结合运动员的服饰、场景与文字说明，既展现了体育赛事的专业性，也凸显了苏炳添在100米项目中“跑进10秒”的竞技目标与突破潜力。'},
                        {'frame_index': 1,
                         'description': '这张图片呈现的是**2021西安安全运动会男子100米比赛**的现场场景，聚焦于运动员苏炳添在半决赛阶段的表现。  \n\n### 场景与元素  \n- **场地**：画面主体是标准田径场跑道，红褐色跑道清晰可见；背景是大片绿色草坪，远处有色彩渐变的广告牌（紫蓝配色，带有文字信息）。  \n- **运动员**：画面中有多名运动员在跑道上奔跑，主体是**苏炳添**（身穿红色运动背心、黑色短裤，号码布上显示数字“9”），他处于画面右侧，动作专注有力。左侧还有其他运动员，身着不同颜色运动服（如橙色、蓝色），形成梯队式跑步状态。  \n- **文字信息**：图片叠加了关键文字说明——  \n  - 上方文字：“2021西安安全运动会男子100米比赛 苏炳添半决赛跑出10秒06晋级决赛”  \n  - 下方文字：“苏炳添成绩10秒05（修正后10秒06）”  \n\n### 画面细节与氛围  \n- 画面充满动感，运动员奔跑的姿态展现出力量与速度感，背景广告牌与跑道的细节（如跑道纹理、草坪质感）清晰可辨。  \n- 文字标注明确点出赛事名称、比赛阶段及成绩，直观传递了“苏炳添在100米半决赛中以10秒05（修正后10秒06）晋级决赛”的核心信息，强化了图片的赛事纪实属性。  \n\n整体而言，这张图片以田径赛场为背景，通过运动员动态与文字信息的结合，生动展现了2021年西安安全运动会男子100米项目中苏炳添的竞技表现与赛事成绩。'}]
    }
    generate_note(config_dic)