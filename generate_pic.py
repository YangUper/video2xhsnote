from playwright.sync_api import sync_playwright
from pathlib import Path
import time

url = 'https://chat.qwen.ai/'
storage_file = 'storage.json'
img_dir = Path('./image')

note_path = input('请选择一篇笔记以生成对应图片（笔记路径）：').strip()
while not Path(note_path).exists():
    note_path = input('您输入的笔记路径有误，请重新输入：')
file_name = Path(note_path).stem
img_dir = img_dir / file_name
img_dir.mkdir(parents=True, exist_ok=True)

with open(note_path, 'r', encoding='utf-8') as f:
    note_content = f.read().split("```")[1].split('\n', 1)[-1]
# print(note_content)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    if Path(storage_file).exists():
        print('已登录，无需输入用户名和密码')
        context = browser.new_context(storage_state=storage_file)
        page = context.new_page()
        page.goto(url, wait_until='networkidle')

        login_btn = page.get_by_role(role='button', name='Log in').click()
        login_with_github_btn = page.get_by_role(role='button', name=' 继续使用 Github 登录')
        login_with_github_btn.click()
    else:
        print('第一次登录，需要提供用户名和密码')
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until='networkidle')

        login_btn = page.get_by_role(role='button', name='Log in')

        # print(login_btn.is_visible())
        if login_btn.count() > 0:
            login_btn.click()
            login_with_github_btn = page.get_by_role(role='button', name=' 继续使用 Github 登录')
            login_with_github_btn.click()
            username_or_email_input = page.get_by_label('Username or email address')
            password_input = page.get_by_label('Password')

            username_or_email = input('现在需要登录qwen官网，需要您的github用户名或者绑定的邮箱：').strip()
            password = input('请继续输入您的github密码：').strip()

            username_or_email_input.fill(username_or_email)
            password_input.fill(password)
            signin_btn = page.get_by_role(role='button', name='Sign in').first
            signin_btn.click()

            # 保存登录状态到文件
            context.storage_state(path=storage_file)

    pic_generate_btn = page.get_by_text('图像生成')
    pic_generate_btn.click()

    one_and_one_btn = page.get_by_text('1:1')
    one_and_one_btn.click()
    nine_and_sixteen_btn = page.get_by_text('9:16')
    nine_and_sixteen_btn.click()

    desc_input = page.get_by_placeholder('描述你想要生成的图像。')

    prompt = f"""
    根据以下小红书笔记内容生成对应场景的真实感图片：
    【笔记内容】
    {note_content}

    【图片要求】
    - 风格：小红书常见的真实生活感、干净自然、治愈系光影
    - 构图：主体现明显，画面简洁不杂乱，留白适当
    - 画面氛围：柔和自然光、温柔色调、轻微胶片质感
    - 背景：真实、不过度虚化，不使用 AI 常见的奇怪结构
    - 真实生活场景，不要夸张，不要奇幻，不要动漫风，不要抽象风
    - 元素细节符合现实逻辑（不要多余手指、不要扭曲、不出现乱码文字）
    - 分辨率：高清 4K
    """

    send_btn = page.locator('#send-message-button')

    desc_input.fill(prompt)

    while True:
        with page.expect_request('https://cdn.qwenlm.ai/output/**') as img:
            send_btn.click()
        img_data = img.value.response().body()
        timestamp = str(int(time.time()))
        img_path = img_dir / (timestamp + '.jpg')
        with open(img_path, 'wb') as f:
            f.write(img_data)
        print(f'图片已经存放于{img_path}，请您查看。')
        add_desc = input(f"如果对于{img_path}还需要进行更改，请进一步给我您的需求，没有则输入“ok”退出程序：").strip()
        if add_desc == 'ok':
            break
        else:
            desc_input.fill(add_desc)
            continue

    browser.close()