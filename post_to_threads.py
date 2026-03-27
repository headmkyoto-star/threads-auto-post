import anthropic
import requests
import os
import random

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN", "")
USER_ID = "27185017111098955"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def generate_post():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # 10回に2回は営業・告知、8回は日常・癒し系
    post_type = "promo" if random.random() < 0.2 else "daily"
    
    if post_type == "promo":
        instruction = """あなたは京都のドライヘッドスパ専門サロン「head.m.kyoto」のSNS担当者です。
サロンの予約・来店を促す投稿を1つ作成してください。

サロンの特徴：
- 京都にあるドライヘッドスパ専門サロン
- 水を使わないドライヘッドスパで服を着たまま受けられる
- 頭・首・肩のコリをほぐす至福の時間

投稿スタイル：
- 絵文字を使う（🌿✨💆‍♀️🍃🌸など）
- 短い改行で読みやすく
- 予約や来店を自然に促す
- ハッシュタグを末尾に（#ドライヘッドスパ #京都 #headmkyoto）
- 100〜200文字程度

投稿内容のみ返してください。"""
    else:
        instruction = """あなたは京都のドライヘッドスパ専門サロン「head.m.kyoto」のSNS担当者です。
サロンの雰囲気や日常、お客様の声などを伝える温かい投稿を1つ作成してください。

サロンの特徴：
- 京都にあるドライヘッドスパ専門サロン
- 癒しと心地よさを大切にした空間

投稿スタイル：
- 絵文字を使う（🌿✨💆‍♀️🍃🌸など）
- 短い改行で読みやすく
- 営業感を出さず、日常・癒し・気づきを伝える
- お客様の笑顔、季節感、サロンのひとコマなど
- 100〜200文字程度

投稿内容のみ返してください。"""
    
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": instruction}]
    )
    return message.content[0].text

def create_thread(text):
    url = f"https://graph.threads.net/v1.0/{USER_ID}/threads"
    params = {"media_type": "TEXT", "text": text, "access_token": ACCESS_TOKEN}
    response = requests.post(url, params=params)
    return response.json()

def publish_thread(creation_id):
    url = f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish"
    params = {"creation_id": creation_id, "access_token": ACCESS_TOKEN}
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
