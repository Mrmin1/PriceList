# Бот-портфолио - полностью через GitHub, бесплатно, без Render

1. Залей ВСЕ файлы из архива на GitHub (включая папку .github)
2. Settings -> Secrets and variables -> Actions -> New repository secret:
   BOT_TOKEN = токен от @BotFather
   MY_USERNAME = твой юзернейм без @
3. Actions -> portfolio-bot -> Run workflow -> Run workflow
4. Открой своего бота в Telegram, нажми /start

Как работает: GitHub каждые 5 минут запускает бота на 4 минуты. Бот отвечает на кнопки. Потом выключается и запускается заново. Клиент этого почти не замечает - задержка максимум 1-2 минуты.
Никаких $7, никакого ПК, токен НЕ в коде, только в Secrets.
