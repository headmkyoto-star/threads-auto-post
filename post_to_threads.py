import requests
import random

USER_ID = "27185017111098955"
ACCESS_TOKEN = "THREADS_ACCESS_TOKEN"

posts = [
    "今日もお客様の笑顔に癒されました✨ ヘッドスパ後の「スッキリした！」という言葉が何より嬉しいです。頭皮をほぐすことで、心もほぐれていく瞬間がたまりません🌿 #ヘッドスパ #京都祇園 #ヘッドミント京都 #セラピスト日記",
    "頭皮マッサージは血行促進に効果的です🩸 毎日のシャンプー時に、指の腹でくるくるとマッサージするだけでも違いますよ！ぜひ試してみてください✨ #ヘッドスパ #京都祇園 #ヘッドミント京都 #美容豆知識",
    "京都の朝は空気が澄んでいて、サロンへの道のりが気持ちいい🌸 今日も一日、お客様の頭皮と心を癒すために全力を尽くします💪 #ヘッドスパ #京都祇園 #ヘッドミント京都 #京都生活",
    "施術中に「気持ちよくて眠れました」とおっしゃっていただけると、本当に嬉しいです😊 ヘッドスパには深いリラクゼーション効果があります。ぜひ体験してみてください✨ #ヘッドスパ #京都祇園 #ヘッドミント京都",
    "最近気づいたこと💡 頭皮の状態は生活習慣を映す鏡だということ。睡眠・食事・ストレス…すべてが頭皮に現れます。定期的なケアで内側から美しく🌿 #ヘッドスパ #京都祇園 #ヘッドミント京都 #頭皮ケア",
    "今日はリピーターのお客様が久しぶりにご来店✨ 「ここに来ると元気になれる」という言葉に、セラピストをやっていてよかったと心から思いました🙏 #ヘッドスパ #京都祇園 #ヘッドミント京都",
    "ストレスが溜まると頭皮が固くなりやすいんです😣 定期的なヘッドスパで、頭皮をほぐしてリフレッシュしませんか？祇園の隠れ家サロンでお待ちしています🌸 #ヘッドスパ #京都祇園 #ヘッドミント京都",
    "今日の京都は風が心地よくて、施術後のお客様も外の空気を楽しんでいらっしゃいました🍃 こんな日のヘッドスパは格別ですね✨ #ヘッドスパ #京都祇園 #ヘッドミント京都 #京都",
]

def post_to_threads(text):
    url1 = f"https://graph.threads.net/v1.0/{USER_ID}/threads"
    data1 = {"media_type": "TEXT", "text": text, "access_token": ACCESS_TOKEN}
    r1 = requests.post(url1, data=data1)
    result1 = r1.json()
    creation_id = result1.get("id")
    if not creation_id:
        print(f"エラー: {result1}")
        return False
    url2 = f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish"
    data2 = {"creation_id": creation_id, "access_token": ACCESS_TOKEN}
    r2 = requests.post(url2, data=data2)
    print(f"投稿完了: {r2.json()}")
    return True

if __name__ == "__main__":
    post_text = random.choice(posts)
    print(f"投稿内容:\n{post_text}\n")
    post_to_threads(post_text)
