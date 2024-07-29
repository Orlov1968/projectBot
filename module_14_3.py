from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
# Инициализация клавиатуры и создание кнопок
kb = InlineKeyboardMarkup()
kb_1 = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
button_2 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
button_4 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
button_5 = InlineKeyboardButton(text="Product2", callback_data="product_buying")
button_6 = InlineKeyboardButton(text="Product3", callback_data="product_buying")
button_7 = InlineKeyboardButton(text="Product4", callback_data="product_buying")
kb.row(button_1, button_2)
kb_1.row(button_4, button_5, button_6, button_7)
buy_kb = ReplyKeyboardMarkup()
button_3 = KeyboardButton(text="Купить")
button_8 = KeyboardButton(text="Рассчитать")
button_9 = KeyboardButton(text="Информация")
buy_kb.row(button_8, button_9)
buy_kb.add(button_3)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Запуск бота и ответ на запуск
@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью", reply_markup=buy_kb)


# Пользователь написал "Рассчитать" - появилась клавиатура и предложение
@dp.message_handler(text="Рассчитать")
async def main_manu(message):
    await message.answer("Выберите опцию", reply_markup=kb)


# На нажатие кнопки "Формула расчёта" - выйдет формула
@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10 x вес(кг) + 6.25 х рост(см) + 5 х возраст(лет) - 161")
    await call.answer()


# На нажатие кнопки "Рассчитать норму калорий" - будет выполняться /
# последовательность ниже
@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()


#
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()


#
@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()  # Запись в словарь полученных данных от пользователя
    need_for_calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) + \
                        5 * float(data['age']) - 161  # Расчёт, согласно формулы
    await message.answer(f"Ваша норма калорий {need_for_calories}")
    await state.finish()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    with open("files_photo/i_4.webp", "rb") as photo_file:
        for i in range(1, 5):
            await message.answer_photo(photo_file, f"Название: продукт{i} | "
                                                   f"Описание: о продукте{i} |"
                                                   f" Цена: {i * 100}", reply_markup=kb_1)
    await message.answer("Выберите продукт для покупки", reply_markup=kb_1)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
