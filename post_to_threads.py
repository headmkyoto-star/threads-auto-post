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

PROMO_OPENING_A = """京都にいるよ〜って方🙋\u200d♀️
祇園でドライヘッドスパいかがですか💆\u200d♀️💗
70分コース3,980円🫶🌿"""

PROMO_OPENING_B = """京都祇園でドライヘッドスパ受けたい方いますか☺️？
70分3,980円🌿"""

def get_season():
    month = datetime.date.today().month
    if month in [3, 4, 5]:
        return "春"
    elif month in [6, 7, 8]:
        return "夏"
    elif month in [9, 10, 11]:
        return "秋"
    else:
        return "冬"

def get_image_url():
    for _ in range(3):
        try:
            r = requests.get(GITHUB_API_IMAGES, timeout=10)
            files = r.json()
            images = [f["name"] for f in files if f["name"].lower().endswith((".jpg",".jpeg",".png"))]
            if images:
                return GITHUB_RAW_BASE + random.choice(images).replace(" ", "%20")
        except:
            time.sleep(2)
    return None

def generate_post():
    key_preview = ANTHROPIC_API_KEY[:20] if ANTHROPIC_API_KEY else "EMPTY"
    print("API_KEY_PREVIEW:" + key_preview)

    jst = datetime.timezone(datetime.timedelta(hours=9))
    hour = datetime.datetime.now(jst).hour
    theme = random.choice(DAILY_THEMES)

    def call_claude(prompt, max_tokens=100):
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        return resp.json()["content"][0]["text"].strip()

    if hour == 9:
        prompt_text = """ヘッドミント京都祇園店のセラピストとして、以下の投稿の続きに追加する一言を書いてください。

【投稿の書き出し（固定）】
京都にいるよ〜って方🙋‍♀️✨
祇園でドライヘッドスパいかがですか💆‍♀️💗
70分コース3,980円🫶🌿

【追加する一言のルール】
・1文だけ（短く！）
・来たくなる・コメントしたくなる問いかけか、背中を押す一言
・絵文字は🩷🫶🥹🌸✨🫧☺️💗🤍🫰など可愛い系のみ（0〜1個）
・「。」「、」は使わない
・時間に関する表現は一切使わない
・「完全個室」「ヘッドセラピー」は使わない
・ハッシュタグなし
・追加する一言だけ出力（書き出しは繰り返さない）"""
        return PROMO_OPENING_A + "\n" + call_claude(prompt_text)

    elif hour == 17:
        prompt_text = """ヘッドミント京都祇園店のセラピストとして、以下の投稿の続きに追加する一言を書いてください。

【投稿の書き出し（固定）】
京都祇園でドライヘッドスパ受けたい方いますか☺️？
70分3,980円🌿

【追加する一言のルール】
・1文だけ（短く！）
・来たくなる・コメントしたくなる問いかけか、背中を押す一言
・絵文字は🩷🫶🥹🌸✨🫧☺️💗🤍🫰など可愛い系のみ（0〜1個）
・「。」「、」は使わない
・時間に関する表現は一切使わない
・「完全個室」「ヘッドセラピー」は使わない
・ハッシュタグなし
・追加する一言だけ出力（書き出しは繰り返さない）"""
        return PROMO_OPENING_B + "\n" + call_claude(prompt_text)

    else:
        season = get_season()
        prompt_text = f"""ヘッドミント京都祇園店で働く20代前半のセラピストとして、Threadsに投稿する短い文を書いてください。

テーマ:「{theme}」

【絶対に守るルール】
・全体で80文字以内（短く！長くしない）
・堅苦しくない 日常会話っぽい軽いノリで書く
・真面目すぎない ちょっとゆるくてOK
・「わかる～」「それな！」って思わせる共感か、くすっと笑える内容にする
・最後はコメントしたくなる問いかけで終わる
・絵文字は🩷🫶🥹🌸✨🫧☺️💗🤍🫰など可愛い系のみ（2〜3個）
・「。」「、」は使わない
・朝/昼/夕/夜/何時など時間に関する表現は一切使わない
・季節に関する表現は基本的に使わない。どうしても使う場合のみ現在の季節「{season}」に合わせる
・「完全個室」「ヘッドセラピー」は使わない
・ハッシュタグなし
・文と文の間は改行する（1文ごとに改行）
・投稿文だけ出力"""

        return call_claude(prompt_text, max_tokens=300)

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
    elif image_url:
        # 画像付きが失敗→もう1回リトライ
        time.sleep(5)
        result2 = create_thread(post_text, image_url)
        if "id" in result2:
            time.sleep(30)
            pub2 = publish_thread(result2["id"])
            print("SUCCESS" if pub2.get("id") else "PUBLISH_FAILED2:" + str(pub2))
        else:
            # それでも失敗→テキストのみ
            result3 = create_thread(post_text, None)
            if "id" in result3:
                time.sleep(30)
                pub3 = publish_thread(result3["id"])
                print("SUCCESS_TEXT_ONLY" if pub3.get("id") else "FAILED:" + str(pub3))
            else:
                print("CREATE_FAILED:" + str(result3))
    else:
        print("CREATE_FAILED_NO_IMAGE:" + str(result))
