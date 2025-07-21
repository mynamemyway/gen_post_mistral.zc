# 🤖 Telegram Bot на базе Mistral AI

Простой Telegram-бот, генерирующий текстовые посты и изображения с помощью **Mistral AI API**.  
Использует `pyTelegramBotAPI`, `mistralai`, `python-dotenv`, и поддерживает логирование.

---

## 📌 Основные возможности

- 🚀 Генерация текстовых постов на основе пользовательского запроса  
- 🖼 Генерация изображений через Mistral AI (через `beta.agents`)  
- 📱 Простое взаимодействие через Telegram  
- 🧠 Выбор стиля генерации поста (логический, креативный, сбалансированный)
- 🧾 Поддержка эмодзи, хэштегов и структурированного текста  

---

## 🔧 Требования

Для запуска бота вам понадобится:

- Python 3.8+
- Установленные зависимости (поверенные):
  - `pyTelegramBotAPI==4.27.0`
  - `python-dotenv==1.1.1`
  - `mistralai==1.9.2`
  - `Pillow==11.3.0` [?]
  - `Flask==3.0.0`
- Учетные записи:
  - [Telegram Bot Token](https://core.telegram.org/bots/api )
  - [Mistral AI API Key](https://mistral.ai )
  - [WEBHOOK_HOST](https://render.com )

---

## 📦 Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/ ваше-имя/ваш-проект.git
cd ваш-проект
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создайте файл .env в корне проекта:

```env
TELEGRAM_BOT_TOKEN = "ВАШ Telegram Bot Token"
MISTRAL_API_KEY = "ВАШ Mistral AI API Key"
WEBHOOK_HOST = https://название-твоего-бота.onrender.com
```

## 🚀 Запуск бота

```bash
python3 bot.py
```

Бот начнет работу и будет ожидать инструкции для генерации от пользователя.

## 📱 Использование

1. Отправьте команду `/start` для приветствия
2. Выберите стиль генерации поста (температуру)
3. Введите тему поста и ожидайте генерацию

## 📁 Структура проекта
```
.
├── bot.py               # Основной код бота
├── .env                 # Файл с токенами
├── .gitignore           # Файлы и папки, исключённые из контроля версий
├── README.md            # Этот файл
└── requirements.txt     # Список зависимостей
```

## 📝 Пример .gitignore

Создайте файл .gitignore в корне проекта с таким содержимым:
```
# Виртуальное окружение
venv/
__pycache__/
*.pyc

# Персональные данные
.env
.env.local
.env.development
.env.test

# Логи
*.log
logs/

# Системные файлы
.DS_Store
Thumbs.db
```

## ⚠️ Возможные ошибки и решения

**Ошибка: "Mistral object has no attribute 'images'"**  
Mistral AI не поддерживает метод `images.generate` в текущей версии SDK. Используется `beta.agents`.

**Ошибка: "AuthenticationError"**  
Проверьте правильность ввода `TELEGRAM_BOT_TOKEN` и `MISTRAL_API_KEY` в `.env` файле.

**Ошибка: "No module named 'mistralai'"**  
Убедитесь, что вы установили библиотеку: `pip install mistralai==1.9.2`

## 📋 План по внедрению и доработке фич

**Прогресс:**  
☑ 8 из 13 фич реализовано  
`[████████████░░] 62%`

1. 🔄 Апгрейд взаимодействия:  
   ☑ Обращение к пользователю по имени из Telegram (`first_name` или `username`)  
   ☑ Генерация изображения к послу (временно отключена из-за лимитов)  
   ☑ Выбор стиль текста (температура = креативность)  
   ☐ Вкл / выкл хэштеги  
   ☐ Вкл / выкл эмодзи  

2. 🚀 Деплой на Render с настройкой вебхука:  
   ☑ `webhook`  
   ☑ Настройка env-переменных  
   ☑ Активация `setWebhook`  
   ☑ HTTPS-маршруты  
   ☑ Добавлен anti-sleep module для render.com  

3. ⏰ Автоматическая отправка постов:  
   ☐ Команда `/schedule`  
   ☐ Ежедневная/еженедельная рассылка  
   ☐ Использование `APScheduler`

## 📚 Полезные ссылки

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api )
- [Mistral AI Documentation](https://docs.mistral.ai/ )
- [Telegram бот на Python — пример](https://habr.com/ru/articles/750332/ )
- [Как работать с .env и load_dotenv](https://habr.com/ru/articles/662406/ )

## 📝 Лицензия
MIT License — см. файл LICENSE для деталей.