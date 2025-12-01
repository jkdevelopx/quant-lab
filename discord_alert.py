# แก้ discord_alert.py ทั้งไฟล์ใหม่ (คัดลอกทับเลย)

import requests
from datetime import datetime

# ใส่ webhook ของคุณตรงนี้ (หรือปล่อยว่างไว้ก็ได้ ไม่ error)
WEBHOOK = "https://discord.com/api/webhooks/1444548741439815741/2FLPVF2W0XJiznw81vRHHTWfQeaH85MXdM92G0uuCjwYBL0OD3KP3gQYwLm5Hl1JNryG"  # แก้ตรงนี้

def send_daily_signals(signals):
    if not WEBHOOK or "ใส่" in WEBHOOK or WEBHOOK == "":
        print("Webhook not set → Skip sending to Discord")
        return

    if not signals:
        payload = {"content": "No strong signals today."}
    else:
        embed = {
            "title": "AlphaSignal Pro — Daily Signals",
            "description": f"{len(signals)} high-confidence opportunities",
            "color": 3447003,
            "timestamp": datetime.utcnow().isoformat(),
            "fields": []
        }
        for s in signals[:10]:
            emoji = "STRONG BUY" if "STRONG" in s['signal'] else "BUY" if "BUY" in s['signal'] else "WATCH"
            embed["fields"].append({
                "name": f"{emoji} {s['symbol']}",
                "value": f"Confidence: {s['confidence']:.1%}\nPrice: ${s['price']:,.2f}",
                "inline": True
            })
        payload = {"embeds": [embed]}

    try:
        requests.post(WEBHOOK, json=payload)
        print("Signals sent to Discord!")
    except:
        print("Failed to send to Discord (check webhook URL)")