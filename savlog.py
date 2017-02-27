#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request as req
import argparse
import sys, codecs
import io

global pageNum

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


def savlog_individual(url):
    titles = []
    bodies = []

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

    if len(titles) == len(bodies):
        for num in range(len(titles)):
            print ("title is %s and content is %s" % (titles[num].text, bodies[num]))
    else:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='save blog data')
    parser.add_argument('--name', '-n', type=str, default='')
    args = parser.parse_args()

    if args.name == "橋本奈々未":
        name = "nanami.hashimoto"
    elif args.name == "西野七瀬":
        name = "nanase.nishino"
    elif args.name == "白石麻衣":
        name = "mai.shiraishi"
    elif args.name == "伊藤万理華":
        name = "marika.ito"
    elif args.name == "齋藤飛鳥":
        name == "asuka.saito"

    url = "http://blog.nogizaka46.com/" + name
    #savlog_general(url)
    savlog_individual(url)

    #ページを増やして無限ループで関数呼び出し
    #ページ数がこれ以上増えない(=pege not foundが返ってくる)時はbreak