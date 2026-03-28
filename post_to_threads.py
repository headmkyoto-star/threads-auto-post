import requests
import os
import random
import time
import datetime
import json

ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN", "")
USER_ID = "27185017111098955"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/headmkyoto-star/threads-auto-post/main/images/"
GITHUB_API_IMAGES = "https://api.github.com/repos/headmkyoto-star/threads-auto-post/contents/images"

DAILY_THEMES = [
    "今日の施術中に感じたこと・気づき","お客様が帰り際に言ってくれた言葉","施術前後でお客様の表情が変わる瞬間",
    "最近施術していて気になるお客様の悩みの傾向","ヘッドスパ中にお客様がよく眠ってしまう話",
    "施術中に大切にしていること・こだわり","今日いちばん印象に残ったお客様との会話",
    "リピートしてくれるお客様への感謝気持ち","施術後にお客様がもらした一言が嬉しかった",
    "ドライヘッドスパの施術で気をつけていること","ヘッドスパと睡眠の深い関係",
    "頭皮マッサージが眼精疲労に効く理由","スマホ疲れが頭部にどう影響するか",
    "デスクワーク続きの人に出やすい頭部の張り","首こり・肩こりが実は頭から来ている話",
    "頭皮の血行と肌荒れ・顔色の意外なつながり","自律神経と頭部の緊張の関係",
    "頭の重さと疲れのメカニズム","ドライヘッドスパが寝落ちを引き起こす理由",
    "食事・水分と頭皮コンディションのこと","セラピストとして最近うれしかったこと",
    "この仕事を続けていて良かったと思う瞬間","セラピストになった理由・きっかけ",
    "技術を磨くために最近やっていること","先輩セラピストから学んだ大切なこと",
    "自分自身がセラピーを受けて気づいたこと","施術中に無心になれる感覚について",
    "お客様の信頼を感じたエピソード","セラピストとして壁にぶつかった話と乗り越え方",
    "今日のサロンの雰囲気・スタッフの様子","今日の京都の天気や空の様子",
    "京都の季節の移り変わりを感じた瞬間","祇園エリアで最近気になること・お気に入りの場所",
    "京都の朝の空気感・静かな時間のこと","今日食べたランチや立ち寄ったお店",
    "季節の変わり目に感じるカラダの変化","最近のマイブーム・ハマっているもの",
    "休日の過ごし方・リフレッシュ法","今日の気分や感情を素直につぶやく",
    "朝の準備・ルーティンで大事にしていること","サロンで聴いているBGMや香りのこと",
    "サロンの内装や照明へのこだわり","お客様を迎えるときに意識していること",
    "施術前のカウンセリングで大切にしていること","サロンの空気感・居心地を作るための工夫",
    "今日のちょっとした嬉しい出来事","スタッフとの他愛ない会話が癒しだった話",
    "お客様から教えてもらったお得情報や話題","ふと立ち止まって感じた感謝のきもち",
]
PROMO_THEMES = [
    "首や肩のこりが気になる方への提案","睡眠が浅い・眠れない方への提案",
    "眼精疲労・頭痛が続く方への提案","70分3980円のお得さを伝える","初めての方への安心感を伝える",
]

def get_time_context():
    hour = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).hour
    if 5 <= hour < 10: return "asa"
    elif 10 <= hour < 14: return "hiru"
    elif 14 <= hour < 18: return "yugata"
    else: return "yoru"

def get_image_url():
    try:
        r = requests.get(GITHUB_API_IMAGES, timeout=10)
        files = r.json()
        images = [f["name"] for f in files if f["name"].lower().endswith((".jpg",".jpeg",".png"))]
        if images:
            return GITHUB_RAW_BASE + random.choice(images).replace(" ", "%20")
    except:
        pass
    return None

def generate_post():
    key_preview = ANTHROPIC_API_KEY[:20] if ANTHROPIC_API_KEY else "EMPTY"
    print("API_KEY_PREVIEW:" + key_preview)

    is_promo = random.random() < 0.2
    theme = random.choice(PROMO_THEMES if is_promo else DAILY_THEMES)
    time_ctx = get_time_context()

    if is_promo:
        prompt_text = "ヘッドミント京都祇園店のセラピストとしてThreadsに投稿する文を1つ書いてください。テーマ:「" + theme + "」時間帯:" + time_ctx + " ルール:投稿文のみ出力。文ごとに改行。各文に絵文字。ハッシュタグなし。150文字以内。価格は必ず「70分3,980円」と明記すること。「完全個室」とは絶対に書かないこと。"
    else:
        prompt_text = "ヘッドミント京都祇園店のセラピストとしてThreadsに投稿する文を1つ書いてください。テーマ:「" + theme + "」時間帯:" + time_ctx + " ルール:投稿文のみ出力。文ごとに改行。各文に絵文字。ハッシュタグなし。150文字以内。「完全個室」とは絶対に書かないこと。"

    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt_text}]
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        data=body,
        timeout=30
    )
    print("API_STATUS:" + str(r.status_code))
    result = r.json()
    if "error" in result:
        raise Exception("API_ERROR:" + str(result["error"]))
    return result["content"][0]["text"].strip()

def create_thread(text, image_url=None):
    url = "https://graph.threads.net/v1.0/" + USER_ID + "/threads"
    params = {"media_type": "IMAGE" if image_url else "TEXT", "text": text, "access_token": ACCESS_TOKEN}
    if image_url:
        params["image_url"] = image_url
    return requests.post(url, params=params, timeout=30).json()

def publish_thread(creation_id):
    url = "https://graph.threads.net/v1.0/" + USER_ID + "/threads_publish"
    return requests.post(url, params={"creation_id": creation_id, "access_token": ACCESS_TOKEN}, timeout=30).json()

if __name__ == "__main__":
    post_text = generate_post()
    print("GENERATED_OK")
    image_url = get_image_url()
    result = create_thread(post_text, image_url)
    if "id" in result:
        time.sleep(30)
        pub = publish_thread(result["id"])
        print("SUCCESS" if pub.get("id") else "PUBLISH_FAILED:" + str(pub))
    else:
        result2 = create_thread(post_text, None)
        if "id" in result2:
            time.sleep(30)
            pub2 = publish_thread(result2["id"])
            print("SUCCESS" if pub2.get("id") else "FAILED:" + str(pub2))
        else:
            print("CREATE_FAILED:" + str(result2))
