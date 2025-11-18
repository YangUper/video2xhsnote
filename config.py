# 输出的音频路径
audio_dir = './audio'
# 小红书笔记输出路径
output_dir = './notes'
# 视觉理解prompt
vision_prompt = """
    请分析并描述这张图片（来自视频的一帧）。请从以下维度进行说明：
    1. 画面中的主要主体与物体  
    2. 场景环境与背景信息  
    3. 人物或物体的动作、姿势或交互  
    4. 氛围、光线、色调  
    5. 可以推断的场景语义或可能发生的事件  
    请尽量客观、简洁、结构化地描述画面。
"""
# 视频抽帧间隔，数值越小，抽帧数量越多，处理时间越长
interval = 500
# 视觉理解模型（注意名称与ollama中一致，使用前先从ollama拉取模型）
vision_model = 'qwen3-vl:2b'
# 笔记生成模型（注意名称与ollama中一致，使用前先从ollama拉取模型）
generate_model = 'deepseek-r1:8b'
# 有显卡则为"cuda"，否则为"cpu"，mac用户为"mps"
device = 'cuda'
