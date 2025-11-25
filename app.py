import telebot, TOKEN, os

# Замените на свой токен
#BOT_TOKEN = TOKEN.NAME
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("Токен бота не задан! Установите переменную BOT_TOKEN.")

# Таблицы кодировок
MONTH_CODES = {
    1: 'N',   # Январь
    2: 'E',   # Февраль
    3: '1',   # Март
    4: 'P',   # Апрель
    5: 'M',   # Май
    6: 'Y',   # Июнь
    7: 'U',   # Июль
    8: 'K',   # Август
    9: 'O',   # Сентябрь
    10: 'R',  # Октябрь
    11: 'V',  # Ноябрь
    12: 'X'   # Декабрь
}

DAY_CODES = {
    1: "A",
    2: "F",
    3: "K",
    4: "P",
    5: "T",
    6: "X",
    7: "7",
    8: "B",
    9: "G",
    10: "L",
    11: "Q",
    12: "U",
    13: "Y",
    14: "14",
    15: "C",
    16: "H",
    17: "M",
    18: "R",
    19: "V",
    20: "Z",
    21: "21",
    22: "D",
    23: "I",
    24: "N",
    25: "S",
    26: "W",
    27: "27",
    28: "28",
    29: "E",
    30: "J",
    31: "O"
}

# Обратные словари для декодирования
REVERSE_DAY_CODES = {v: k for k, v in DAY_CODES.items()}
REVERSE_MONTH_CODES = {v: k for k, v in MONTH_CODES.items()}

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришлите закодированную дату в формате <день><месяц>, например: AFN (1 января) или OX (31 декабря).")

@bot.message_handler(func=lambda message: True)
def decode_date(message):
    text = message.text.strip()

    if not text:
        bot.reply_to(message, "Сообщение пустое. Пример: AFN")
        return

    decoded_day = None
    decoded_month = None

    # Перебираем возможные длины кода дня: от 1 до 4 символов
    for i in range(1, min(5, len(text) + 1)):
        day_code = text[:i]
        month_code = text[i:]

        if day_code in REVERSE_DAY_CODES and month_code in REVERSE_MONTH_CODES:
            decoded_day = REVERSE_DAY_CODES[day_code]
            decoded_month = REVERSE_MONTH_CODES[month_code]
            break

    if decoded_day is None or decoded_month is None:
        bot.reply_to(
            message,
            "Не удалось распознать дату. Убедитесь, что вы отправили корректную комбинацию в формате <день><месяц>.\n"
            "Примеры: AFN → 1 января, OX → 31 декабря."
        )
        return

    # Форматируем и отправляем результат
    bot.reply_to(
        message,
        f"Расшифрованная дата: {decoded_day:02d}.{decoded_month:02d}"
    )

if __name__ == '__main__':
    bot.polling(none_stop=True)