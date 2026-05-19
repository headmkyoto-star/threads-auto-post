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
GITHUB_API_VIDEOS = "https://api.github.com/repos/headmkyoto-star/threads-auto-post/contents/videos"
GITHUB_RAW_VIDEOS = "https://raw.githubusercontent.com/headmkyoto-star/threads-auto-post/main/videos/"

DAILY_THEMES = [
    # 体の疲れ・感覚系
    "頭が重たくてぼーっとする感じについて",
    "目の奥の疲れとドライヘッドスパの相性",
    "寝ても疲れが取れない感じについて",
    "スマホを長時間使った後の頭の重さ",
    "力を抜くのが意外と難しいという話",
    "深呼吸が自然とできるようになる瞬間",
    "頭をほぐすと体全体がゆるんでいく感じ",
        "首や肩に力が入りっぱなしになってる話",
    "夕方になると頭が重くなる話",
    "耳の周りや側頭部が張ってる感覚",
    "集中しすぎて頭が熱くなる感じ",
    "頭皮が硬くなってることに気づいてない話",
    "目がしょぼしょぼする日の頭の疲れ",
    "仕事終わりに頭がずっと動いてる感じ",
    "体は休んでても頭だけ疲れてる話",

    # こんな方に来てほしい系
    "普段頑張りすぎてる人こそ頭を休めてほしい",
    "頭痛じゃなくても頭の疲れはちゃんとある",
    "デスクワークが多い方の頭の重さあるある",
    "なんとなく体がだるい日が続く方へ",
    "休日なのにゆっくり休めた気がしない方へ",
    "スマホをよく見る方の頭の疲れについて",
    "細かい作業や集中仕事が多い方へ",
    "運転が多くて首がこりやすい方へ",
    "人と話すことが多くて疲れやすい方へ",
    "忙しくて自分のことを後回しにしてる方へ",
    "睡眠は取れてるのに疲れが抜けない方へ",

    # セラピスト日常・気持ち系
    "この仕事をしていて好きな瞬間",
    "施術中に集中してる感覚が好きな話",
    "お客さんが満足して帰るときの気持ち",
    "施術中に眠ってしまうお客さんが多い話",
    "施術後にお客さんの表情がほぐれる瞬間",
    "リピートしてくれるお客さんへの感謝",
    "初めてドライヘッドスパを受けた方の反応",
    "施術前と後で体の感覚がガラッと変わる話",
    "お客さんの頭の硬さに毎回驚く話",
    "この仕事を選んでよかったと思う瞬間",
    "施術室が好きな理由",
    "静かな空間で集中する心地よさ",
    "技術を磨きたいと思うきっかけ",
    "うまく緩められたときの手の感覚",
    "お客さんが眠れた日の達成感",

    # ドライヘッドスパの気持ちよさ系
    "完全に力を抜いてもらうときの気持ちよさ",
    "静かな空間で頭をほぐす時間について",
    "ドライヘッドスパを受けた後のすっきり感",
    "頭をさわってもらう気持ちよさって独特",
    "施術中の静けさと心地よさについて",
    "頭皮がほぐれると顔までスッキリする話",
    "施術中に頭が軽くなっていく感覚",
    "首がすっと伸びる感じについて",
    "ぐっすり眠れるようになったという話",
    "誰かに頭を任せる感覚って独特だという話",

    # 日常・ご褒美系
    "頑張りすぎた日の自分へのご褒美",
    "一人でゆっくりする時間の大切さ",
    "仕事終わりにほっとできる場所について",
    "週に一度だけ自分を優先してもいい話",
    "忙しい日が続いたときこそケアが必要な話",
    "何も考えなくていい時間があってもいいという話",
    "ぼーっとしていい時間の贅沢さ",
    "自分のことを後回しにしがちな人へ",

    # お客さんとの話系（個人情報なし）
    "常連さんに教えてもらった頭の疲れサイン",
    "初めて来たのにすぐ眠れた方の話",
    "遠くから来てくれるお客さんへの感謝",
    "施術後にすごく喜んでくれた日の話",
    "久しぶりに来てくれた方が言ってたこと",

    # 連休・時期系
    "連休明けの体の重さについて",
    "長期休暇後に体がリセットされない話",
    "気温の変化で体がしんどくなる話",
    ]

POST_STYLES = [
    {"name": "共感系", "instruction": "お客さんの気持ちに寄り添う共感系。「〜って感じしませんか？」「〜な日ってありますよね」のように、読み手の体験に寄り添う構造で書く"},
    {"name": "気づき系", "instruction": "施術や仕事で気づいたことをさらっと伝える気づき系。「最近気づいたんですけど〜」「施術してて思うのは〜」のように、ふと気づいたことを共有する構造で書く"},
    {"name": "本音系", "instruction": "セラピストとして思うことをぽつりと言う本音系。短くていい。「本音を言うと〜」「正直なところ〜」のように、率直な気持ちを書く"},
    {"name": "驚き系", "instruction": "意外な事実や体の仕組みを伝える驚き系。「実は〜」「意外と知られてないんですけど〜」のように、驚きの情報から始める構造で書く"},
    {"name": "問いかけ系", "instruction": "いきなり問いかけから始める問いかけ系。「最近どうですか？」「〜って疲れてませんか？」のように、読み手への問いから始める"},
    {"name": "来店誘導系", "instruction": "「〜な方はぜひ」「京都祇園でお待ちしています」のような来店を促す投稿。押し付けがましくならないように"},
    {"name": "日記系", "instruction": "その日の施術で感じたこと・うれしかったこと・気づいたことをさらっと書く日記系。「今日のお客さんが〜」では始めない。お客さんの個人情報は絶対書かない。「最近思うのは〜」「ふと感じるのは〜」のように視点を変えて書く"},
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

def get_media():
    """画像・動画リストをGitHub APIから取得。GitHub認証で5000req/hourに拡大"""
    images_pool = []
    videos_pool = []
    GH_TOKEN = os.environ.get("GH_TOKEN", "")
    api_headers = {"Authorization": "token " + GH_TOKEN} if GH_TOKEN else {}
    # 画像取得（最大3回リトライ）
    for attempt in range(3):
        try:
            r = requests.get(GITHUB_API_IMAGES, headers=api_headers, timeout=10)
            print("IMAGE_API_STATUS:" + str(r.status_code))
            if r.status_code == 200 and isinstance(r.json(), list):
                for f in r.json():
                    if f["name"].lower().endswith((".jpg",".jpeg",".png")):
                        images_pool.append({"url": GITHUB_RAW_BASE + f["name"].replace(" ","%20"), "type": "IMAGE"})
                print("IMAGE_COUNT:" + str(len(images_pool)))
                break
            elif r.status_code == 403:
                print("IMAGE_API_RATELIMIT:" + str(r.json())[:100])
            else:
                print("IMAGE_API_ERROR:" + str(r.json())[:100])
        except Exception as e:
            print("IMAGE_EXCEPTION:" + str(e)[:80])
        time.sleep(2)
    # 動画取得（最大3回リトライ）
    for attempt in range(3):
        try:
            r = requests.get(GITHUB_API_VIDEOS, headers=api_headers, timeout=10)
            print("VIDEO_API_STATUS:" + str(r.status_code))
            if r.status_code == 200 and isinstance(r.json(), list):
                for f in r.json():
                    if f["name"].lower().endswith((".mp4",".mov")):
                        videos_pool.append({"url": GITHUB_RAW_VIDEOS + f["name"].replace(" ","%20"), "type": "VIDEO"})
                print("VIDEO_COUNT:" + str(len(videos_pool)))
                break
            elif r.status_code == 403:
                print("VIDEO_API_RATELIMIT:" + str(r.json())[:100])
            else:
                print("VIDEO_API_ERROR:" + str(r.json())[:100])
        except Exception as e:
            print("VIDEO_EXCEPTION:" + str(e)[:80])
        time.sleep(2)
    # 13時は動画必須（取れなかったら例外→shell側の再試行へ）
    jst = datetime.timezone(datetime.timedelta(hours=9))
    hour = datetime.datetime.now(jst).hour
    if hour == 13:
        if videos_pool:
            chosen = random.choice(videos_pool)
            print("MEDIA_CHOSEN:13H_VIDEO:" + chosen["url"].split("/")[-1][:40])
            return chosen
        else:
            raise RuntimeError("13H_VIDEO_REQUIRED_BUT_NONE_FOUND")
    # その他の時間: 画像・動画ランダム
    media_pool = images_pool + videos_pool
    if not media_pool:
        return None
    chosen = random.choice(media_pool)
    print("MEDIA_CHOSEN:" + chosen["type"] + ":" + chosen["url"].split("/")[-1][:40])
    return chosen

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
・文の末尾に絵文字を1つつける（😮‍💨🙌😅🫠🤔💆👀💪🥺😬💭など）。ネカマ絵文字（🩷💗🌸🫶）は使わない
・「。」「、」は使わない
・時間に関する表現は一切使わない
・「完全個室」「ヘッドセラピー」は使わない
・「あなた」という表現は使わない
・「僕たち」「私たち」「スタッフ一同」など複数形の主語は使わない
・一人称は省略するか「私」のみ。投稿者は若い女性セラピスト設定（「またあなたに来たい」などNG。「また来たい」「またお願いしたい」のように自然に言い換える）
・施術名は「ヘッドスパ」ではなく必ず「ドライヘッドスパ」と書く
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
・文の末尾に絵文字を1つつける（😮‍💨🙌😅🫠🤔💆👀💪🥺😬💭など）。ネカマ絵文字（🩷💗🌸🫶）は使わない
・「。」「、」は使わない
・時間に関する表現は一切使わない
・「完全個室」「ヘッドセラピー」は使わない
・ハッシュタグなし
・追加する一言だけ出力（書き出しは繰り返さない）"""
        return PROMO_OPENING_B + "\n" + call_claude(prompt_text)

    else:
        season = get_season()
        style = random.choice(POST_STYLES)
        print("STYLE_CHOSEN:" + style["name"])
        print("THEME_CHOSEN:" + theme[:40])
        prompt_text = f"""京都祇園にあるドライヘッドスパ店「ヘッドミント」のセラピストとして、Threadsに投稿する文を1つ書いて。店には複数のセラピストがいて、毎回違うスタッフが投稿している設定。

テーマ:「{theme}」

【今回の投稿スタイル（必ずこのスタイルで書く）】
{style["name"]}: {style["instruction"]}

【最重要：自然さ・短さ】
・AIっぽい完璧な文章は絶対NG。リアルな人が書いた短いつぶやき感を目指す
・1〜2文だけ。多くても短い文を3つまで
・「〜なんですよね」「〜ですよね」「〜だなぁ」「〜って感じ」のような口語表現をたまに使う
・接続詞（「そして」「だから」「でも」など）の連発は禁止。最大1個まで
・きれいにまとめようとしない。途中で終わる感じや余韻があってOK
・40〜55文字を厳守。これより長いのは絶対ダメ
【最重要ルール・必ず守ること】
・絶対に各文の末尾に絵文字をつける。1文でも絵文字なしの行を作らない
・「。」「、」は絶対に使わない。句読点を一切入れない
・「」（鍵括弧）は絶対に使わない。引用・強調でも「」は使わない。誰かのセリフや感想を書くときも「」で囲まず、地の文として書く（例：×「気持ちいい」→ ○ 気持ちいいって😊）

【ルール】
・40〜55文字以内（必ず守る！）
・ですます調ベースで書く。ただし堅くならない。若いセラピストがサロンのSNSに書くような親しみやすくて温かみのある口調（例：「気になる方はぜひ」「〜って感じしませんか？」「ぜひ来てみてください」）
・タメ口は使わない。「いらっしゃいます」「〜される方」など硬い敬語も使わない
・「。」「、」は絶対に使わない
・「〜多いですよ」「〜あります」など事実を断言して文を終わらせない。各文は次へ自然につながるか、最後は問いかけで締める
・各文の末尾に絵文字をつける。基本は1つ。**1投稿に必ず1箇所は連続絵文字（2つ並び）を入れる**。連続絵文字の組み合わせ例: 💆‍♀️🫧・🤩❓・🐑💤・😴🫧・😓💦・😮‍💨🫠・🥺💭・😴✨・💪🔥・👀💦・🧘✨・😅💆・🙌😊・🤔💆‍♀️・😶‍🌫️🛌・💤🐑。同じ絵文字を1投稿内で繰り返さない。投稿ごとに使う絵文字を変える（😮‍💨🙌😅🫠🤔💆👀💪🥺😬💭🧠😶‍🌫️😓😴😵‍💫🤯💆‍♂️🛌🔋⚡🧘✨😤😮😑💦🥰💖など豊富に使い分ける。🥰💖はたまに使う程度でOK）
・🩷💗🌸🫶などネカマ絵文字は使わない
・🧠は頭の重さ・ぼーっとする・考えすぎなど頭に直接関係する内容のときだけ使う。多用しない
・「？→絵文字」が基本、感情強め時は「絵文字→？」もあり
・「。」「、」は使わない
・時間・季節・情景描写はしない
・モヤモヤ・不安・気分の落ち込みなど心理的なネガティブ内容は書かない。体の疲れ・施術・お客さんに関連した内容にする
・解剖学・筋肉の構造・技術的な説明など医療・専門系の内容は書かない。ドライヘッドスパはリラクゼーションなので癒し・気持ちよさ・疲れが取れる感覚に寄せる
・カウンセリング技法・施術の進め方・セラピストとしての意識・プロ意識系の内容も書かない
・京都の街並み・天気・飲食店など施術と無関係な話は絶対に書かない。必ずサロン・施術・体の疲れ・お客さんに関連した内容にする
・方言は無理に入れない。「めっちゃ」「ほんま」「〜やん」程度なら自然に使っていい。それ以外の関西弁は使わない
・「完全個室」「ヘッドセラピー」は使わない
・ハッシュタグなし・文と文の間は改行
・1文を途中で改行しない。改行は必ず絵文字の直後（文と文の間）だけ。詩のように1行1フレーズに切る書き方は絶対にしない
・投稿文だけ出力"""

        return call_claude(prompt_text, max_tokens=200)

def create_thread(text, media=None):
    url = "https://graph.threads.net/v1.0/" + USER_ID + "/threads"
    media_type = media["type"] if media else "TEXT"
    params = {"media_type": media_type, "text": text, "access_token": ACCESS_TOKEN}
    if media and media["type"] == "IMAGE":
        params["image_url"] = media["url"]
    elif media and media["type"] == "VIDEO":
        params["video_url"] = media["url"]
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
    post_text = post_text.replace("「", "").replace("」", "")
    print("GENERATED_OK")
    media = get_media()
    print("MEDIA:" + (media["type"] if media else "NONE"))
    used_media = False
    result = create_thread(post_text, media)
    if "id" in result:
        container_id = result["id"]
        if media:
            wait_secs = 60 if media["type"] == "VIDEO" else 30
            print(f"WAIT:{wait_secs}s for {media['type']}")
            time.sleep(wait_secs)
            used_media = True
        else:
            time.sleep(5)
        pub = publish_thread(container_id)
        if pub.get("id"):
            print("SUCCESS_WITH_IMAGE" if used_media else "SUCCESS_TEXT_ONLY")
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
