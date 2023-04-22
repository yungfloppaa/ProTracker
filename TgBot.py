import telebot
import main

from telebot import types



class Telebot:
    def __init__(self):
        self.a = ''
        self.bot = telebot.TeleBot('6031419131:AAGJIz5ytYr-FzjbtuQkQa24TXidHHktrzs')

        @self.bot.message_handler(commands=['start'])
        def start(self, message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            self.bot.send_message(message.from_user.id,
                                  f"👋 Привет, {message.from_user.first_name}! Я твой бот "
                                  f"по Dota 2", reply_markup=markup)
            self.bot.send_message(message.from_user.id, 'Введите "Поменять ник" прежде чем начать')

        @self.bot.message_handler(content_types=['text'])
        def get_text_messages(self, message):
            if message.text == 'Поменять ник':
                message.text = None
                self.bot.send_message(message.from_user.id, 'Введите ник')
                while message.text is None:
                    print(message.text)
                    pass
                print(message.text)
                self.a = main.ProTracker(message.text)
                self.bot.send_message(message.from_user.id, f'Ваш ник успешно изменен на'
                                                            f' {message.text}',
                                      parse_mode='Markdown')
            elif message.text == 'Статистика последних игр за 8 дней':
                print(self.a.lastgames())
                self.bot.send_message(message.from_user.id, self.a.lastgames())

            elif message.text == 'В разработке':
                self.bot.send_message(message.from_user.id,
                                      'В разработке',
                                      parse_mode='Markdown')

        self.bot.polling(none_stop=True, interval=0)
Telebot()

