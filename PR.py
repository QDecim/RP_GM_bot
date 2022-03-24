import sqlite3
import telebot

#   Тестовий
token = "2122500218:AAGtQO1v4crQX44LwNqdRFeBWVDWwfdIZJ0"
#   Актуальний
#token = "5136560642:AAHPSBjR8YJQAh0m6djR1YPfdIwWM1x0kX8"

bot = telebot.TeleBot(token, parse_mode=None)

#import time

#==========================================================================================================
#                                               План:
#==========================================================================================================

# Прогрес написання:  4.5/7 модулів

#   Початок роботи о 9:22 23.03.2022 
#   І. Закінчив о 2:45 24.03.2022
#   ІІ.

#    1. Організація системи командних частин для текстового оформлення РП                                                                                       1 <----------- У ПРОЦЕСІ
#    2. Забезпечення ідентифікації користувачів та введення їх нікнеймів, запис відповідних даних до бд                                                         2 <----------- ЗРОБИВ та ДОРОБИВ
#    3. Створення необхідних виправлень для стилізації тексту                                                                                                   3 <----------- У ПРОЦЕСІ
#    4. Система видалення повідомлення                                                                                                                          4 <----------- ЗРОБИВ та ВИРІШИВ: ПОХУЙ
#    5. Вирішити запитання, як структурувати повідомлення: чи як відповідь до минулих повідомлень, чи як окремі та пофіг                                        5 <----------- ЗРОБИВ
#    6. Якимось хуєм запулити бота на сервер, хоча б на хамачі                                                                                                  6 <-----------
#    7. Додати обмеження. Потрібно зробити так, щоб до відпису ГМа ніхто не міг писати в чат.
# P.S. Взагалі, можна просто видаляти повідомлення, що написані без /b/. Типу, щоб історія не продовжувалась

#==========================================================================================================
#                                               SQLite
#==========================================================================================================

## Создаем соединение с нашей базой данных, у нас это просто файл базы
#conn = sqlite3.connect('Chinook_Sqlite.sqlite')

## Создаем курсор - это специальный объект который делает запросы и получает их результаты
#cursor = conn.cursor()

## Делаем SELECT запрос к базе данных, используя обычный SQL-синтаксис
#cursor.execute("""
#  SELECT name
#  FROM Artist
#  ORDER BY Name LIMIT 3
#""")

## Получаем результат сделанного запроса
#results = cursor.fetchall()

## Делаем INSERT запрос к базе данных, используя обычный SQL-синтаксис
#cursor.execute("insert into Artist values (Null, 'A Aagrh!') ")

## Если мы не просто читаем, но и вносим изменения в базу данных - необходимо сохранить транзакцию
#conn.commit()

## Не забываем закрыть соединение с базой данных
#conn.close()

#==========================================================================================================
#                                             МОДУЛЬ ВИДАЛЕННЯ
#==========================================================================================================
def delete_module(message):

    print("Deleted message id = " + str(message.message_id) + "\n\tText: " + str(message.text) + "\n\n")

    bot.delete_message(message.chat.id, message.message_id, timeout = 1)

#==========================================================================================================
#                                               START MODULE
#==========================================================================================================

@bot.message_handler(commands=['start'])
def message_start(message):

    if message.chat.type == "supergroup":
        bot.send_message(message.chat.id, "Усім привіт")

    if message.chat.type == "private":
        bot.send_message(message.chat.id, "Вибач, та поки я не функціоную у приватних повідомленнях :(")

@bot.message_handler(commands=['new_chat_members', 'help'])
def message_help(message):    
    bot.reply_to(message, "Привіт! Ти потрапив до RP-чату. Будь-ласка, ознайомся з правилами:\nhttps://telegra.ph/Zb%D1%96rnik-prostih-pravil-dlya-troshki-prikoln%D1%96shogo-oformlennya-chatu-03-23")

@bot.message_handler(commands=['testQD'])
def test_module(message):
    pass

#==========================================================================================================
#                                               МОДУЛЬ РЕЄСТРАЦІЇ
#==========================================================================================================

@bot.message_handler(commands=['reg'])
def reg_module(message):

    print("Підключення БД")
    con2BD = sqlite3.connect('sql/UP _ '+ message.chat.title +'.sqlite')
    cursor = con2BD.cursor()

    try:
        cursor.execute("""CREATE TABLE members(
            'user_id' INTEGER NOT NULL PRIMARY KEY,
            'username' STRING,
            'pseudonym' STRING NOT NULL
        )""") 
        print("Створив нову ТАБЛИЦЮ")
    except:
        pass
    
    try:
        cursor.execute(f"INSERT into members (user_id, username, pseudonym) values ({message.from_user.id}, '{message.from_user.username}', '{message.text[4::]}'); ")
        bot.reply_to(message, f"Вітаю, {message.text[4::]}, я тебе запам'ятав :3")
        con2BD.commit()    
    except sqlite3.DatabaseError as err: 
        print("\t---> Error: ", err)

        cursor.execute("""
            SELECT user_id, username, pseudonym
            FROM members
            ORDER BY user_id
        """)
        rows = cursor.fetchall()

        for row in rows:        
            if message.from_user.id == row[0]:
                bot.reply_to(message, f"Ви вже зареєстровані, як {row[2]}. \nЯ перейменував вас, як {message.text[4::]}. \n\nСподіваюсь, що тепер ви задоволені...")
                cursor.execute(f"DELETE FROM members WHERE user_id = '{row[0]}';")

        con2BD.commit()    

        cursor.execute(f"INSERT into members (user_id, username, pseudonym) values ({message.from_user.id}, '{message.from_user.username}', '{message.text[4::]}'); ")      

        con2BD.commit()

        cursor.execute("""
          SELECT user_id, username, pseudonym
          FROM members
          ORDER BY user_id
        """)
        rows = cursor.fetchall()

        for row in rows:        
           if message.from_user.id == row[0]:
                print(f"\t {message.from_user.username} -----> {row[2]}")

    con2BD.close()

#==========================================================================================================
#                                             МОДУЛЬ ЗМІСТУ <-------------------Треба зробити стоп для підсумків ГМа-----------------------
#==========================================================================================================

@bot.message_handler(commands=['end'])
def modulEndPart(message):

    bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    limited_there = message.reply_to_message.message_id + 1

    while True:
        bot.delete_message(message.chat.id, limited_there, timeout = 1)

        if ...:
            pass

#==========================================================================================================
#                                               МОДУЛЬ ДІЙ
#==========================================================================================================
    
@bot.message_handler(commands=['d'])
def action(message):
    
    print("Підключення БД")
    con2BD = sqlite3.connect('sql/UP _ '+ message.chat.title +'.sqlite')
    cursor = con2BD.cursor()

    try:
        cursor.execute("""
            SELECT user_id, username, pseudonym
            FROM members
            ORDER BY user_id
            """)
        rows = cursor.fetchall()

        print("-> Хтось виконує дію")
        for row in rows:        
            if message.from_user.id == row[0]:
                pseudonym = row[2]

        text = message.text[2::]
        bot.send_message(message.chat.id, f"{pseudonym}" + text)
        delete_module(message)

    except sqlite3.DatabaseError as err:
        bot.reply_to(message, "Я ще не знаю, хто ти такий. Відрекомендуй себе командою /reg <твій псевдонім чи ім'я>")
    
    con2BD.close()


#==========================================================================================================
#                                             МОДУЛЬ МОДЕРАЦІЇ <---------------------------------------------------------
#==========================================================================================================

@bot.message_handler(commands=['ban'])
def ban_module(message):
    pass

#==========================================================================================================
#                                             ПУЛІНГ СЕРВЕРІВ
#==========================================================================================================

bot.polling(interval = 5)


