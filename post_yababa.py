import requests
import random
import os

ACCESS_TOKEN = os.environ.get("YABABA_ACCESS_TOKEN", "YABABA_ACCESS_TOKEN")
USER_ID = os.environ.get("YABABA_USER_ID", "YABABA_USER_ID")

posts = [
    """経営してると
うまくいく日ばかりじゃない

それでも続けてるのは
このお店が好きだから""",

    """スタッフが頑張ってる姿を見ると
自分も頑張らなあかんなと思う

支えてるつもりが
支えられてることの方が多い気がする""",

    """お客様からのありがとうが
スタッフに届いてるの見ると

オーナーやっててよかったと思う瞬間""",

    """失敗しても
次どうするかだけ考える

落ち込む時間がもったいない
…とはいえ少し落ち込む""",

    """スタッフに任せることを覚えてから
お店が変わった

全部自分でやろうとしてた頃の自分に
早く教えてあげたい""",

    """経営の勉強って終わりがない
知れば知るほど知らないことが増える

でもその感覚が嫌いじゃない""",

    """今日も一日
スタッフとお客様のために動く

それが自分の仕事やと思ってる""",

    """うまくいかない日もある
でも翌朝になったらリセットして
また動き出せる

それが続けるコツな気がしてる"""
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
