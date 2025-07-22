import telebot
import requests
import json
import os
from keep_alive import keep_alive

BOT_TOKEN = '7922820750:AAHdR4_c3RFXYrjZl0q3-CPNiCqgjQgAyM4'
NOTIFY_TO = '6404118457'

bot = telebot.TeleBot(BOT_TOKEN)
LOG_FILE = 'downloads.json'

def log_download(user_id, username, link):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []
    data.append({
        "user_id": user_id,
        "username": username,
        "link": link
    })
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_tiktok_video(url):
    try:
        response = requests.get("https://tikwm.com/api/", params={"url": url})
        data = response.json()
        if data.get('code') == 0 and 'play' in data.get('data', {}):
            return data['data']['play']
    except Exception as e:
        print("Error fetching video:", e)
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 مرحبك بك في بوت صيد معرفات تيك توك\n\nهذه البوت مدفوع، للاشتراك قم بمراسلة المطور @xx9kxx")

@bot.message_handler(func=lambda m: 'tiktok.com' in m.text)
def handle_link(message):
    link = message.text.strip()
    bot.reply_to(message, "⏳ جاري تحميل الفيديو...")
    video_url = get_tiktok_video(link)
    if video_url:
        try:
            bot.send_video(message.chat.id, video_url, caption="✅ تم التحميل بدون علامة مائية.")
            notify_text = (
                f"📥 تم تحميل فيديو جديد\n"
                f"👤 المستخدم: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
                f"🔗 الرابط: {link}"
            )
            bot.send_message(NOTIFY_TO, notify_text, parse_mode='Markdown')
            log_download(message.from_user.id, message.from_user.username or message.from_user.first_name, link)
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ لم أتمكن من إرسال الفيديو: {e}")
    else:
        bot.send_message(message.chat.id, "❌ لم أتمكن من تحميل الفيديو. تأكد من صحة الرابط أو حاول لاحقًا.")

keep_alive()
bot.polling()
