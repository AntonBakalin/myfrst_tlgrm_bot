import requests
from bs4 import BeautifulSoup as bs
import json
import os


def getURLlist():
    search_strings = [
        'амплификатор',
        'оборудование+для+ПЦР',
        'процессор+магнитных+частиц',
        'станция+пробоподготовки',
        'выделения+нуклеиновых+кислот'
    ]
    url_list = []
    for search_string in search_strings:
        page_num = 1
        url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?'
        params = [
            'searchString={}'.format(search_string),
            'morphology=on',
            'search-filter=Дате+размещения',
            'pageNumber={}'.format(page_num),
            'sortDirection=false',
            'recordsPerPage=_50',
            'showLotsInfoHidden=false',
            'sortBy=PUBLISH_DATE',
            'fz44=on',
            'fz223=on',
            'af=on',
            'currencyIdGeneral=-1'
        ]
        url = url + '&'.join(params)
        url_list.append(url)
    return url_list


makeFullURL = (lambda string: string if string.startswith('http') else 'https://zakupki.gov.ru' + string)

retURL = (lambda url, text: '[{}]({})'.format(text, url))


def getLots(url_list):
    for url in url_list:
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

        data = requests.get(url, headers=headers).text
        reader = bs(data).find_all('div', 'row no-gutters registry-entry__form mr-0')

        purchases = {}

        for div in reader:
            lot_num = div.find_all('a')[2].text.strip()  # Текст ссылки на лот
            lot_url = makeFullURL(div.find_all('a')[2].get('href'))  # Достать ссылку на лот
            lot_descr = ''.join(filter(str.isprintable,
                                       div.find('div', 'registry-entry__body-value').text))  # Описание торгов
            purchases[lot_num] = {'url': lot_url, 'lot_descr': lot_descr}
    return purchases


def storeData(lots):
    with open('prev_data.json', 'w', encoding='utf-8') as storage:
        json.dump(lots, storage)


def checkDiff(lots):
    if os.path.exists('prev_data.json'):
        answer = []
        with open('prev_data.json', 'r', encoding='utf-8') as storage:
            prev = json.load(storage)
            for elem in lots.items():
                if elem[0] not in prev.keys():
                    answer.append(retURL(elem[1]['url'], elem[0])
                                  + ' ' + elem[1]['lot_descr']
                                  )
            return '\n'.join(answer)


def retDataFromStorage():
    answer = []
    with open('prev_data.json', 'r', encoding='utf-8') as storage:
        prev = json.load(storage)
        for elem in prev.items():
            answer.append(retURL(elem[1]['url'], elem[0])
                          + ' ' + elem[1]['lot_descr']
                          )
    return '\n'.join(answer)


def storeUsers(data):
    file = 'users.json'
    with open(file, 'w') as f:
        json.dump(data, f)


def readUsers():
    file = 'users.json'
    with open(file, 'r+', encoding='utf-8') as f:
        f_data = f.read()
        j_data = json.loads(f_data)
        return j_data


def addUser(user):
    users = readUsers()
    user = str(user)
    users['users'][user] = []
    storeUsers(users)


def delUser(user):
    users = readUsers()
    user = str(user)
    if user in users['users']:
        users['users'].pop(user)
    else:
        pass
    storeUsers(users)