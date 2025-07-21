import os
import telebot
from telebot import types
from dotenv import load_dotenv
from mistralai import Mistral
import io
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из файла .env
load_dotenv()

# --- Конфигурация API ключей ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Проверка, что токены загружены
if not TELEGRAM_BOT_TOKEN:
    logger.error(
        "Ошибка: Токен Telegram бота не найден в .env. Убедитесь, что TELEGRAM_BOT_TOKEN установлен."
    )
    exit(1)
if not MISTRAL_API_KEY:
    logger.error(
        "Ошибка: Ключ Mistral API не найден в .env. Убедитесь, что MISTRAL_API_KEY установлен."
    )
    exit(1)

# Инициализация Telegram бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Инициализация клиента Mistral API
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

# Глобальная переменная для хранения температуры
user_temperature = {}


def generate_text_with_mistral(prompt: str, temperature: float) -> str:
    """
    Генерирует текстовый пост с заданной температурой.
    """
    try:
        chat_response = mistral_client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "system",
                    "content": "Ты - креативный ассистент, который пишет интересные и уникальные посты.",
                },
                {
                    "role": "user",
                    "content": f"Напиши увлекательный пост, который вызывает эмоции на теме: '{prompt}', используй эмодзи и добавь хэштеги",
                },
            ],
            temperature=temperature,
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        logger.error(f"Ошибка при генерации текста с Mistral: {e}")
        if "AuthenticationError" in str(e) or "invalid api key" in str(e).lower():
            return "Не удалось сгенерировать текст. Проверьте ваш API ключ Mistral."
        return "Не удалось сгенерировать текст. Попробуйте еще раз."


def generate_image_with_mistral(prompt: str) -> bytes | None:
    """
    Генерирует изображение с помощью Mistral AI.
    """
    try:
        # Создание агента для генерации изображения
        image_agent = mistral_client.beta.agents.create(
            model="mistral-medium-2505",
            name="Агент генерации изображений",
            description="Агент, используемый для генерации изображений.",
            instructions="Используй инструмент для генерации изображений, когда тебя просят создать изображение. Генерируй изображения в высоком качестве.",
            tools=[{"type": "image_generation"}],
            completion_args={
                "temperature": 0.5,
                "top_p": 0.9,
            },
        )

        # Начало диалога с агентом
        response = mistral_client.beta.conversations.start(
            agent_id=image_agent.id,
            inputs=f"Создай уникальное и привлекательное изображение по запросу: '{prompt}'. Изображение должно соответствовать теме поста. Сгенерируй только одно изображение.",
        )

        # Поиск file_id в ответе
        file_id = None
        if hasattr(response, "outputs"):
            for chunk in response.outputs:
                if hasattr(chunk, "content"):
                    for content in chunk.content:
                        if hasattr(content, "type") and content.type == "tool_file":
                            file_id = content.file_id
                            break
                if file_id:
                    break

        if not file_id:
            logger.error(
                "Не удалось получить ID файла изображения из ответа Mistral. Возможно, агент не сгенерировал изображение или структура ответа изменилась."
            )
            return None

        # Скачивание файла изображения
        file_bytes_stream = mistral_client.files.download(file_id=file_id)
        return file_bytes_stream.read()
    except Exception as e:
        logger.error(
            f"Ошибка при генерации изображения с Mistral (через beta.agents): {e}"
        )
        return None


# --- Обработчики команд и сообщений Telegram бота ---
@bot.message_handler(commands=["start"])
def send_welcome(message):
    """
    Обработчик команды /start. Приветствует пользователя и предлагает меню с выбором стиля.
    """
    user_id = message.from_user.id
    user_temperature[user_id] = 0.7  # Стандартная температура

    user_name = (
        message.from_user.first_name or message.from_user.username or "пользователь"
    )
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Логический"),
        types.KeyboardButton("Креативный мастер"),
        types.KeyboardButton("Сбалансированный"),
    )

    bot.reply_to(
        message,
        f"Привет, {user_name}!\n"
        "Я твой личный генератор контента на основе Mistral AI🙏\n\n"
        "🪄 Выбери стиль генерации текста в меню:\n"
        "🔹 Логический — точный, структурированный текст\n"
        "🔹 Креативный мастер — яркий, неожиданный текст\n"
        "🔹 Сбалансированный — точность и эмоции в балансе\n\n"
        "✍ После выбора просто отправь мне тему для поста.",
        reply_markup=markup,
    )


@bot.message_handler(
    func=lambda message: message.text
    in ["Логический", "Креативный мастер", "Сбалансированный"]
)
def set_temperature(message):
    """
    Обработчик кнопок выбора температуры.
    """
    user_id = message.from_user.id
    style = message.text

    temps = {
        "Логический": 0.1,
        "Креативный мастер": 1.0,
        "Сбалансированный": 0.6,
    }
    user_temperature[user_id] = temps[style]

    bot.reply_to(
        message,
        f"Выбран стиль: {style}\n"
        "Теперь отправь мне тему поста, и я напишу его для тебя🙌",
        # reply_markup оставлен, как есть — кнопки не исчезают
    )


@bot.message_handler(func=lambda message: True)
def process_prompt_step(message):
    """
    Обработчик текстовых сообщений (промптов) от пользователя.
    Генерирует текст и изображение, затем отправляет их.
    """
    chat_id = message.chat.id
    user_prompt = message.text
    user_id = message.from_user.id
    user_name = (
        message.from_user.first_name or message.from_user.username or "пользователь"
    )
    temperature = user_temperature.get(user_id, 0.7)

    bot.send_message(
        chat_id,
        f"Уже генерирую твой пост, {user_name}🤍",
    )
    try:
        # Шаг 1: Генерация текста поста
        generated_text = generate_text_with_mistral(user_prompt, temperature)
        if not generated_text:
            bot.send_message(
                chat_id,
                "Не удалось сгенерировать текст поста. Попробуй ещё раз, возможно, проблема с API ключом.",
            )
            return

        # Шаг 2: Генерация изображения по тому же промпту
        generated_image_bytes = generate_image_with_mistral(user_prompt)

        # Шаг 3: Отправка результата
        if generated_image_bytes:
            image_file = io.BytesIO(generated_image_bytes)
            image_file.name = "generated_image.png"

            # Ограничение длины подписи до 1024 символов
            caption_limit = 1024
            truncated_caption = (
                (generated_text[:caption_limit] + "...")
                if len(generated_text) > caption_limit
                else generated_text
            )

            bot.send_photo(chat_id, image_file, caption=truncated_caption)
            logger.info(f"Пост и изображение отправлены пользователю {chat_id}")
        else:
            bot.send_message(
                chat_id,
                f"Вот твой пост, {user_name}:\n\n{generated_text}\n\n"
                "К сожалению, не удалось сгенерировать изображение. Возможно, превышен лимит запросов.",
            )
            logger.info(
                f"Пост отправлен пользователю {chat_id}, изображение не сгенерировано."
            )

    except Exception as e:
        logger.error(f"Непредвиденная ошибка в process_prompt_step: {e}")
        bot.send_message(
            chat_id, "Произошла непредвиденная ошибка. Пожалуйста, попробуй ещё раз."
        )


# --- Запуск бота ---
def run_bot():
    """
    Запускает бота в режиме long polling.
    """
    logger.info("Бот запущен и готов принимать сообщения.")
    bot.remove_webhook()
    logger.info("Вебхук успешно удален (если был).")
    bot.polling(none_stop=True)


if __name__ == "__main__":
    run_bot()
