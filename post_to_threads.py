import anthropic, requests, os, random, time
ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN", "")
USER_ID = "27185017111098955"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/headmkyoto-star/threads-auto-post/main/images/"
GITHUB_API_IMAGES = "https://api.github.com/repos/headmkyoto-star/threads-auto-post/contents/images"
def get_image_url():
    try:
        r = requests.get(GITHUB_API_IMAGES)
        files = r.json()
        images = [f["name"] for f in files if f["name"].lower().endswith((".jpg",".jpeg",".png"))]
        if images:
            return GITHUB_RAW_BASE + random.choice(images).replace(" ","_")
    except: pass
    return None
def generate_post():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    if random.random() < 0.2:
        p = "ドライヘッドスパ専門サロンのセラピストとして営業投稿を作成。必ず改行して絵文字を入れる。70分3980円を含む。ハッシュタグなし。150文字以内。投稿文のみ出力。"
    else:
        p = "ドライヘッドスパ専門サロンのセラピストとして日常日記系の投稿を作成。必ず改行して絵文字を入れる。ハッシュタグなし。150文字以内。営業色なし。投稿文のみ出力。"
    msg = client.messages.create(model="claude-opus-4-6", max_tokens=300, messages=[{"role":"user","content":p}])
    return msg.content[0].text.strip()
def post_to_threads(text, image_url=None):
    if image_url:
        r = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads", params={"media_type":"IMAGE","image_url":image_url,"text":text,"access_token":ACCESS_TOKEN})
        if r.status_code != 200: return post_to_threads(text, None)
        cid = r.json().get("id")
    else:
        r = requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads", params={"media_type":"TEXT","text":text,"access_token":ACCESS_TOKEN})
        cid = r.json().get("id")
    time.sleep(30)
    return requests.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish", params={"creation_id":cid,"access_token":ACCESS_TOKEN})
text = generate_post()
print(f"投稿:\n{text}\n")
img = get_image_url()
if img: print(f"画像: {img}\n")
r = post_to_threads(text, img)
print("✅ 成功！" if r.status_code == 200 else f"❌ {r.text}")
