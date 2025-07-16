import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import os

from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message()
async def handle_message(message: Message):
    vin = message.text.strip()
    if len(vin) < 10:
        await message.reply("❌ Неверный VIN. Отправь корректный VIN-код.")
        return

    url = f"https://vindecoder.eu/api/v1/{vin}.json"
    try:
        response = requests.get(url)
        data = response.json()
        if "make" in data:
            text = f"🚗 Марка: {data['make']}\n📅 Год: {data['year']}\n🏭 Страна: {data.get('manufactured_in_country', 'N/A')}"
        else:
            text = "Не удалось найти данные по этому VIN."
    except Exception as e:
        text = f"Ошибка при запросе: {e}"

    await message.reply(text)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
