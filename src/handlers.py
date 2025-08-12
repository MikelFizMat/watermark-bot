from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.photo_handler import add_watermark
from src.settings import MENU

router = Router()


class FSMStates(StatesGroup):
    watermark_text = State()
    watermark_photo = State()
    nothing = State()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f"🧡 Рад вас видеть, {message.from_user.first_name}, здесь вы можете быстро наклеить водяной знак на любое фото",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=MENU))


@router.callback_query(F.data == "watermark")
async def watermark_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FSMStates.watermark_text)
    await callback.message.answer(text="💫введите текст, который будет на вотермарке:")


@router.message(FSMStates.watermark_text)
async def watermark_get_text(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(watermark_text=message.text)
        await state.set_state(FSMStates.watermark_photo)
        await message.answer("💫Теперь отправте фото для обработки:")
    else:
        await message.answer("💥Пока этот бот не поддерживает наложение других картинок, вы можете ввести текстом:")


@router.message(FSMStates.watermark_photo)
async def watermark_get_photo(message: Message, bot: Bot, state: FSMContext):
    keyboard = MENU
    keyboard[0] = [InlineKeyboardButton(text="Новая вотермарка 📝", callback_data="watermark")]
    if message.photo:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        photo_data = await bot.download_file(file.file_path)
        data = await state.get_data()
        watermarked_photo_bytes = add_watermark(photo_data, data.get("watermark_text"))
        await message.answer_photo(BufferedInputFile(watermarked_photo_bytes.read(), filename="watermarked.jpg"),
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
        await state.set_state(FSMStates.nothing)
    else:
        await message.answer("💥Введите фото")


@router.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await callback.message.answer(f"Это что-то типа pet проекта, он был создан на всякий случай для портфолио.\n"
                                  f"Проект написан на python благодаря aiogram и pillow\n"
                                  f"Здесь будет ссылка на github",
                                  reply_markup=InlineKeyboardMarkup(inline_keyboard=MENU))
