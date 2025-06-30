import logging
import requests
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

TELEGRAM_TOKEN = '8007646725:AAFLp7AeRkK7XTKOUVMzSeLksYxigtZZnZk'  # <-- Вставьте сюда свой токен Telegram
VK_TOKEN = '128fbd02128fbd02128fbd027b11bae1c91128f128fbd027aedf0331c2bbca772df82c4'      # <-- Вставьте сюда токен VK

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Задание 1: Меню с кнопками "Привет" и "Пока"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Привет"), KeyboardButton("Пока")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.r8007646725:AAFLp7AeRkK7XTKOUVMzSeLksYxigtZZnZkeply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    text = update.message.text
    if text == "Привет":
        await update.message.reply_text(f"Привет, {user_first_name}!")
    elif text == "Пока":
        await update.message.reply_text(f"До свидания, {user_first_name}!")

# Задание 2: Кнопки с URL-ссылками
async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Новости", url="https://news.yandex.ru")],
        [InlineKeyboardButton("Музыка", url="https://music.yandex.ru")],
        [InlineKeyboardButton("Видео", url="https://www.youtube.com")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите ссылку:", reply_markup=reply_markup)

# Задание 3: Динамическая инлайн-клавиатура с возвратом назад
async def dynamic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Показать больше", callback_data="show_more")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Динамическое меню:", reply_markup=reply_markup)

async def dynamic_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "show_more":
        keyboard = [
            [InlineKeyboardButton("Опция 1", callback_data="option_1")],
            [InlineKeyboardButton("Опция 2", callback_data="option_2")],
            [InlineKeyboardButton("Назад", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_reply_markup(reply_markup=reply_markup)
    elif query.data == "back":
        keyboard = [[InlineKeyboardButton("Показать больше", callback_data="show_more")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_reply_markup(reply_markup=reply_markup)
    elif query.data == "option_1":
        await query.edit_message_text("Вы выбрали: Опция 1")
    elif query.data == "option_2":
        await query.edit_message_text("Вы выбрали: Опция 2")

# Интеграция VK API: команда /vkinfo <id или короткое имя>
async def vkinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Укажите VK ID или короткое имя: /vkinfo durov")
        return
    user_id = context.args[0]
    url = "https://api.vk.com/method/users.get"
    params = {
        "user_ids": user_id,
        "fields": "city,verified,domain",
        "access_token": VK_TOKEN,
        "v": "5.199"
    }
    try:
        response = requests.get(url, params=params).json()
        user = response['response'][0]
        text = f"Имя: {user['first_name']} {user['last_name']}\nVK: vk.com/{user['domain']}"
        if 'city' in user:
            text += f"\nГород: {user['city']['title']}"
        if user.get('verified'):
            text += "\n✔️ Аккаунт верифицирован"
        await update.message.reply_text(text)
    except Exception:
        await update.message.reply_text("Не удалось получить информацию о пользователе.")

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^(Привет|Пока)$"), menu_handler))
    application.add_handler(CommandHandler("links", links))
    application.add_handler(CommandHandler("dynamic", dynamic))
    application.add_handler(CallbackQueryHandler(dynamic_callback))
    application.add_handler(CommandHandler("vkinfo", vkinfo))

    print("Бот Cheblako_DZ запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()
