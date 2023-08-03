import hashlib
from langdetect import detect
from bs4 import BeautifulSoup
import requests
import datetime
import re
import json


def ScrapKompas(url: str):
    '''Input berupa string dan akan menghasilkan hasil file berformat JSON'''
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36'}

    link = f"{url}?page=all"

    req = requests.get(link, headers=user_agent)

    datas = BeautifulSoup(req.text, 'html.parser')

    items, __content, __hashtags = datas.find_all(
        'div', 'content_article'), datas.find_all('div', 'read__content'), datas.find_all('ul', 'mob-tagging__items')

    def cleanUniqcode(text):
        pattern = r'[^\x00-\x7F]+'
        return re.sub(pattern, 'a', text)

    listLink = link.split('/')
    for item in items:
        # hype tag
        hypeTag = ''.join(
            item.find('div', 'exp-tag-populer').div.text.split('\n'))

        # image
        image = item.find(
            'div', 'imgHL').div.img['src']

        # source
        source = item.find('div', 'read__date').a.text

        # time
        try:
            __hour = int(listLink[8][:2])
            __minute = int(listLink[8][2:4])
            __second = int(listLink[8][4:6])
            __year = int(listLink[5])
            __mounth = int(listLink[6][1])
            __date = int(listLink[7])
        except:
            __hour = int(listLink[7][:2])
            __minute = int(listLink[7][2:4])
            __second = int(listLink[7][4:6])
            __year = int(listLink[4])
            __mounth = int(listLink[5][1])
            __date = int(listLink[6])

        # pub_hour
        pub_hour = ''.join(
            str(datetime.date(__year, __mounth, __date)).split('-'))

        # pub_minute
        pub_minute = f'{pub_hour}' + \
            ''.join(str(datetime.time(__hour, __minute)).split(':')[:-1])

        # pub_year
        pub_year = __year

        # pub_day
        pub_day = str(datetime.datetime(__year, __mounth, __date).strftime('%A').replace('Sunday', 'Minggu').replace('Monday', 'Senin').replace(
            'Tuesday', 'Selasa').replace('Wednesday', 'Rabu').replace('Thursday', 'Kamis').replace('Friday', 'Jumat').replace('Saturday', 'Sabtu'))

        # created_at
        created_at = str(datetime.datetime(
            __year, __mounth, __date, __hour, __minute, __second))

        # title
        title = item.find('h1', 'read__title').text

        # editor
        editor = item.find('h6', {'id': 'editor'}).a.text

        # author
        try:
            author = item.find('div', 'read__credit__logo').a.text
        except:
            author = item.find('h6', {'id': 'penulis'}).a.text
        # time_zone
        time_zone = str(datetime.datetime(__year, __mounth, __date,
                        __hour, __minute, __second).astimezone())[-6:]

    # hashtags
    htag = []
    for hashtag in __hashtags:
        hashtaggg = hashtag.find_all('a')
        for h in hashtaggg:
            htag.append('#' + h.text)
    hashtags = htag

    # content
    konten = []
    for cont in __content:
        _cont = cont.find_all('p')
        for c in _cont:
            strong_tags = c.find_all('strong')
            for strong_tag in strong_tags:
                strong_tag.string = ''
            konten.append(''.join(c.find_all(string=True)))
    content_cleaned = [cleanUniqcode(paragraph)
                       for paragraph in konten]
    if content_cleaned[0][:3] == ' - ':
        content = ''.join(content_cleaned)[3:]
    elif content_cleaned[0][:2] == ' -' or content_cleaned[0][:2] == '- ':
        content = ''.join(content_cleaned)[2:]
    elif content_cleaned[0][0] == ' ':
        content = ''.join(content_cleaned)[1:]
    else:
        content = ''.join(content_cleaned)

    # id
    id = str(hashlib.md5(link.encode()).hexdigest())

    # language
    lang = str(detect(datas.get_text()))

    # crawling date
    crawlingDate = str(datetime.datetime.now())

    # description
    desc = '{0}{1}'.format(content[:100], '...')

    # Menambahkan data dict ke datas
    datas = {
        "hashtags": hashtags,
        "pub_hour": pub_hour,
        "link": link,
        "created_at": created_at,
        "source": source,
        "title": title,
        "content": content,
        "pub_minute": pub_minute,
        "pub_year": pub_year,
        "id": id,
        "lang": lang,
        "image": image,
        "editor": editor,
        "author": author,
        "pub_day": pub_day,
        "time_zone": time_zone,
        "crawlingDate": crawlingDate,
        "desc": desc
    }
    # Menkonversi daftar dict menjadi string berformat JSON
    jsons = json.dumps(datas)

    # Membuka dan menulis file
    try:
        with open('kompas.json', 'w') as file:
            file.write(jsons)
    except:
        with open('kompas.json', 'r+') as file:
            file.write(jsons)
