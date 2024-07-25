from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import asyncio

api = "-----------------------------------------"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
# Инициализация клавиатуры и создание кнопок, подстраивающихся под размер экрана
kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Рассчитать"), KeyboardButton \
    (text="Информация")]], resize_keyboard=True)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Создаём handler для запуска бота
@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=kb)


# Создаём обработчики сообщений
@dp.message_handler(text=["Рассчитать"])
async def set_age(message):
    await message.answer("Введите свой возраст")
    await UserState.age.set()  # Вызов ф-ции состояния


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)  # Заносим сообщение в базу состояния
    await message.answer("Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()  # Записываем в словарь все сообщения \
    # из базы состояния
    need_for_calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) + \
                        5 * float(data['age']) - 161  # Расчёт, согласно формулы
    await message.answer(f"Ваша норма калорий {need_for_calories}")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
