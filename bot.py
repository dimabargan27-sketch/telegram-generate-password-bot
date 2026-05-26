import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import random
import string
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CopyTextButton
import os

#токен бота
TOKEN = "8999001074:AAEdnvz5qRLinqsAigiN4U7HSordpWasrAM"

#создание бота
bot = Bot(token = TOKEN)
dp = Dispatcher()

#команды
@dp.message(Command("create"))
async def create(message: types.Message):
    await message.answer("Введите длину вашего пароля (от 4 до 30 символов).")

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Привет! Я бот-генератор паролей.\n\n"
        "Используй команду /create, чтобы начать генерацию пароля.")

#обработчик сообщений
@dp.message()
async def generate_password(message: types.Message):

    #превращяем строку в число
    try:
        password_length = int(message.text)

        #проверка на длину пароля
        if password_length < 4:
            await message.answer("*❌ Пароль должен состоять минимум из 4 символов. Введите данные корректно.*", parse_mode="Markdown")
            return
        if password_length > 30:
            await message.answer("*❌ Максимальная длина пароля 30 символов. Введите данные корректно.*", parse_mode="Markdown")
            return
        
        #генерация паролей
        simvols = string.ascii_letters + string.digits + string.punctuation
        user_password = "".join(random.choice(simvols) for _ in range(password_length))

        #кнопка сохранения пароля
        copy_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="📋 Скопировать пароль",
                    copy_text = CopyTextButton(text = user_password)
                )]
            ]
        )

        #отправляем результат
        await message.answer(
            f"🔐 Твой пароль:\n{user_password}\n\nЧтобы сгенерировать новый, отправь /create",
            reply_markup=copy_button
            )

    #обработчик ошибок
    except ValueError:
        await message.answer("*❌ Пожалуйста введите ЧИСЛО - длину пароля.*", parse_mode="Markdown")

#запуск бота
async def main():
    port = int(os.environ.get("PORT", 8080))
    print(f"Бот запущен на порту {port}...")
    await dp.start_polling(bot)

#проверка точки входа файла
if __name__ == "__main__":
    asyncio.run(main())
