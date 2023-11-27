from telebot import types
from datetime import datetime

from PIL import Image, ImageDraw

from bot import BOT as bot

import io

@bot.message_handler(commands=["start"])
def start(message: types.Message):
    """Функция принимает комманду /start от пользователя и отправляет приветсвие!"""

    text = f"""
    Hello, {message.from_user.username}. I am EchoTelegramBot!
    """

    bot.send_message(chat_id=message.chat.id, text=text)



@bot.message_handler(commands=["help"])
def help(message: types.Message):
    """Функция отвечает на команду /help"""

    text = f"""
    Это телеграм бот сделанный для обучения.
    Он занимается повторением пользователя.

    ID пользователя: {message.from_user.id}
    Время отправки сообщения (по серверу): {datetime.utcfromtimestamp(message.date)}
    Время отправки сообщения: {datetime.now()}
    """

    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(content_types=["text"])
def reply_message(message: types.Message):
    """Функция принимает сообщение от пользователя и переотправляет ему же"""

    text = f"{message.text} 😝😝😝😝"

    bot.reply_to(message=message, text=text)


@bot.message_handler(content_types=["photo"])
def reply_photo(message: types.Message):

    photo_id = message.photo[-1].file_id
    file = bot.get_file(file_id=photo_id)
    file = bot.download_file(file_path=file.file_path)

    # with open(f"{datetime.now()}.jpeg", "wb") as f:
    #     f.write(file)

    with io.BytesIO(initial_bytes=file) as f:
        image = Image.open(fp=f)
        ID = ImageDraw.Draw(im=image)
        ID.text(xy=(20, 20), text=f"~{message.from_user.username}", fill=(0, 0, 0))
        
        with io.BytesIO() as output:
            image.save(output, format="JPEG")
            output.seek(0)
            bot.send_photo(message.chat.id, photo=output)

    


if __name__ == "__main__":
    bot.infinity_polling()