from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "-------------------------------------"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=["Привет"])
async def hy_message(message):
    # print("Поздоровались")
    await message.answer("Введите команду /start, чтобы начать общение")


@dp.message_handler(commands=["start"])
async def start_message(message):
    # print("Привет! Я бот, помогающий твоему здоровью.")
    await message.answer("Привет! Я бот, помогающий твоему здоровью.")


# @dp.message_handler()
# async def all_message(message):
#     print("Введите команду \start, чтобы начать общение")
#     # await message.answer(message.text.upper())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
