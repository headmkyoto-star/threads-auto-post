# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import anthropic
import requests
import os
import random
import time
import datetime

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN", "")
USER_ID = "27185017111098955"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/headmkyoto-star/threads-auto-post/main/images/"
GITHUB_API_IMAGES = "https://api.github.com/repos/headmkyoto-star/threads-auto-post/contents/images"

DAILY_THEMES = [
    "今日の施術中に感じたこと・気づき",
    "お客様が帰り際に言ってくれた言葉",
    "施術前後でお客様の表情が変わる瞬間",
    "最近施術していて気になるお客様の悩みの傾向",
    "ヘッドスパ中にお客様がよく眠ってしまう話",
    "施術中に大切にしていること・こだわり",
    "今日いちばん印象に残ったお客様との会話",
    "リピートしてくれるお客様への感謝気持ち",
    "施術後にお客様がもらした一言が嬉しかった",
    "ドライヘッドスパの施術で気をつけていること",
    "ヘッドスパと睡眠の深い関係",
    "頭皮マッサージが眼精疲労に効く理由",
    "スマホ疲れが頭部にどう影響するか",
    "デスクワーク続きの人に出やすい頭部の張り",
    "首こり・肩こりが実は頭から来ている話",
    "頭皮の血行と肌荒れ・顔色の意外なつながり",
    "自律神経と頭部の緊張の関係",
    "頭の重さと疲れのメカニズム",
    "ドライヘッドスパが寝落ちを引き起こす理由",
    "食事・水分と頭皮コンディションのこと",
    "セラピストとして最近うれしかったこと",
    "この仕事を続けていて良かったと思う瞬間",
    "セラピストになった理由・きっかけ",
    "技術を磨くために最近やっていること",
    "先輩セラピストから学んだ大切なこと",
    "自分自身がセラピーを受けて気づいたこと",
    "施術中に無心になれる感覚について",
    "お客様の信頼を感じたエピソード",
    "セラピストとして壁にぶつかった話と乗り越え方",
    "今日のサロンの雰囲気・スタッフの様子",
    "今日の京都の天気や空の様子",
    "京都の季節の移り変わりを感じた瞬間",
    "祇園エリアで最近気になること・お気に入りの場所",
    "京都の朝の空気感・静かな時間のこと",
    "今日食べたランチや立ち寄ったお店",
    "季節の変わり目に感じるカラダの変化",
    "最近のマイブーム・ハマっているもの",
    "休日の過ごし方・リフレッシュ法",
    "今日の気分や感情を素直につぶやく",
    "朝の準備・ルーティンで大事にしていること",
    "サロンで聴いているBGMや香りのこと",
    "サロンの内装や照明へのこだわり",
    "お客様を迎えるときに意識していること",
    "施術前のカウンセリングで大切にしていること",
    "サロンの空気感・居心地を作るための工夫",
    "今日のちょっとした嬉しい出来事",
    "スタッフとの他愛ない会話が癒しだった話",
    "お客様から教えてもらったお得情報や話題",
    "今日感じたこれいいなという瞬間",
    "ふと立ち止まって感じた感謝のきもち",
]

PROMO_THEMES = [
    "首や肩のこりが気になる方への提案",
    "睡眠が浅い・眠れない方への提案",
    "眼精疲労・頭痛が続く方への提案",
    "70分3980円のお得さを伝える",
    "初めての方への安心感を伝える",
]

def get_time_context():
    hour = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).hour
    if 5 <= hour < 10:
        return "朝"
    elif 10 <= hour < 14:
        return "昼"
    elif 14 <= hour < 18:
        return "夕方"
    else:
        return "夜"

def get_image_url():
    try:
        r = requests.get(GITHUB_API_IMAGES, timeout=10)
        files = r.json()
        images = [f["name"] for f in files if f["name"].lower().endswith((".jpg", ".jpeg", ".png"))]
        if images:
            chosen = random.choice(images).replace(" ", "%20")
            return GITHUB_RAW_BASE + chosen
    except Exception as e:
        print("画像取得エラー: " + str(e))
    return None

def generate_post():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    time_context = get_time_context()
    is_promo = random.random() < 0.2
    if is_promo:
        theme = random.choice(PROMO_THEMES)
        prompt = "あなたはドライヘッドスパ専門サロン「head.m.kyoto」のセラピストです。\nThreadsに投稿する文章を1つ作ってください。\n\n今の時間帯：" + time_context + "\n今回のテーマ：「" + theme + "」\n\nルール：\n- 投稿文のみ出力（前置きや説明は不要）\n- 必ず文と文の間で改行する（1文ごとに改行）\n- 各文か段落に絵文字を入れる\n- 70分3980円を自然に含める\n- ハッシュタグは絶対に使わない\n- 150文字以内\n"
    else:
        theme = random.choice(DAILY_THEMES)
        prompt = "あなたはドライヘッドスパ専門サロン「head.m.kyoto」のセラピストです。\nThreadsに投稿する文章を1つ作ってください。\n\n今の時間帯：" + time_context + "\n今回のテーマ：「" + theme + "」\n\nルール：\n- 投稿文のみ出力（前置きや説明は不要）\n- 必ず文と文の間で改行する（1文ごとに改行）\n- 各文か段落に絵文字を入れる\n- 営業っぽくしない・自然な日常感で\n- ハッシュタグは絶対に使わない\n- 150文字以内\n"

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

def create_thread(text, image_url=None):
    url = "https://graph.threads.net/v1.0/" + USER_ID + "/threads"
    if image_url:
        params = {"media_type": "IMAGE", "image_url": image_url, "text": text, "access_token": ACCESS_TOKEN}
    else:
        params = {"media_type": "TEXT", "text": text, "access_token": ACCESS_TOKEN}
    response = requests.post(url, params=params, timeout=30)
    return response.json()

def publish_thread(creation_id):
    url = "https://graph.threads.net/v1.0/" + USER_ID + "/threads_publish"
    params = {"creation_id": creation_id, "access_token": ACCESS_TOKEN}
    response = requests.post(url, params=params, timeout=30)
    return response.json()

if __name__ == "__main__":
    print("投稿生成中...")
    post_text = generate_post()
    print("生成完了")
    print("---")
    print(post_text)
    print("---")

    image_url = get_image_url()
    if image_url:
        print("画像URL取得: OK")

    result = create_thread(post_text, image_url)
    print("スレッド作成結果: " + str(result))

    if "id" in result:
        print("30秒待機中...")
        time.sleep(30)
        publish_result = publish_thread(result["id"])
        print("投稿結果: " + str(publish_result))
        if publish_result.get("id"):
            print("SUCCESS: 投稿完了")
        else:
            print("FAILED: 投稿失敗")
    else:
        print("ERROR: スレッド作成失敗")
        if image_url:
            print("画像なしで再試行中...")
            result2 = create_thread(post_text, None)
            if "id" in result2:
                time.sleep(30)
                r2 = publish_thread(result2["id"])
                if r2.get("id"):
                    print("SUCCESS: テキストのみで投稿完了")
                else:
                    print("FAILED: 再試行も失敗: " + str(r2))
