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

PROMO_OPENING_A = """京都にいるよ〜って方🙋‍♀️
祇園でドライヘッドスパいかがですか💆✨
70分コース3,980円🌿"""

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
    for attempt in range(3):
        try:
            r = requests.get(GITHUB_API_IMAGES, timeout=10)
            print("IMAGE_API_STATUS:" + str(r.status_code))
            files = r.json()
            if isinstance(files, list):
                images = [f["name"] for f in files if f["name"].lower().endswith((".jpg",".jpeg",".png"))]
                print("IMAGE_COUNT:" + str(len(images)))
                if images:
                    chosen = random.choice(images)
                    url = GITHUB_RAW_BASE + chosen.replace(" ", "%20")
                    print("IMAGE_CHOSEN:" + chosen[:40])
                    return url
            else:
                print("IMAGE_API_ERROR:" + str(files)[:100])
        except Exception as e:
            print("IMAGE_EXCEPTION:" + str(e)[:80])
            time.sleep(2)
    print("GET_IMAGE_FAILED")
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
・絵文字は0〜1個まで、使いすぎない
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
・絵文字は0〜1個まで、使いすぎない
・「。」「、」は使わない
・時間に関する表現は一切使わない
・「完全個室」「ヘッドセラピー」は使わない
・ハッシュタグなし
・追加する一言だけ出力（書き出しは繰り返さない）"""
        return PROMO_OPENING_B + "\n" + call_claude(prompt_text)

    else:
        season = get_season()
        prompt_text = f"""京都祇園にあるドライヘッドスパ店「ヘッドミント」のセラピストとして、Threadsに投稿する文を1つ書いて。店には複数のセラピストがいて、毎回違うスタッフが投稿している設定。

テーマ:「{theme}」

【投稿スタイル】毎回以下のどれかで書く（バラバラに）
・セラピストがお客さんに話しかける（「〜な人いますか？」「よかったら来てください」など）
・お客さんの気持ちに共感する（「〜って感じしない？」「わかる人いますか？」など）
・施術や仕事を通じた気づきをさらっと伝える（自慢ではなく自然に）

【ルール】
・80文字以内
・ですます調ベースで書く。ただし堅くならない。若いスタッフがサロンのSNSに書くような、親しみやすくて温かみのある口調（例：「〜な方、多いですよ」「気になる方はぜひ」「〜って感じしませんか？」）
・タメ口は使わない。「いらっしゃいます」「〜される方」など硬い敬語も使わない
・各文の末尾に絵文字を1つつける（😮‍💨🙌😅🫠🤔💆👀💪🥺など）
・🩷💗🌸🫶などネカマ絵文字は使わない
・「？→絵文字」が基本、感情強め時は「絵文字→？」もあり
・「。」「、」は使わない
・時間・季節・情景描写はしない
・方言は無理に入れない。「めっちゃ」「ほんま」「〜やん」程度なら自然に使っていい。それ以外の関西弁は使わない
・「完全個室」「ヘッドセラピー」は使わない
・ハッシュタグなし・文と文の間は改行
・投稿文だけ出力"""

        return call_claude(prompt_text, max_tokens=300)

def create_thread(text, image_url=None):
    url = "https://graph.threads.net/v1.0/" + USER_ID + "/threads"
    params = {"media_type": "IMAGE" if image_url else "TEXT", "text": text, "access_token": ACCESS_TOKEN}
    if image_url:
        params["image_url"] = image_url
    return requests.post(url, params=params, timeout=30).json()

def wait_for_image(creation_id):
    # Threads APIのステータス確認が動作しないため固定待機
    print("IMAGE_WAIT:30s")
    time.sleep(30)
    return True

def publish_thread(creation_id):
    url = "https://graph.threads.net/v1.0/" + USER_ID + "/threads_publish"
    return requests.post(url, params={"creation_id": creation_id, "access_token": ACCESS_TOKEN}, timeout=30).json()

if __name__ == "__main__":
    post_text = generate_post()
    print("GENERATED_OK")
    image_url = get_image_url()
    print("IMAGE_URL:" + ("OK" if image_url else "NONE"))
    used_image = False
    result = create_thread(post_text, image_url)
    if "id" in result:
        container_id = result["id"]
        if image_url:
            # 画像処理完了まで待機
            wait_for_image(container_id)
            used_image = True
        else:
            time.sleep(5)
        pub = publish_thread(container_id)
        if pub.get("id"):
            print("SUCCESS_WITH_IMAGE" if used_image else "SUCCESS_TEXT_ONLY")
        else:
            # publish失敗→テキストのみで再試行
            print("PUBLISH_FAILED_IMG:" + str(pub))
            if image_url:
                result2 = create_thread(post_text, None)
                if "id" in result2:
                    time.sleep(5)
                    pub2 = publish_thread(result2["id"])
                    print("SUCCESS_TEXT_ONLY" if pub2.get("id") else "FAILED:" + str(pub2))
    else:
        # 画像付き作成失敗→テキストのみで再試行
        if image_url:
            result2 = create_thread(post_text, None)
            if "id" in result2:
                time.sleep(5)
                pub2 = publish_thread(result2["id"])
                print("SUCCESS_TEXT_ONLY" if pub2.get("id") else "FAILED:" + str(pub2))
            else:
                print("CREATE_FAILED:" + str(result2))
        else:
            print("CREATE_FAILED:" + str(result))
