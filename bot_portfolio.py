
# Бот-портфолио для услуг
# Как запустить:
# 1. В Telegram найди @BotFather -> /newbot -> придумай имя -> получи TOKEN
# 2. Вставь TOKEN ниже вместо "ВСТАВЬ_ТОКЕН_СЮДА"
# 3. Установи библиотеку: pip install python-telegram-bot
# 4. Запусти: python bot.py
# Паспорт, самозанятость и прочее НЕ нужны. Только Telegram.
# Свои работы: замени PHOTO_ID / ссылки на свои фото. Можно просто положить фото рядом с ботом и отправлять по file_id.
# Как получить file_id: отправь фото боту @userinfobot или своему боту и посмотри в логах, либо пока оставь текст + ссылки на твой канал.

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "ВСТАВЬ_ТОКЕН_СЮДА"

# СЮДА ВСТАВЬ СВОЙ ЮЗЕРНЕЙМ БЕЗ @, например "vibecodegames"
MY_USERNAME = "ВСТАВЬ_СВОЙ_ЮЗЕРНЕЙМ"

logging.basicConfig(level=logging.INFO)

# ================== ТЕКСТЫ И ПРАЙСЫ - МЕНЯЙ ПОД СЕБЯ ==================

SERVICES = {
    "cards": {
        "title": "🎨 Карточки для WB / Ozon",
        "desc": "Продающие карточки, которые выделяют товар.\nФормат: 1200x1600, 3:4. Срок: от 30 минут.\nПервый эскиз покажу до оплаты.",
        "portfolio_text": "📸 Мои работы:\n1. Карточка для крема — главный слайд + инфографика\n2. Карточка для наушников — 5 слайдов\n3. Карточка для кружки — обложка + размеры\n\n👉 Все работы смотри тут: [твой канал / Behance]",
        # Если есть фото - вставь file_id или URL. Пока оставим заглушки, бот пришлет текст + кнопки.
        # Пример: "photos": ["https://.../photo1.jpg", "https://.../photo2.jpg"]
        "photos": [],
        "price": (
            "💰 ПРАЙС — Карточки WB / Ozon\n\n"
            "🟢 ЛЁГКАЯ — 1 обложка\n400 ₽\n• 1 главный слайд\n• 1 правка\n• Срок: 30 минут\n\n"
            "🟡 СТАНДАРТ — 5 слайдов\n1 500 ₽\n• Главный слайд + 4 инфо-слайда\n• Размеры, состав, комплектация\n• 2 правки\n• Срок: 1-2 часа\n\n"
            "🔴 МАКСИМУМ — 8 слайдов\n2 500 ₽\n• Полный комплект под WB + Ozon\n• 2 варианта обложки на выбор\n• 2 правки\n• Срок: 3-4 часа\n\n"
            "➕ Дополнительно:\n• 1 доп. слайд — 300 ₽\n• Адаптация WB -> Ozon — 400 ₽\n• Срочно за 30 минут — +50%\n\n"
            "Оплата: 50% до, 50% после. По СБП на карту."
        )
    },
    "present": {
        "title": "📊 Презентации PowerPoint",
        "desc": "Красивые презентации для диплома, бизнеса и школы.\nБез шаблонов из интернета — в твоем стиле.",
        "portfolio_text": "📸 Мои работы:\n1. Презентация для защиты диплома — 12 слайдов\n2. Презентация для бизнеса — 10 слайдов\n3. Школьная презентация — 8 слайдов",
        "photos": [],
        "price": (
            "💰 ПРАЙС — Презентации\n\n"
            "🟢 ЛЁГКАЯ — до 8 слайдов\n800 ₽\n• Титульник + текст + картинки\n• 1 правка\n• Срок: 1 час\n\n"
            "🟡 СТАНДАРТ — 10-12 слайдов\n1 200 ₽\n• Дизайн в едином стиле\n• Инфографика, таблицы, иконки\n• 2 правки\n• Срок: 2-3 часа\n\n"
            "🔴 МАКСИМУМ — 15+ слайдов\n2 000 ₽\n• Полный дизайн + анимация\n• Диаграммы и инфографика\n• 2 правки\n• Срок: 4-5 часов\n\n"
            "Оплата: 50% до, 50% после. По СБП."
        )
    },
    "excel": {
        "title": "📗 Excel / Word / Документы",
        "desc": "Таблицы с формулами, прайсы, учет, оформление документов.\nДелаю так, чтобы все считалось само.",
        "portfolio_text": "📸 Мои работы:\n1. Таблица учета товаров для WB — с формулами\n2. Прайс для магазина — 1 страница\n3. Оформленная курсовая в Word",
        "photos": [],
        "price": (
            "💰 ПРАЙС — Excel / Word\n\n"
            "🟢 ЛЁГКАЯ — 1 таблица / 1 документ\n500 ₽\n• Простая таблица или оформление\n• 1 правка\n• Срок: 30 минут\n\n"
            "🟡 СТАНДАРТ — таблица с формулами\n1 000 ₽\n• Формулы, фильтры, итоги\n• Красивое оформление\n• 2 правки\n• Срок: 1-2 часа\n\n"
            "🔴 МАКСИМУМ — учет под ключ\n1 500 ₽\n• Учет товаров / заказов / денег\n• Автоматический подсчет\n• Инструкция как пользоваться\n• Срок: 3-4 часа\n\n"
            "Оплата: 50% до, 50% после. По СБП."
        )
    },
    "resume": {
        "title": "📄 Резюме",
        "desc": "Резюме, которое заметят. Стильный PDF за 1 час.\nПришли опыт текстом — остальное сделаю я.",
        "portfolio_text": "📸 Мои работы:\n1. Резюме оператора ПК\n2. Резюме дизайнера инфографики\n3. Резюме менеджера маркетплейсов",
        "photos": [],
        "price": (
            "💰 ПРАЙС — Резюме\n\n"
            "🟢 ЛЁГКАЯ — 1 страница\n500 ₽\n• Стильный PDF\n• 1 правка\n• Срок: 30 минут\n\n"
            "🟡 СТАНДАРТ — резюме + сопроводительное\n700 ₽\n• Резюме + письмо работодателю\n• Инфографика навыков\n• 2 правки\n• Срок: 1 час\n\n"
            "🔴 МАКСИМУМ — для hh.ru + Авито\n1 000 ₽\n• Резюме + 2 варианта сопроводительного\n• Адаптация под 2 вакансии\n• Срок: 2 часа\n\n"
            "Оплата: 50% до, 50% после. По СБП."
        )
    },
    "filling": {
        "title": "🛒 Заполнение карточек WB / Ozon",
        "desc": "Заполню карточки в кабинете: фото, характеристики, описание.\nТы занимаешься продажами — я рутиной.",
        "portfolio_text": "📸 Мои работы:\n1. Заполнено 20 карточек для магазина косметики\n2. Заполнено 15 карточек для магазина одежды\n3. Таблица характеристик для 30 товаров",
        "photos": [],
        "price": (
            "💰 ПРАЙС — Заполнение карточек\n\n"
            "🟢 ЛЁГКАЯ — 1-5 карточек\n100 ₽ / карточка\n• Заполнение по твоему шаблону\n• Срок: 30 минут\n\n"
            "🟡 СТАНДАРТ — 10 карточек\n90 ₽ / карточка = 900 ₽\n• + таблица в Excel\n• Срок: 1-2 часа\n\n"
            "🔴 МАКСИМУМ — 20+ карточек\n80 ₽ / карточка\n• + проверка всех карточек\n• + таблица учета\n• Срок: 3 часа\n\n"
            "Оплата: за 5 карточек вперед по СБП, остальное после."
        )
    },
    "avito": {
        "title": "📢 Оформление Авито / VK / Telegram",
        "desc": "Обложки для Авито, оформление канала, шаблоны для постов.",
        "portfolio_text": "📸 Мои работы:\n1. 3 обложки для Авито — магазин техники\n2. Оформление Telegram-канала\n3. 3 шаблона для постов VK",
        "photos": [],
        "price": (
            "💰 ПРАЙС — Оформление\n\n"
            "🟢 ЛЁГКАЯ — 1 обложка Авито\n300 ₽\n• 1 картинка 800x600\n• 1 правка\n• Срок: 30 минут\n\n"
            "🟡 СТАНДАРТ — 3 обложки Авито\n900 ₽\n• Единый стиль\n• 2 правки\n• Срок: 1 час\n\n"
            "🔴 МАКСИМУМ — канал под ключ\n1 500 ₽\n• Аватар + 3 шаблона постов\n• Описание канала\n• Срок: 2-3 часа\n\n"
            "Оплата: 50% до, 50% после. По СБП."
        )
    },
}

# ================== КЛАВИАТУРЫ ==================

def main_menu():
    kb = [
        [InlineKeyboardButton("🎨 Карточки WB / Ozon", callback_data="svc_cards")],
        [InlineKeyboardButton("📊 Презентации", callback_data="svc_present")],
        [InlineKeyboardButton("📗 Excel / Word", callback_data="svc_excel")],
        [InlineKeyboardButton("📄 Резюме", callback_data="svc_resume")],
        [InlineKeyboardButton("🛒 Заполнение карточек", callback_data="svc_filling")],
        [InlineKeyboardButton("📢 Оформление Авито / VK", callback_data="svc_avito")],
        [InlineKeyboardButton("💬 Заказать / Написать мне", url=f"https://t.me/{MY_USERNAME}")],
    ]
    return InlineKeyboardMarkup(kb)

def service_menu(key):
    kb = [
        [InlineKeyboardButton("💰 Прайс", callback_data=f"price_{key}")],
        [InlineKeyboardButton("📸 Портфолио", callback_data=f"portfolio_{key}")],
        [InlineKeyboardButton("✅ Заказать", url=f"https://t.me/{MY_USERNAME}")],
        [InlineKeyboardButton("⬅️ Назад к услугам", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(kb)

def back_to_service(key):
    kb = [
        [InlineKeyboardButton("💰 Прайс", callback_data=f"price_{key}")],
        [InlineKeyboardButton("✅ Заказать", url=f"https://t.me/{MY_USERNAME}")],
        [InlineKeyboardButton("⬅️ Назад", callback_data=f"svc_{key}")],
    ]
    return InlineKeyboardMarkup(kb)

# ================== ХЕНДЛЕРЫ ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! 👋\n\n"
        "Я делаю карточки, презентации, таблицы и резюме.\n"
        "Быстро, без бирж и без паспорта — напрямую.\n\n"
        "Выбери услугу ниже 👇\n"
        "В каждой — портфолио и честный прайс."
    )
    await update.message.reply_text(text, reply_markup=main_menu())

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "back_main":
        await q.edit_message_text(
            "Выбери услугу 👇\nВ каждой — портфолио и прайс.",
            reply_markup=main_menu()
        )
        return

    if data.startswith("svc_"):
        key = data.replace("svc_", "")
        s = SERVICES[key]
        text = f"{s['title']}\n\n{s['desc']}\n\nНажми «Портфолио» — покажу 2-3 работы.\nНажми «Прайс» — покажу цены от лёгкой до сложной."
        await q.edit_message_text(text, reply_markup=service_menu(key))
        return

    if data.startswith("price_"):
        key = data.replace("price_", "")
        s = SERVICES[key]
        await q.edit_message_text(s['price'], reply_markup=back_to_service(key))
        return

    if data.startswith("portfolio_"):
        key = data.replace("portfolio_", "")
        s = SERVICES[key]
        # Если добавишь фото - бот отправит их, если нет - просто текст
        if s.get("photos"):
            try:
                media = [InputMediaPhoto(p) for p in s["photos"]]
                await q.message.reply_media_group(media)
            except Exception as e:
                print("Ошибка фото:", e)
        await q.edit_message_text(
            f"{s['title']}\n\n{s['portfolio_text']}\n\nХочешь так же? Жми «Заказать» 👇",
            reply_markup=back_to_service(key)
        )
        return

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_button))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
