import os
from dotenv import load_dotenv
from telebot import TeleBot, types
from google import genai

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN is not set (check your .env).")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set (check your .env).")

bot = TeleBot(TELEGRAM_TOKEN)

client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=["start"])
def start(user_message: types.Message):
    bot.send_message(
        user_message.chat.id,
        "привет, напиши свой вопрос - я отвечу с помощью Gemini"
    )

@bot.message_handler(func=lambda message: True)
def chatai(user_message: types.Message):
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message.text,
    )
    bot.send_message(user_message.chat.id, resp.text)

if __name__ == "__main__":
    bot.infinity_polling()