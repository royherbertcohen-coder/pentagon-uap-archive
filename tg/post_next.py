"""Post the next queued item to the UFO.IL Telegram channel. Queue: tg/queue.json (list of {date, video_url, caption}).
Posts every entry whose date <= today (Israel) and not yet posted; marks posted in tg/posted.json."""
import json, os, urllib.request, datetime, zoneinfo
T = os.environ["TG_BOT_TOKEN"]; CHAT = os.environ["TG_CHAT_ID"]
today = datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Jerusalem")).date().isoformat()
q = json.load(open("tg/queue.json", encoding="utf-8"))
posted = set(json.load(open("tg/posted.json", encoding="utf-8"))) if os.path.exists("tg/posted.json") else set()
for e in q:
    key = e["date"] + "|" + e["video_url"]
    if e["date"] <= today and key not in posted:
        body = json.dumps({"chat_id": CHAT, "video": e["video_url"], "caption": e["caption"], "supports_streaming": True}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{T}/sendVideo", data=body, headers={"Content-Type": "application/json"})
        r = json.loads(urllib.request.urlopen(req, timeout=120).read())
        print(e["date"], r.get("ok"), r.get("description", ""))
        if r.get("ok"): posted.add(key)
json.dump(sorted(posted), open("tg/posted.json", "w", encoding="utf-8"), indent=0)
