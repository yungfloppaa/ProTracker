import telebot
import main

from telebot import types

bot = telebot.TeleBot('6031419131:AAGJIz5ytYr-FzjbtuQkQa24TXidHHktrzs')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.from_user.id, f"👋 Привет, {message.from_user.first_name}! Я твой бот "
                                           f"по Dota 2", reply_markup=markup)
    bot.send_message(message.from_user.id, 'Введите ваш ник в Dota 2 прежде чем начать.')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Поменять ник':
        bot.send_message(message.from_user.id, 'Введите ник')
        a = main.ProTracker(message.text)
        bot.send_message(message.from_user.id, f'Ваш ник успешно изменен на {message.text}',
                         parse_mode='Markdown')
    elif message.text == 'Статистика последних игр за 8 дней':
        print(a.lastgames())
        bot.send_message(message.from_user.id, a.lastgames())

    elif message.text == 'В разработке':
        bot.send_message(message.from_user.id,
                         'Подробно про советы по оформлению публикаций прочитать по ' + '[ссылке](https://habr.com/ru/docs/companies/design/)',
                         parse_mode='Markdown')


bot.polling(none_stop=True, interval=0)
