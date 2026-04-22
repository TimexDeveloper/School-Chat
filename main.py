import logging
import os
import sys
from openai import OpenAI

os.system('color')

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',    # Синий
        'INFO': '\033[92m',     # Зеленый
        'WARNING': '\033[93m',  # Желтый
        'ERROR': '\033[91m',    # Красный
        'RESET': '\033[0m'      # Сброс цвета
    }

    def format(self, record):
        log_fmt = f"{self.COLORS.get(record.levelname, '')}[%(levelname)s]{self.COLORS['RESET']} %(message)s"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

DEBUG_REM = False

logger = logging.getLogger("InformaticsAI")
logger.setLevel(logging.DEBUG if DEBUG_REM else logging.INFO)

ch = logging.StreamHandler()
ch.setFormatter(ColoredFormatter())
logger.addHandler(ch)

API_KEY = "your_key_here"

def fetch_informatics_data(grade):
    logger.debug(f"Попытка отправить запрос для {grade} класса через OpenRouter...")
    
    if API_KEY == "your_key_here":
        logger.error("API_KEY не установлен! Вставь ключ от OpenRouter в код.")
        return "Ошибка конфигурации: отсутствует API_KEY."

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY,
    )

    try:
        logger.debug("Ожидание ответа от сервера...")
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[
                {
                    "role": "user",
                    "content": f"Ты помощник по информатике. Расскажи кратко и понятно основные темы программы за {grade} класс российской школы. Используй списки."
                }
            ]
        )
        result = completion.choices[0].message.content
        logger.info(f"Данные для {grade} класса успешно получены.")
        return result

    except Exception as e:
        logger.error(f"Произошла ошибка при запросе: {e}")
        return "Произошла ошибка. Проверь интернет или API-ключ."

def main():
    print("="*50)
    print(" ПРИЛОЖЕНИЕ: ИНФОРМАТИКА 1-11 КЛАСС ")
    print("="*50)
    logger.info("Приложение готово к работе.")

    while True:
        print("\nВведите номер класса (1-11) или 'exit' для выхода:")
        user_input = input(">>> ").strip().lower()

        if user_input == 'exit':
            logger.warning("Завершение сеанса...")
            break
        
        if user_input.isdigit() and 1 <= int(user_input) <= 11:
            print(f"\n{'-'*20} ЗАГРУЗКА {'-'*20}")
            info = fetch_informatics_data(user_input)
            print("\n" + info)
            print("-" * 50)
        else:
            logger.error(f"Некорректный ввод: '{user_input}'. Введите число от 1 до 11.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\nПрограмма остановлена пользователем.")
        sys.exit()
