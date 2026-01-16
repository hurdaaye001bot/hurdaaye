import os
import telebot
import requests
from flask import Flask

# web server for hosting
app = Flask(__name__)
@app.route('/')
def home(): return "Hurdaaye is awake"

# bot setup
BOT_TOKEN = "7973315664:AAFmsTRNTqjVDD5hrrDnOIXbcNut7AJvlTQ"
GEMINI_KEY = "AIzaSyDGD1_UKUmfj1U-UtTDE1epfkoznvOQyZo"
bot = telebot.TeleBot(BOT_TOKEN)
user_memory = {}

def get_gemini_response(user_id, text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    if user_id not in user_memory: user_memory[user_id] = []
    user_memory[user_id].append({"role": "user", "parts": [{"text": text}]})
    if len(user_memory[user_id]) > 10: user_memory[user_id] = user_memory[user_id][-10:]
    payload = {"contents": user_memory[user_id], "system_instruction": {"parts": [{"text": "Your name is Hurdaaye. Human friend."}]}}
    try:
        r = requests.post(url, json=payload, timeout=30)
        bot_text = r.json()['candidates'][0]['content']['parts'][0]['text']
        user_memory[user_id].append({"role": "model", "parts": [{"text": bot_text}]})
        return bot_text
    except: return "slow signal friend try again"

@bot.message_handler(func=lambda m: True)
def handle(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, get_gemini_response(m.from_user.id, m.text))

if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))).start()
    print("HURDAAYE IS STARTING...")
    bot.infinity_polling()
