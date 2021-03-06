# @MyShinyRestrant

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import sqlite3
from datetime import datetime

step = {}


def start(bot, update):
    id = update.message.chat_id
    bot.sendMessage(chat_id=id, text='Добро пожаловать в наш ресторан! Чтобы оформить заказ, наберите /order, '
                                     'Чтобы забронировать столик, наберите /book, '
                                     'Чтобы отменить ранее совершенное бронирование, жмите /cancel.')


def order(bot, update):
    id = update.message.chat_id
    bot.sendMessage(chat_id=id, text='Введите номер столика')
    step[id] = 1


def book(bot, update):
    id = update.message.chat_id
    bot.sendMessage(chat_id=id, text='Какой столик выбираем? :)')
    step[id] = 3


def end(bot, update):
    id = update.message.chat_id
    step[id] = 0
    bot.sendMessage(chat_id=id, text='Заказ добавлен!')


def cancel(bot, update):
    id = update.message.chat_id
    bot.sendMessage(chat_id=id, text='Введите номер столика, с которого хотите снять бронь: ')
    step[id] = 4


def texter(bot, update):
    id = update.message.chat_id
    if step.get(id) == 1:
        add_order(bot, id, update.message.text)
    elif step.get(id) == 2:
        add_dishes(bot, id, update.message.text)
    elif step.get(id) == 3:
        add_booking(bot, id, update.message.text)
    elif step.get(id) == 4:
        delete_booking(bot, id, update.message.text)
    else:
        bot.sendMessage(chat_id=id, text='Извините, я не понимаю :)')


def add_order(bot, id, num):
    conn1 = sqlite3.connect('Restaurant.db')
    c1 = conn1.cursor()
    date = str(datetime.now())
    c1.execute("INSERT INTO Заказы (Столик, Дата) VALUES ('%s','%s')" % (num, date))
    c1.execute("SELECT Заказ FROM Заказы WHERE Столик = '%s' AND Дата = '%s'" % (num, date))
    ord = c1.fetchone()
    add_dishes.ord = ord[0]
    conn1.commit()
    c1.close()
    conn1.close()
    bot.sendMessage(chat_id=id, text='Введите блюдо. Когда закончите, введите /end')
    step[id] = 2


def add_dishes(bot, id, dish):
    conn1 = sqlite3.connect('Restaurant.db')
    c1 = conn1.cursor()
    c1.execute("INSERT INTO Заказы_Блюда (Заказ, Блюдо) VALUES ('%s','%s')" % (add_dishes.ord, dish))
    conn1.commit()
    c1.close()
    conn1.close()
    bot.sendMessage(chat_id=id, text='Введите блюдо. Когда закончите, введите /end')


def add_booking(bot, id, num):
    conn1 = sqlite3.connect('Restaurant.db')
    c1 = conn1.cursor()
    date = str(datetime.now())
    c1.execute("INSERT INTO Бронирование (Столик, Дата) VALUES ('%s','%s')" % (num, date))
    conn1.commit()
    c1.close()
    conn1.close()
    bot.sendMessage(chat_id=id, text='Столик забронирован! Если хотите отменить бронирование, нажмите /cancel.')


def delete_booking(bot, id, num):
    conn1 = sqlite3.connect('Restaurant.db')
    c1 = conn1.cursor()
    c1.execute("DELETE FROM Бронирование WHERE Столик = ({})".format(num))
    conn1.commit()
    c1.close()
    conn1.close()
    bot.sendMessage(chat_id=id, text='Столик снова свободен для бронирования!')


def main():
    updater = Updater(token='280940734:AAE3eZ4QFNkyzpM95oCVJZcAy6awwJZlH50')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("order", order))
    dispatcher.add_handler(CommandHandler("end", end))
    dispatcher.add_handler(CommandHandler("book", book))
    dispatcher.add_handler(CommandHandler("cancel", cancel))
    dispatcher.add_handler(MessageHandler(Filters.text, texter))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
