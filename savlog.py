#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from PIL import Image
from datetime import datetime
import urllib.request as req
import argparse
import sys, codecs
import io
import re
import os
import os.path

pageNum = 1


def return_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    request = req.Request(url=url, headers=headers)
    html = req.urlopen(request).read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    return soup


def return_date(url):
    _url = url
    days = []
    soup = return_html(_url)
    entrybottom = soup.find_all('div', class_='entrybottom')
    # get each date
    for day in entrybottom:
        split_word = day.text.split()
        word = split_word[0]
        split_day = word.split('/')
        year = split_day[0]
        month = split_day[1]
        date = year + month
        days.append(date)

    return days  


def return_date2(url):
    _url = url
    days = []
    soup = return_html(_url)
    entrybottom = soup.find_all('div', class_='entrybottom')
    # get each date
    for day in entrybottom:
        split_word = day.text.split()
        word = split_word[0]
        split_day = word.split('/')
        year = split_day[0]
        month = split_day[1]
        day = split_day[2]
        date = year + month + day
        days.append(date)

    return days


def savlog_general(url):
    authors = []
    titles = []

    soup = return_html(url)
    spans = soup.find_all('span', class_ = 'heading')
    for author in spans:
        authors.append(author.find('span', class_ = 'author'))
    for title in spans:
        titles.append(title.find('span', class_ = "entrytitle").find('a'))

    for a in range(len(authors)):
        print ("name is %s and title is %s" % (authors[a].text, titles[a].text))


def savlog_individual(url,member_path):
    titles = []
    bodies = []
    days = []
    images = []
    global pageNum

    # make individual member's folder or change current path to member path
    if not os.path.isdir(member_path):
        os.mkdir(member_path)
        os.chmod(member_path, 0o777)

    soup = return_html(url)

    entrytitle = soup.find_all('span',class_='entrytitle')
    entrybody = soup.find_all('div', class_='entrybody')
    entrybottom = soup.find_all('div', class_='entrybottom')

    # get each blog titles
    for title in entrytitle:
        titles.append(title.find('a'))

    # get each sentences and images
    for body in entrybody:
        sentence = ''
        image = []
        for div in body.find_all('div'):
            sentence += div.text
        bodies.append(sentence)

        for img in body.find_all('img'):
            emoji_remover = re.search(r"gif", img['src'])
            if emoji_remover:
                print("絵文字は嫌い！")
            else:
                image.append(img['src'])
        each_images = '_'.join(image)
        images.append(each_images)

        #print ('images start!!')
        #print (each_images)
        #print ('images finish!!')
    
    # get each date
    for day in entrybottom:
        split_word = day.text.split()
        word = split_word[0]
        split_day = word.split('/')
        date = '_'.join(split_day)
        days.append(date)

    # title matches sentence
    if len(titles) == len(bodies) and len(bodies) == len(days) and len(days) == len(titles):
        os.chdir(member_path)
        for num in range(len(titles)):
            #print (days[num])
            save_path = './' + days[num]
            if not os.path.isdir(save_path):
                os.mkdir(save_path)
                os.chdir(save_path)
            else:
                os.chdir(save_path)
            
            write_file = titles[num].text + '.txt'
            with open(write_file, 'w', encoding='utf-8') as f:
                f.write(bodies[num])
                f.close()
            counter = 1
            if images.count('') > 0:
                pass
            else:
                split_image = images[num].split('_')
                print(split_image)
                for save_image in split_image:
                    #print (save_image)
                    image = req.urlopen(save_image)
                    image_file = 'img' + str(counter) + '.jpg'
                    with open(image_file, 'wb') as f:
                        f.write(image.read())
                        f.close()
                    counter += 1

            os.chdir('../')
            #print (titles[num].text, bodies[num])

    os.chdir('../../')


def next_pages(url, search_url, name, member_path, year, month, date):
    _url = url
    _search_url = search_url
    _name = name
    _member_path = member_path
    _year = year
    _month = month
    _date = date
    global pageNum

    new_name = _name + "/?p=" + str(pageNum) + "&d=" + _date
    nextsearch_url = _url + new_name
    
    # page 2 doesn't exsits
    counter = 0
    days1 = return_date2(_search_url)
    days2 = return_date2(nextsearch_url)
    a = len(days2) if len(days1)>len(days2) else len(days1)
    for i in range(a):
        if days1[i] == days2[i]:
            counter += 1

    if counter == a:
        pageNum = 1
        calculated_month = int(_month) - 1

        # move to previous month
        if calculated_month == 0:
            print ("next is previous year!")
            _year = str(int(_year)-1)
            _month = str(12)
        elif calculated_month < 10:
            print ("previous month!! still continuing!!")
            _month = str(0) + str(calculated_month)
        else:
            print ("previous month")
            _month = str(calculated_month)
        return _year, _month
            
    # page 2 or more exists
    else:
        savlog_individual(nextsearch_url, _member_path)
        pageNum += 1
        return next_pages(_url, _search_url, _name, _member_path, _year, _month, _date)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='save blog data')
    parser.add_argument('--name', '-n', type=str, default='')
    args = parser.parse_args()

    # convert us-ascii to utf-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if os.path.isdir('./members') == False:
        os.mkdir('./members')
        os.chmod('./members', 0o777)

    url = "http://blog.nogizaka46.com/"
    name = ""
    today = datetime.now()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    current_date = year + month
    #date = current_date
    date = str(2012) + str(0) + str(5)

    if args.name == '':
        savlog_general(url)
    else:
        if args.name == "秋元真夏":
            name = "manatsu.akimoto/"
        elif args.name == "生田絵梨花":
            name = "erika.ikuta/"
        elif args.name == "生駒里奈":
            name = "rina.ikoma/"
        elif args.name == "伊藤かりん":
            name = "junna.itou/"
        elif args.name == "伊藤純奈":
            name = "karin.itou/"
        elif args.name == "伊藤万理華":
            name = "marika.ito/"
        elif args.name == "井上小百合":
            name = "sayuri.inoue/"
        elif args.name == "衛藤美彩":
            name = "misa.eto/"
        elif args.name == "川後陽菜":
            name = "hina.kawago/"
        elif args.name == "川村真洋":
            name = "mahiro.kawamura/"
        elif args.name == "北野日奈子":
            name = "hinako.kitano/"
        elif args.name == "齋藤飛鳥":
            name == "asuka.saito/"
        elif args.name == "斎藤ちはる":
            name == "chiharu.saito/"
        elif args.name == "斉藤優里":
            name == "yuuri.saito/"
        elif args.name == "相楽伊織":
            name == "iori.sagara/"
        elif args.name == "桜井玲香":
            name == "reika.sakurai/"
        elif args.name == "佐々木琴子":
            name == "kotoko.sasaki/"
        elif args.name == "白石麻衣":
            name = "mai.shiraishi/"
        elif args.name == "新内眞衣":
            name == "mai.shinuchi/"
        elif args.name == "鈴木絢音":
            name == "ayane.suzuki/"
        elif args.name == "高山一実":
            name == "kazumi.takayama/"
        elif args.name == "寺田蘭世":
            name == "ranze.terada/"
        elif args.name == "中田花奈":
            name == "kana.nakada/"
        elif args.name == "中元日芽香":
            name == "himeka.nakamoto/"
        elif args.name == "西野七瀬":
            name = "nanase.nishino/"
        elif args.name == "能條愛未":
            name == "ami.noujo/"
        elif args.name == "橋本奈々未":
            name == "nanami.hashimoto/"
        elif args.name == "樋口日奈":
            name == "hina.higuchi/"
        elif args.name == "星野みなみ":
            name == "minami.hoshino/"
        elif args.name == "堀未央奈":
            name == "miona.hori/"
        elif args.name == "松村沙友理":
            name == "sayuri.matsumura/"
        elif args.name == "山崎怜奈":
            name == "rena.yamazaki/"
        elif args.name == "若月佑美":
            name == "yumi.wakatsuki/"
        elif args.name == "渡辺みり愛":
            name == "miria.watanabe/"
        elif args.name == "和田まあや":
            name == "maaya.wada/"
        elif args.name == "三期生":
            name == "third/"
        else:
            sys.stderr.write("There is no member! ")

    member_path = './members/' + name
    first_url = url + name
    roop_counter = 1

    while True:
        print ('search date is ' + date)
        counter = 0
        current_url = url + name + "?d=" + date
        roop_counter += 1
        first_url_days = return_date(first_url)
        current_url_days = return_date(current_url)
        for i in range(len(current_url_days)):
            if first_url_days[i] == current_url_days[i]:
                counter += 1

        # this page is the same as first-url's page
        if counter == len(first_url_days) == len(current_url_days):
            counter = 0
            # just in case
            suspicious_month = str(0) + str(int(month)-1)
            if int(month) == 1:
                suspicious_month = str(12)
                suspicious_year = str(int(year)-1)
            else:
                suspicious_month = str(0) + str(int(month)-1)
                suspicious_year = year
            suspicious_date = suspicious_year + suspicious_month
            suspicious_url = url + name + "?d=" + suspicious_date
            suspicious_days = return_date(suspicious_url)
            print ('suspicious date is ' + suspicious_date)
            for i in range(len(suspicious_days)):
                if first_url_days[i] == suspicious_days[i]:
                    counter += 1
            # not updated blog for two conecutive months -> there is no article cuz it is too previous year 
            if counter == len(first_url_days) == len(suspicious_days):
                print ('nothing!!!!')
                break
            else:
                month = suspicious_month
                year = suspicious_year
                date = suspicious_date

        else:
            print ('start')
            #processing when page number is 1
            search_url = url + name + "?d=" + date
            savlog_individual(search_url, member_path)
            pageNum += 1
            print ('pagenum 0 finished!')

            next_year, next_month = next_pages(url, search_url, name, member_path, year, month, date)
            year = next_year
            month = next_month
            date = year + month
            print ('round' + str(roop_counter) + 'finished!!')

    print ('saving is finished!!')
