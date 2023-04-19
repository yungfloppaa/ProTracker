import requests
from bs4 import BeautifulSoup as b

username = str(input())
r = requests.get(f'https://www.dota2protracker.com/player/{username}')
soup = b(r.text, 'html.parser')
kk = soup.find_all(class_='played-box')
games = soup.find_all(class_='yellow')
try:
    games_last_8_days = str(games[0])[21:23].rstrip('<')
except IndexError:
    print('Нет профиля')
    games_last_8_days = 'Ошибка: нет профиля на Dota2protracker'
well = []
for el in kk:
    well.append(str(el).strip('\n').split(' '))
heroes = []
hero = []
winrate = []
for i in well:
    for el in i:
        if 'class="green"' in str(el):
            winrate.append(el[14:19].rstrip('%'))
        elif 'class="yellow"' in str(el):
            winrate.append(el[15:20].rstrip('%'))
        elif 'class="red"' in str(el):
            winrate.append(el[12:17].rstrip('<').rstrip('%'))

for i in well:
    for el in i:
        if 'data=' in el:
            heroes.append(el[6:])

for el in heroes:
    a = str(el).find('"')
    if a != -1:
        hero.append(el[:a])
    elif a == -1:
        hero.append(el)
all = []
print(winrate)
print(hero)
for i in range(len(hero)):
    aa = f'{hero[i]}: {winrate[i]}%'
    all.append(aa)
print(f'Last games per 8 days: ({games_last_8_days} games)')
for el in all:
    print(el)