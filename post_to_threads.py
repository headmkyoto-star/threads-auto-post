import anthropic
import requests
import os

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN", "")
USER_ID = "27185017111098955"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def generate_post():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": """あなたは京都のドライヘッドスパ専門サロン「head.m.kyoto」のSNS担当者です。
Threadsに投稿する内容を1つ作成してください。

サロンの特徴：
- 京都にあるドライヘッドスパ専門サロン
- ドライヘッドスパ、フェイシャル、ボディトリートメントなど
- リラックスできる和の空間を提供

投稿スタイル：
- 絵文字を使う（🌿✨💆‍♀️🍃🌸など）
- 短い改行で読みやすく
- お客様への気遣い、サロンの雰囲気、施術の魅力を伝える
- 季節感も取り入れる
- 100〜200文字程度

投稿内容のみ返してください。"""
            }
        ]
    )
    return message.content[0].text

def create_thread(text):
    url = f"https://graph.threads.net/v1.0/{USER_ID}/threads"
    params = {
        "media_type": "TEXT",
        "text": text,
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    return response.json()

def publish_thread(creation_id):
    url = f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish"
    params = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }
    response = requests.post(url, params=params)
    return response.json()

if __name__ == "__main__":
    post_text = generate_post()
    print(f"生成された投稿:\n{post_text}")

    result = create_thread(post_text)
    print(f"スレッド作成: {result}")

    if "id" in result:
        publish_result = publish_thread(result["id"])
        print(f"投稿完了: {publish_result}")
    else:
        print("エラー: スレッド作成失敗")
