import telebot
import requests
import re

# ⚠️ ضع توكن البوت الخاص بك هنا
BOT_TOKEN = "8784566055:AAG-zPhJQ0NgR3HVMG61cjm-pK2BytnY1Xw"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط فيديو من تيك توك أو إنستغرام وسأقوم بتحميله لك فوراً. 🚀")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url_match = re.search(r'(https?://\S+)', message.text)
    
    if not url_match:
        bot.reply_to(message, "الرجاء إرسال نص يحتوي على رابط فيديو صحيح.")
        return

    url = url_match.group(0)
    status_msg = bot.reply_to(message, "جاري سحب الفيديو... ⏳")

    # الوسيط الأول للتيك توك
    api_url = f"https://api.tiklydown.eu.org/api/download?url={url}"

    try:
        response = requests.get(api_url).json()
        if "video" in response and "noWatermark" in response["video"]:
            video_url = response["video"]["noWatermark"]
            bot.send_video(message.chat.id, video_url, reply_to_message_id=message.message_id)
            bot.delete_message(message.chat.id, status_msg.message_id)
            return
    except:
        pass

    # الوسيط الثاني لإنستغرام وباقي المواقع
    try:
        generic_api = "https://co.wuk.sh/api/json"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        res = requests.post(generic_api, json={"url": url, "vQuality": "720"}, headers=headers).json()
        if "url" in res:
            bot.send_video(message.chat.id, res["url"], reply_to_message_id=message.message_id)
            bot.delete_message(message.chat.id, status_msg.message_id)
        else:
            raise Exception()
    except:
        bot.edit_message_text("عذراً، السيرفر مضغوط حالياً. جرب رابطاً آخر لاحقاً.", message.chat.id, status_msg.message_id)

# تشغيل البوت
bot.infinity_polling()
