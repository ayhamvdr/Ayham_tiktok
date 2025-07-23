import telebot
import requests
from keep_alive import keep_alive  # ← لإبقاء البوت يعمل

BOT_TOKEN = "7922820750:AAHdR4_c3RFXYrjZl0q3-CPNiCqgjQgAyM4"
NOTIFY_TO = "6404118457"

bot = telebot.TeleBot(BOT_TOKEN)

def get_tiktok_video(url):
    try:
        response = requests.get("https://tikwm.com/api/", params={"url": url})
        data = response.json()
        if data['code'] == 0:
            return data['data']['play']
        return None
    except:
        return None

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "👋 أرسل رابط فيديو من TikTok وسأقوم بتحميله بدون علامة مائية.")

@bot.message_handler(func=lambda m: "tiktok.com" in m.text)
def handle_link(message):
    bot.reply_to(message, "⏳ جاري تحميل الفيديو...")
    video_url = get_tiktok_video(message.text.strip())
    if video_url:
        bot.send_video(message.chat.id, video_url, caption="✅ تم التحميل بدون علامة مائية.")
        bot.send_message(NOTIFY_TO, f"📥 تحميل جديد من [{message.from_user.first_name}](tg://user?id={message.from_user.id})", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ لم أتمكن من تحميل الفيديو. تأكد من الرابط.")

keep_alive()  # لتشغيل السيرفر
bot.polling()
