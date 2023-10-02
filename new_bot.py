import time
import os
import requests
import telebot
import json
from telebot import types
import pandas as pd
from config import TOKEN, TOKEN_ADMIN, admin_id, group_id, paus  #******************Ваш токен**************
import openpyxl
import save_to_sql
import threading


headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9,ru-RU;q=0.8,en-US;q=0.7',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wildberries.ru',
    'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
bot = telebot.TeleBot(TOKEN_ADMIN)



def admin_panel():
    @bot.message_handler(commands=['start'])
    def start_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Обновить список ключевых слов')
        itembtn2 = types.KeyboardButton('Изменить процент скидки')
        itembtn3 = types.KeyboardButton('Выгрузить всю базу в Excel')
        itembtn4 = types.KeyboardButton('Обновить порог цены')
        itembtn5 = types.KeyboardButton('Удалить базу данных')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
        bot.send_message(message.chat.id,
                         text=f"Здравствуйте, {message.from_user.first_name.format(message.from_user)}, бот предназначен для поиска товара на WildBerries по ключевому слову.\nВыберете пункт меню⤵⤵⤵️️",
                         parse_mode='HTML', reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def commands(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Обновить список ключевых слов')
        itembtn2 = types.KeyboardButton('Изменить процент скидки')
        itembtn3 = types.KeyboardButton('Выгрузить всю базу в Excel')
        itembtn4 = types.KeyboardButton('Обновить порог цены')
        itembtn5 = types.KeyboardButton('Удалить базу данных')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
        if message.text == "Обновить список ключевых слов":
            bot.send_message(message.chat.id, text=f"{message.from_user.first_name.format(message.from_user)},  введите /word и список ключевых слов через запятую\nНапример\n/word смартфоны, очки, галстуки", reply_markup=markup)
        elif message.text == "Выгрузить всю базу в Excel":
            df_all = []
            lst = save_to_sql.search_db('wb.db')
            bot.send_document(message.chat.id, open(f"./all_base.xlsx", 'rb'), caption='Выгрузили всю базу в эксель')
        elif message.text =="Изменить процент скидки":
            bot.send_message(message.chat.id, text=f"{message.from_user.first_name.format(message.from_user)},  введите /proc и процент скидки\nНапример\n/proc 30", reply_markup=markup)
        elif message.text == "Обновить порог цены":
            bot.send_message(message.chat.id,
                              text=f"{message.from_user.first_name.format(message.from_user)},  введите /price и и порог цены в рублях\nНапример\n/price 1000",
                              reply_markup=markup)
        elif '/price' in message.text:
            text = message.text
            text = float(text.lstrip('/price').strip())
            print(text)

            text = float(text) * 100.0
            print(text)
            with open('price.txt', 'w', encoding='utf-8') as f:
                f.write(str(text))
                bot.send_message(chat_id=message.chat.id, text='Порог цены обновлен!')
        elif '/proc' in message.text:
            text = message.text
            text = float(text.lstrip('/proc').strip())
            print(text)

            text = float(text)/100.0
            print(text)
            with open('proc.txt', 'w', encoding='utf-8') as f:
                f.write(str(text))
                bot.send_message(chat_id=message.chat.id, text='Процент скидки обновлен!')
        elif message.text == "Удалить базу данных":
            path = 'wb.db'
            os.remove(path)
            # save_to_sql.del_table('wb.db')
            bot.send_message(chat_id=message.chat.id, text='База данных успешно удалена!')
        elif '/word' in message.text:
            text = message.text
            text = text.lstrip('/word').strip()
            with open('key_words.txt', 'w', encoding='utf-8') as f:
                f.write(text)
                bot.send_message(chat_id=message.chat.id, text='Список ключевых слов обновлен!')

    bot.polling(none_stop=True)

def main():
    admin_panel()


if __name__ == '__main__':
    main()
