# 🤖 Telegram Bot на базе Mistral AI

Простой Telegram-бот, генерирующий текстовые посты и изображения с помощью **Mistral AI API**.  
Использует `pyTelegramBotAPI`, `mistralai`, `python-dotenv`, и поддерживает логирование.

---

## 📌 Основные возможности

- 🚀 Генерация текстовых постов на основе пользовательского запроса  
- 🖼 Генерация изображений через Mistral AI (через `beta.agents`)  
- 📱 Простое взаимодействие через Telegram  
- 🧾 Поддержка эмодзи, хэштегов и структурированного текста  

---

## 🔧 Требования

Для запуска бота вам понадобится:

- Python 3.8+
- Установленные зависимости:
  - `pyTelegramBotAPI==4.14.0`
  - `python-dotenv==1.0.0`
  - `mistralai==1.9.2`
  - `Pillow==9.5.0`
- Учетные записи:
  - [Telegram Bot Token](https://core.telegram.org/bots/api )
  - [Mistral AI API Key](https://mistral.ai )

---

## 📦 Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/ ваше-имя/ваш-проект.git
cd ваш-проект

2. Установите зависимости:

```bash
pip install -r requirements.txt

3. Создайте файл .env в корне проекта:

```env
TELEGRAM_BOT_TOKEN=ваш_telegram_bot_token
MISTRAL_API_KEY=ваш_mistral_api_key

🚀 Запуск бота

```bash
python3 bot.py

Бот начнет работу и будет ожидать идею для поста от пользователя в Telegram.

📱 Использование

Отправьте команду /start для приветствия
Нажмите кнопку "Генерировать пост 🚀"
Введите тему поста — бот сгенерирует текст и изображение

📁 Структура проекта

.
├── bot.py               # Основной код бота
├── .env                 # Файл с токенами
├── README.md            # Этот файл
├── requirements.txt     # Список зависимостей


⚠️ Возможные ошибки и решения
Ошибка: "Mistral object has no attribute 'images'"
Mistral AI не поддерживает метод images.generate в текущей версии SDK. Используется beta.agents для генерации изображений.
Ошибка: "AuthenticationError"
Проверьте правильность ввода TELEGRAM_BOT_TOKEN и MISTRAL_API_KEY в .env файле.
Ошибка: "No module named 'mistralai'"
Убедитесь, что вы установили библиотеку: pip install mistralai==1.9.2

📚 Полезные ссылки

Telegram Bot API Documentation
Mistral AI Documentation
Telegram бот на Python — пример
Как работать с .env и load_dotenv

📝 Лицензия
MIT License — см. файл LICENSE для деталей.