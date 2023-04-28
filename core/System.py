# import json
# from requests import *
from lib import downloader
from datetime import datetime
from dotenv import dotenv_values
from module.messageText import *
from lib.sendVideo import sendVideo
from lib.sendMessage import sendMessage

token_bot = dotenv_values()['TOKEN_BOT']


# Эта функция для вывода даты и времени в консоль разработчика, когда пользователь отправил сообщение/ссылку.
def get_time(tt):
    ttime = datetime.fromtimestamp(tt)
    return f"{ttime.day}.{ttime.month}.{ttime.year} {ttime.hour}:{ttime.minute}:{ttime.second}"


# Функция обработки сообщений от бота Telegram
def Bot(update):
    try:
        # Если сообщение является обратным вызовом (callback), то она извлекает информацию об идентификаторе
        # пользователя, имени пользователя, сообщении, идентификаторе сообщения и времени сообщения.
        if 'callback_query' in str(update):
            userid = update['callback_query']['from']['id']
            first_name = update['callback_query']['from']['first_name']
            meseg = update['callback_query']['data']
            msgid = update['callback_query']['message']['message_id']
            timee = update['callback_query']['message']['date']
            tipeChat = update['callback_query']['message']['chat']['type']
        # В противном случае она извлекает информацию о том же самом, но от обычного сообщения.
        else:
            userid = update['message']['chat']['id']
            meseg = update['message']['text']
            msgid = update['message']['message_id']
            timee = update['message']['date']
            first_name = update['message']['chat']['first_name']
            tipeChat = update['message']['chat']['type']
        # Затем функция использует модуль downloader для загрузки видео из TikTok, если сообщение содержит ссылку на
        # видео TikTok. Если загрузка видео прошла успешно, функция отправляет видео пользователю в чате Telegram.
        dl = downloader.tiktok_downloader()
        if tipeChat != "private":
            sendMessage(userid, privateText, msgid)
            return
        print(f"{get_time(timee)} -> {userid} - {first_name} -> {meseg}")
        # Если сообщение начинается с команды /start, то функция отправляет сообщение со стартовым текстом.
        if meseg.startswith('/start'):
            sendMessage(chat_id=userid, message=startText, message_id=msgid)
        # Проверяет, содержит ли сообщение ссылку на видео TikTok. Если сообщение содержит ссылку на видео TikTok,
        # то функция использует модуль downloader для загрузки видео.
        elif "tiktok.com" in meseg and "https://" in meseg:
            # Метод 'musicaldown' модуля 'downloader' принимает URL-адрес видео TikTok в качестве аргумента и
            # загружает видео, сохраняя его под именем 'video.mp4'.
            sendMessage(userid, waitText, 0)
            getvid = dl.musicaldown(url=meseg, output_name="video.mp4")
            # Затем функция проверяет, успешно ли было загружено видео. Если загрузка прошла успешно, то функция
            # отправляет видео пользователю в чате Telegram с помощью метода 'sendVideo'.
            if getvid:
                sendVideo(chat_id=userid, video="video.mp4",
                          caption=videoText, message_id=msgid)
                return
            # Иначе функция отправляет сообщение пользователю, указывая на неудачу загрузки с помощью метода sendMessage
            else:
                sendMessage(userid, failedText, msgid)
                return
            # os.remove('video.mp4')
        # Если сообщение содержит команду /help, то функция отправляет сообщение со справкой.
        elif "/help" in meseg:
            sendMessage(
                userid, helpText, msgid)
        # Если сообщение начинается с команды /donation, то функция отправляет сообщение с информацией о пожертвованиях.
        elif meseg.startswith("/donation"):
            sendMessage(userid, donationText, msgid)
            return
        else:
            sendMessage(userid, errorText, 0, 'error.jpg')
    # Если во время выполнения возникает исключение KeyError,
    # то функция записывает информацию об ошибке в лог-файл и завершает работу.
    except KeyError as e:
        print(f"- {e}")
        open(".log", "a+", encoding="utf-8").write(str(update) + "\n")
        return
