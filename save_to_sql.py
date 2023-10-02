import sqlite3
from operator import itemgetter
import pandas as pd
# from config import price_threshold
# import psycopg2


def add_db(data, total_score, key_words):
    connect = sqlite3.connect('wb.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS wb_item(
        id TEXT,
        name TEXT,
        brand TEXT,
        salePriceU TEXT
)
     """)
    connect.commit()

    perem = data['id']

    cursor.execute('SELECT id FROM wb_item WHERE id = ?', [perem])
    data_test = cursor.fetchone()
    last_price = cursor.execute('SELECT salePriceU FROM wb_item WHERE id = ?', [perem]).fetchone()
    # print(last_price)
    # print(data_test)
    data_discont ={}
    result = ''
    if data_test is None:
        price_threshold = ''
        with open('price.txt', 'r', encoding='utf-8') as f:
            price_threshold = float(f.readline().strip())
        if float(data['salePriceU']) >= price_threshold:
            cursor.execute('INSERT INTO wb_item VALUES (?,?,?,?)', [data['id'], data['name'], data['brand'], data['salePriceU']])
            connect.commit()
            cursor.close()
    else:
        proc = ''
        with open('proc.txt', 'r', encoding='utf-8') as f:
            proc = float(f.readline().strip())

        if float(data['salePriceU'])/float(str(last_price[0])) <= (1 - proc):
            res = (1 - float(data['salePriceU'])/float(str(last_price[0])))*100
            name = data['name']
            id_key = str(data['id'])
            link_item = f'https://www.wildberries.ru/catalog/{id_key}/detail.aspx?targetUrl=SP'
            new_price = data['salePriceU']
            brand = data['brand']
            link = f'<a href="{link_item}">{name}</a>'
            price_threshold = ''
            with open('price.txt', 'r', encoding='utf-8') as f:
                price_threshold = float(f.readline().strip())

            if float(data['salePriceU']) >= price_threshold:
                result = f'{link}\n🆔{id_key}\n=======================\n' \
                         f'💵 Цена ДО {float(last_price[0])/100} руб.\n' \
                         f'💎 Цена ПОСЛЕ {float(new_price/100)} руб.\n' \
                         f'📈 Скидка {round(res, 2)}%\n=======================\n' \
                         f'💼 Бренд: {brand}\n=======================\n' \
                         f'💬 Ключ: {key_words}\n' \
                         f'📦 Всего найдено товаров: {total_score}'

            set_column = f"salePriceU = '{data['salePriceU']}'"
            cursor.execute(f"""UPDATE wb_item SET {set_column} WHERE salePriceU={last_price[0]}""")

            # print(result)
        connect.commit()
        cursor.close()
    return result

def del_table(name_db):
    connect = sqlite3.connect(name_db)
    cursor = connect.cursor()
    cursor.execute("DROP TABLE IF EXISTS wb_item")
    cursor.close()
    return True

def search_db(key):
    connect = sqlite3.connect(key)
    cursor = connect.cursor()
    df = pd.read_sql_query("SELECT * FROM wb_item", connect)
    df.to_excel('all_base.xlsx', index=False)
    cursor.close()












