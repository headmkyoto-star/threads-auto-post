import anthropic
import requests
import os
import random
import time

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN", "")
USER_ID = "27185017111098955"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/headmkyoto-star/threads-auto-post/main/images/"
GITHUB_API_IMAGES = "https://api.github.com/repos/headmkyoto-star/threads-auto-post/contents/images"

def get_image_url():
    try:
        r = requests.get(GITHUB_API_IMAGES)
        files = r.json()
        images = [f["name"] for f in files if f["name"].lower().endswith((".jpg", ".jpeg", ".png"))]
        if images:
            selected = random.choice(images)
            return GITHUB_RAW_BASE + selected.replace(" ", "_")
    except:
        pass
    return None

def generate_post():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    post_type = "promo" if random.random() < 0.2 else "daily"

    if post_type == "promo":
        prompt = """あなたはドライヘッドスパ専門サロンのセラピストです。
Threadsに投稿する短い営業投稿を1つ作成してください。
条件：ドライヘッドスパ専門、70分3,980円、ハッシュタグなし、150文字以内、自然な日本語、絵文字OK
投稿文のみ出力してください。"""
    else:
        prompt = """あなたはドライヘッドスパ専門サロンのセラピストです。
Threadsに投稿する日常・日記系の投稿を1つ作成してください。
条件：セラピストの日常や気づき、ハッシュタグなし、150文字以内、自然な日本語、絵文字OK、営業色なし
投稿文のみ出力してください。"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

def post_to_threads(text, image_url=None):
    if image_url:
        container_data = {
            "media_type": "IMAGE",
            "image_url": image_url,
            "text": text,
            "access_token": ACCESS_TOKEN
        }
        r = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads", params=container_data)
        if r.status_code != 200:
            print(f"画像エラー、テキストのみで投稿: {r.text}")
            return post_to_threads(text, None)
        creation_id = r.json().get("id")
        time.sleep(30)
    else:
        container_data = {
            "media_type": "TEXT",
            "text": text,
            "access_token": ACCESS_TOKEN
        }
        r = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads", params=container_data)
        creation_id = r.json().get("id")
        time.sleep(30)

    publish_data = {"creation_id": creation_id, "access_token": ACCESS_TOKEN}
    r = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish", params=publish_data)
    return r

post_text = generate_post()
print(f"生成された投稿:\n{post_text}\n")
image_url = get_image_url()
if image_url:
    print(f"使用する画像: {image_url}\n")
result = post_to_threads(post_text, image_url)
print(f"投稿結果: {result.status_code}")
if result.status_code == 200:
    print("✅ 投稿成功！")
else:
    print(f"❌ エラー: {result.text}")
