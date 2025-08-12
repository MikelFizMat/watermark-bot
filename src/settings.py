from aiogram.types import InlineKeyboardButton
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
MENU = [[InlineKeyboardButton(text="Создать водяной знак 📝", callback_data="watermark")],
        [InlineKeyboardButton(text="Об этом боте 🤖", callback_data="about")]]
