from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage

# ใส่ Channel Access Token ของคุณที่นี่
CHANNEL_ACCESS_TOKEN = ("fdkj/piRdfWx2r5akI1dgyN7kW9bnCrXxio0MlhikwnPxSojWximYAwMTWeLIHLtvIjzQocn"
                        "/0KFZ6Bbj8gW9jfZ82IbLymSkQBtb46ZRCNHYbTQ0dK4a7wOrB7f0u9CzK6LSaBcP5sjPqh+X/bBngdB04t89/1O"
                        "/w1cDnyilFU=")

# LINE User ID (สามารถหาได้จาก webhook หรือแอปของคุณ)
MY_USER_ID = "U19a4825bc38592729c5b80681e107301"

# สร้าง LINE API Client
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# ส่งข้อความ
message = TextSendMessage(text="Hello! นี่คือข้อความจาก Python LINE Bot 🚀")
line_bot_api.push_message(MY_USER_ID, message)

print("ส่งข้อความสำเร็จ!")
