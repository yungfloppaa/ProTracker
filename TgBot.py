import telebot
from telebot import types

bot = telebot.TeleBot('6031419131:AAGJIz5ytYr-FzjbtuQkQa24TXidHHktrzs')

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот по Dota 2",
                     reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться':
        bot.send_message(message.from_user.id, 'Введите свой ник')  # ответ
        username = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Статистика последних игр за 8 дней')
        btn2 = types.KeyboardButton('В разработке')
        btn3 = types.KeyboardButton('В разработке')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, 'Что вы хотите узнать?', reply_markup=markup) #ответ
        # бота


    elif message.text == 'Статистика последних игр за 8 дней':
        bot.send_message(message.from_user.id, 'Вы пишете первый пост, его проверяют модераторы, и, если всё хорошо, отправляют в основную ленту Хабра, где он набирает просмотры, комментарии и рейтинг. В дальнейшем премодерация уже не понадобится. Если с постом что-то не так, вас попросят его доработать.\n \nПолный текст можно прочитать по ' + '[ссылке](https://habr.com/ru/sandbox/start/)', parse_mode='Markdown')

    elif message.text == 'Правила сайта':
        bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/docs/help/rules/)', parse_mode='Markdown')

    elif message.text == 'Советы по оформлению публикации':
        bot.send_message(message.from_user.id, 'Подробно про советы по оформлению публикаций прочитать по ' + '[ссылке](https://habr.com/ru/docs/companies/design/)', parse_mode='Markdown')


bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть