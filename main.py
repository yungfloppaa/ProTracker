import requests
from bs4 import BeautifulSoup as b
import telebot

from telebot import types


class ProTracker:
    def __init__(self, nickname):
        self.l = f'https://www.dota2protracker.com/player/{nickname}'
        r = requests.get(self.l)  # создание
        # ссылки на
        soup = b(r.text, 'html.parser')  # вся инфа с профиля
        self.replay = soup.find_all(class_='copy-id')[:3]
        self.kk = soup.find_all(class_='played-box')  # по классам беру инфу с сайта(псоледние игры,
        # сыгранные за 8 дней)
        self.games = soup.find_all(class_='yellow')  # сколько игр было сырано за последние 8 дней
        # сколько игр
        # был
        # сыгранно за
        # последние 8 дней(преобразованное в одно число)
        self.las = soup.find_all(class_='row-0')  # пепрвая игра, со всеми данными, персонаж, роль,
        # итог игры, тиммейты, оппоненты, айтембилд
        self.priveou = soup.find_all(class_='row-1')  # вторая игра, со всеми данными, персонаж,
        # роль, итог игры, тиммейты, оппоненты, айтембилд
        self.prepreviou = soup.find_all(class_='row-2')  # третья игра, со всеми данными, персонаж,
        # роль, итог игры, тиммейты, оппоненты, айтембилд
        self.mmr = soup.find_all(class_='td-mmr')[:3]  # ммр в этих трех играх

    def lastgames(self):
        # games_last_8_days = str(self.games[0])[21:23].rstrip('<')
        well = []
        for el in self.kk:
            well.append(str(el).strip('\n').split(' '))  # все данные из вкладки о последних играх
        heroes = []
        hero = []
        winrate = []
        for i in well:
            for el in i:
                if 'class="green"' in str(el):
                    winrate.append(el[14:19].rstrip('%'))  # винрейт
                elif 'class="yellow"' in str(el):
                    winrate.append(el[15:20].rstrip('%'))  # винрейт
                elif 'class="red"' in str(el):
                    winrate.append(el[12:17].rstrip('<').rstrip('%'))  # винрейт

        for i in well:
            for el in i:
                if 'data=' in el:
                    heroes.append(el[6:])  # ввсе герое, на которых игрок играл за последние 8 дней

        for el in heroes:
            a = str(el).find('"')
            if a != -1:
                hero.append(el[:a])  # отладка
            elif a == -1:
                hero.append(el)
        all = []
        # all.append(f'Всего игр за 8 дней: {games_last_8_days}')
        for i in range(len(hero)):
            aa = f'{hero[i]}: {winrate[i]}%'  # преобразование списка в формате "Герой: винрейт"
            all.append(aa)
        return '\n'.join(all)

    def last3matches(self):
        mmrs = []
        replays = []
        last = []
        priveous = []
        prepriveous = []
        for el in self.replay:
            replays.append(str(el)[25:35])
        for el in self.mmr:
            mmrs.append(str(el)[
                        19:23])  # преобразовал ммр с список, нулевой индекс - последняя игра, индекс 2 - третья игра с конца
        for el in self.las:
            last.append(str(el).split('\n'))  # данные с последней последней игры
        for el in self.priveou:
            priveous.append(str(el).split('\n'))  # данные с предпоследней игры
        for el in self.prepreviou:
            prepriveous.append(str(el).split('\n'))  # данные с предпредпоследней игры
        last = (last[0][0].split('"'))[2:]  # срез данных по последней игре, с нужными данными
        priveous = (priveous[0][0].split('"'))[2:]  # срез данных по предпоследней игре, с нужными
        # данными
        prepriveous = (prepriveous[0][0].split('"'))[2:]  # срез данных по предпредпоследней игре,
        # с нужными данными
        last_info = []
        priveous_info = []
        prepriveous_info = []
        for i in range(1, 18, 2):
            last_info.append(last[i])
        for i in range(1, 18, 2):
            priveous_info.append(priveous[i])
        for i in range(1, 18, 2):
            prepriveous_info.append(prepriveous[i])
        return (f'---------------------------------------- \n'
                f"1st game played on the {last_info[0]} ({last_info[6]}) \n"
                f'Replay: {replays[0]} \n'
                f'Average mmr: {mmrs[0]} \n'
                f'Item build(in order): {last_info[2].replace(",", ", ")} \n'
                f"Player's team: {last_info[7]} \n"
                f"Enemy Team: {last_info[4]} \n"
                f"Famous people: {last_info[5]} \n"
                f"Result: {'win' if int(priveous_info[8]) == 1 else 'lose'} \n"
                f'---------------------------------------- \n'
                f"2nd game played on the {priveous_info[0]} ({priveous_info[6]}) \n"
                f'Replay: {replays[1]} \n'
                f'Average mmr: {mmrs[1]} \n'
                f'Item build(in order): {priveous_info[2].replace(",", ", ")} \n'
                f"Player's team: {priveous_info[7]} \n"
                f"Enemy Team: {priveous_info[4]} \n"
                f"Famous people: {priveous_info[5]} \n"
                f"Result: {'win' if int(priveous_info[8]) == 1 else 'lose'} \n"
                f'---------------------------------------- \n'
                f"3rd game played on the {prepriveous_info[0]} ({prepriveous_info[6]}) \n"
                f'Replay: {replays[2]} \n'
                f'Average mmr: {mmrs[2]} \n'
                f'Item build(in order): {prepriveous_info[2].replace(",", ", ")} \n'
                f"Player's team: {prepriveous_info[7]} \n"
                f"Enemy Team: {prepriveous_info[4]} \n"
                f"Famous people: {prepriveous_info[5]}\n"
                f"Result: {'win' if int(prepriveous_info[8]) == 1 else 'lose'} \n"
                f'----------------------------------------')

    def top_heroes(self):
        r = requests.get('https://www.dota2protracker.com')
        soup = b(r.text, 'html.parser')
        results_all = str(soup.find_all(class_='td-hero-pic')[:3])
        first = str(results_all).split('\n')[3].strip(' ')
        second = str(results_all).split('\n')[8].strip(' ')
        third = str(results_all).split('\n')[13].strip(' ')
        games = str(soup.find_all(class_='perc-wr')[:6]).split(' ')
        game = []
        winrrate = []
        for i in range(2, 15, 5):
            if 'red' in games[i]:
                winrrate.append(str(games[i][12:17]))
            else:
                winrrate.append(str(games[i][14:19]))
        for i in range(4, 15, 5):
            game.append(str(games[i][16:20]))

        return (f'The Most Popular Heroes:\n'
                f'{first} - {game[0]} ({winrrate[0]}) \n'
                f'{second} - {game[1]} ({winrrate[1]}) \n'
                f'{third} - {game[2]} ({winrrate[2]})')

    def topstreamers(self):
        r = requests.get('https://www.dota2protracker.com')
        soup = b(r.text, 'html.parser')
        topstreamers = []
        for i in range(3):
            results_all = str(soup.find_all(class_='twitch-streamer')[i])
            n = results_all.split()[5]
            n = n[n.index('"') + 1: n.index('>') - 2]
            f = results_all.split()[12]
            f = f[f.index('>') + 1: f.index('<')]
            a = results_all.split()[5]
            a = a[a.index('>') + 1: a.index('<')]
            topstreamers.append(f'Стример: {a}, имеет {f} ммр, Ссылка на твич: {n}')
        return '\n'.join(topstreamers)


bot = telebot.TeleBot('6031419131:AAGJIz5ytYr-FzjbtuQkQa24TXidHHktrzs')
a = None
c = None


@bot.message_handler(commands=['start'])
def start(message):
    global a
    global c
    a = None
    c = None
    bot.send_message(message.from_user.id, f"👋 Привет, {message.from_user.first_name}! Я твой бот "
                                           f"по Dota 2", reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.from_user.id, 'Введите ник что бы начать')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Статистика последних игр за 8 дней')
    btn2 = types.KeyboardButton('Подробный разбор последних 3-х игр')
    btn3 = types.KeyboardButton('Поменять ник (В разработке)')
    btn4 = types.KeyboardButton('Профиль на Dota2ProTracker')
    btn5 = types.KeyboardButton('3 самых популярных героев среди про-игроков')
    btn6 = types.KeyboardButton('3 хай-ммр стримера, которые ведут стрим')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    global a
    global c
    if a is None:
        a = message.text
        c = ProTracker(a)
        bot.send_message(message.from_user.id, f'Ваш ник: {message.text}', reply_markup=markup)
    if message.text == 'Поменять ник (В разработке)':
        bot.send_message(message.from_user.id, 'Введите ник')
        message.text = ''
        while message.text == '':
            pass
        else:
            a = message.text
            c = ProTracker(a)
            bot.send_message(message.from_user.id, f'Ваш ник успешно изменен на'
                                                   f' {a}',
                             parse_mode='Markdown')
    elif message.text == 'Статистика последних игр за 8 дней':
        bot.send_message(message.from_user.id, c.lastgames())
    elif message.text == 'Подробный разбор последних 3-х игр':
        bot.send_message(message.from_user.id, c.last3matches())
    elif message.text == 'Профиль на Dota2ProTracker':
        bot.send_message(message.from_user.id, c.l)
    elif message.text == '3 самых популярных героев среди про-игроков':
        bot.send_message(message.from_user.id, c.top_heroes())
    elif message.text == '3 хай-ммр стримера, которые ведут стрим':
        bot.send_message(message.from_user.id, c.topstreamers())
    elif message.text == 'В разработке':
        bot.send_message(message.from_user.id,
                         'В разработке',
                         parse_mode='Markdown')
    bot.send_message(message.from_user.id, 'Что вы хотите узнать?')


bot.polling(none_stop=True, interval=0)
