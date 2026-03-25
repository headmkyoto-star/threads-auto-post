import requests
import random
import os

ACCESS_TOKEN = os.environ.get("SAKI_ACCESS_TOKEN", "SAKI_ACCESS_TOKEN")
USER_ID = os.environ.get("SAKI_USER_ID", "SAKI_USER_ID")

posts = [
    """今日のお客様に
「また来るね」って言ってもらえた☺️

その言葉がほんまに嬉しくて
もっと頑張ろうって思える(*>ᴗ<*)""",

    """施術中って
お客様といっぱいお話しできる時間🤍

今日も色んなこと話してくれて
なんか元気もらいました✨""",

    """ご指名いただけると緊張するけど
めちゃくちゃ嬉しい！

期待に応えられるよう
今日も全力で頑張ります(*´︶`*)♡""",

    """朝からオーナーとミーティング🤔💭
自分の強みって何やろって考えた

まだまだ成長中やけど
毎日少しずつ前進してます！""",

    """お客様の体のコリが
ほぐれていく瞬間が好き☺️

スッキリしたって笑顔見ると
この仕事やっててよかったなって思う""",

    """スタッフとのお昼が
一番の癒し時間です🍱

他愛もない話してるだけで
午後もまた頑張れる(*>ᴗ<*)""",

    """セラピストって
技術だけやなくて
気持ちも届けるお仕事やと思ってる🤍

今日も心を込めて施術します！""",

    """リピートしてくださるお客様って
ほんまにありがたい存在(,,> <,,)

信頼してもらえるよう
これからも丁寧に続けていきます☺️""",

    """「めっちゃスッキリした！」って言ってもらえると
疲れが全部吹き飛ぶ感じがする☺️

この一言のために頑張れてるんかもしれん""",

    """お客様の笑顔が見たくて
今日も元気に出勤しました(*´︶`*)♡

一人ひとりに寄り添える
セラピストでいたいな🤍"""
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
