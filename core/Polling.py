import sys
from time import sleep
from requests import get
from requests.exceptions import *
from core.System import Bot
from dotenv import dotenv_values

token_bot = dotenv_values()['TOKEN_BOT']


# Выполняю бесконечный цикл, в котором бот получает новые смс от пользователей и отправляет их на обработку в Bot()
def Polling():
    api = "https://api.telegram.org/bot" + token_bot + "/"
    update_id = 0
    print("Бот активирован")
    print("Нажми CTRL + C для выхода")
    while True:
        try:
            req = get(f"https://api.telegram.org/bot{token_bot}/getupdates", params={"offset": update_id}).json()
            if len(req['result']) == 0:
                continue
            update = req["result"][0]
            Bot(update)
            update_id = update['update_id'] + 1
            print("-"*40)
        except ConnectionError:
            print('- ошибка соединения! повторите попытку через 5 секунд!')
            sleep(5)
            continue
        except KeyboardInterrupt:
            sys.exit()
