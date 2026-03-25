import requests
import random
import os

ACCESS_TOKEN = os.environ.get("HONOKA_ACCESS_TOKEN", "HONOKA_ACCESS_TOKEN")
USER_ID = os.environ.get("HONOKA_USER_ID", "HONOKA_USER_ID")

posts = [
    """セラピストになって
毎日が新しい発見の連続🌸

お客様から教えてもらうことって
ほんとにたくさんあるな〜って感じてる🥹""",

    """今日施術したお客様に
「手が温かいね」って言ってもらえた🥺💕

そんな一言がすごく嬉しくて
夜まで覚えてた笑""",

    """美容と健康って
切り離せないなってほんとに思う🌿

外見だけじゃなくて
内側からキレイになるお手伝いがしたい✨""",

    """休憩中にスタッフとカフェ☕

他愛もないおしゃべりが
一番のリフレッシュになるの知ってた？笑

明日も頑張れる気がする🌸""",

    """お客様が帰り際に振り返って
にこって笑ってくれた🥺

あの瞬間のためにこの仕事してるって
いつも思う💕""",

    """新しい技術の練習中🔥

最初は全然うまくいかないけど
できるようになった時の嬉しさが
やめられない理由のひとつ笑""",

    """セラピストって
人の体に触れる仕事だからこそ
自分も健康でいないとって思う🌿

最近ストレッチ習慣つけてます✨""",

    """今日のお客様に
「あなたに担当してもらってよかった」
って言ってもらえた🥺💕

この言葉、一生大事にします""",

    """朝、お店に来る前にコーヒー飲むのが最近の習慣☕

なんか気持ちが整う感じがして
お気に入りの時間になってる🌸""",

    """好きな香りに包まれながら施術するの
ほんとに幸せな時間だなって思う🌿

お客様にもその空気が届いてたらいいな💕"""
]

def post_to_threads(text):
    url1 = f"https://graph.threads.net/v1.0/{USER_ID}/threads"
    params1 = {"media_type": "TEXT", "text": text, "access_token": ACCESS_TOKEN}
    r1 = requests.post(url1, params=params1)
    container_id = r1.json().get("id")
    if not container_id:
        print("Error:", r1.json())
        return
    url2 = f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish"
    params2 = {"creation_id": container_id, "access_token": ACCESS_TOKEN}
    r2 = requests.post(url2, params=params2)
    print("Posted:", r2.json())

if __name__ == "__main__":
    post = random.choice(posts)
    print("Posting:", post)
    post_to_threads(post)
