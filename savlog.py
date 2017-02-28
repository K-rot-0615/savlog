#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request as req
import argparse
import sys, codecs
import io
import os
import os.path

pageNum = 0

def savlog_general(url):
    authors = []
    titles = []

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    headers = {"User-Agent": "Mozilla/5.0"}
    request = req.Request(url=url, headers=headers)
    html = req.urlopen(request).read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')

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
    global pageNum

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    headers = {"User-Agent": "Mozilla/5.0"}
    request = req.Request(url=url, headers=headers)
    html = req.urlopen(request).read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')

    entrytitle = soup.find_all('span',class_='entrytitle')
    entrybody = soup.find_all('div', class_='entrybody')

    for title in entrytitle:
        titles.append(title.find('a'))

    for body in entrybody:
        sentence = ''
        for one_sentence in body.find_all('div'):
            sentence += one_sentence.text
        bodies.append(sentence)

    if os.path.isdir(member_path) == False:
        os.mkdir(member_path)

    if len(titles) == len(bodies):
        for num in range(len(titles)):
            print ("title is %s and content is %s" % (titles[num].text, bodies[num]))
        pageNum += 1
    else:
        pass


def return_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    request = req.Request(url=url, headers=headers)
    html = req.urlopen(request).read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    return soup


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='save blog data')
    parser.add_argument('--name', '-n', type=str, default='')
    args = parser.parse_args()

    url = "http://blog.nogizaka46.com/"

    if args.name == '':
        savlog_general(url)
    else:
        if args.name == "秋元真夏":
            name = "manatsu.akimoto"
        elif args.name == "生田絵梨花":
            name = "erika.ikuta"
        elif args.name == "生駒里奈":
            name = "rina.ikoma"
        elif args.name == "伊藤かりん":
            name = "junna.itou"
        elif args.name == "伊藤純奈":
            name = "karin.itou"
        elif args.name == "伊藤万理華":
            name = "marika.ito"
        elif args.name == "井上小百合":
            name = "sayuri.inoue"
        elif args.name == "衛藤美彩":
            name = "misa.eto"
        elif args.name == "川後陽菜":
            name = "hina.kawago"
        elif args.name == "川村真洋":
            name = "mahiro.kawamura"
        elif args.name == "北野日奈子":
            name = "hinako.kitano"
        elif args.name == "齋藤飛鳥":
            name == "asuka.saito"
        elif args.name == "斎藤ちはる":
            name == "chiharu.saito"
        elif args.name == "斉藤優里":
            name == "yuuri.saito"
        elif args.name == "相楽伊織":
            name == "iori.sagara"
        elif args.name == "桜井玲香":
            name == "reika.sakurai"
        elif args.name == "佐々木琴子":
            name == "kotoko.sasaki"
        elif args.name == "白石麻衣":
            name = "mai.shiraishi"
        elif args.name == "新内眞衣":
            name == "mai.shinuchi"
        elif args.name == "鈴木絢音":
            name == "ayane.suzuki"
        elif args.name == "高山一実":
            name == "kazumi.takayama"
        elif args.name == "寺田蘭世":
            name == "ranze.terada"
        elif args.name == "中田花奈":
            name == "kana.nakada"
        elif args.name == "中元日芽香":
            name == "himeka.nakamoto"
        elif args.name == "西野七瀬":
            name = "nanase.nishino"
        elif args.name == "能條愛未":
            name == "ami.noujo"
        elif args.name == "橋本奈々未":
            name == "nanami.hashimoto"
        elif args.name == "樋口日奈":
            name == "hina.higuchi"
        elif args.name == "星野みなみ":
            name == "minami.hoshino"
        elif args.name == "堀未央奈":
            name == "miona.hori"
        elif args.name == "松村沙友理":
            name == "sayuri.matsumura"
        elif args.name == "山崎怜奈":
            name == "rena.yamazaki"
        elif args.name == "若月佑美":
            name == "yumi.wakatsuki"
        elif args.name == "渡辺みり愛":
            name == "miria.watanabe"
        elif args.name == "和田まあや":
            name == "maaya.wada"
        elif args.name == "三期生":
            name == "third"
        else:
            sys.stderr.write("There is no member! ")

    member_path = './members/' + name
    firstsearch_url = url + name

    while True:
        if pageNum == 0:
            savlog_individual(firstsearch_url, member_path)
        else:
            new_name = name + "/?p=" + pageNum
            nextsearch_url = url + new_name
            if return_url(firstsearch_url) == return_url(nextsearch_url):
                break
            else:
                savlog_individual(nextsearch_url, member_path)