import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.markdown import hbold

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv("TG_TOKEN_MOEX")
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: types.Message):
    start_buttons = [
        [types.KeyboardButton(text="Начать отслеживание")],
        [types.KeyboardButton(text="Добавить бумаги")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=start_buttons,
        resize_keyboard=True,
        input_field_placeholder="Выбираем с чего начинаем"
    )
    await message.answer(f"Доброе утро {hbold(message.from_user.full_name)}! C чего начнем?", reply_markup=keyboard)


@dp.message(F.text.lower() == "начать отслеживание")
async def start_notifications(message: types.Message):
    await message.reply("В течение дня Вы будите получать сообщения об анломальных сделках на Московской бирже, "
                        "если таковые будут.", reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text.lower() == "добавить бумаги")
async def adding_shares_secid(message: types.Message):
    await message.reply("Вам необходимо внести SECID бумаги, которую Вы хотите отслеживать.")


async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
