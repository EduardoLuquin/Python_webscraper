# -*- coding: UTF8 -*-
import requests
import datetime

from scraper import check_price


class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30): #Timer set in seconds
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = '1476961985:AAHzrrvQ9UbA6V55cZ2P5cfJpDzjZ0plSdM' #Token of your bot
magnito_bot = BotHandler(token) #Your bot's name

def main_TelegramBot():
    new_offset = 0
    print('Ejecutando TelegramBot')
   
    while True:
        all_updates = magnito_bot.get_updates(new_offset)

        if len(all_updates) > 0:
            print("Dentro Primer if ",all_updates)
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']
                if 'text' not in current_update['message']:
                    first_chat_text = 'New member'
                else:
                    first_chat_text = current_update['message']['text']
                    first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                elif 'new_chat_member' in current_update['message']:
                    first_chat_name = current_update['message']['new_chat_member']['username']
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                else:
                    first_chat_name = "unknown"

                if first_chat_text == 'Item:':
                    check_price()
                    magnito_bot.send_message(first_chat_id, 'Searching your Item ' + first_chat_name)
                    new_offset = first_update_id + 1
                elif first_chat_text == 'Exit:':
                    magnito_bot.send_message(first_chat_id, 'El script se ha detenido')
                    new_offset = first_update_id + 1
                    exit()
                else:
                    magnito_bot.send_message(first_chat_id, 'Escribe la URL de Item para monitorear   Item: <Nombre de tu item>' + first_chat_name)
                    new_offset = first_update_id + 1


#if __name__ == '__main__':
#    try:
#        main_TelegramBot()
#    except KeyboardInterrupt:
#        exit()