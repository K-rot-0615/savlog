#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
from pageInfo import return_html, return_date, return_date2
import urllib.request as req
import argparse
import sys
import codecs
import io
import re
import os
import os.path


def savlog_general(url):
    authors = []
    titles = []

    soup = return_html(url)
    spans = soup.find_all('span', class_='heading')
    for author in spans:
        authors.append(author.find('span', class_='author'))
    for title in spans:
        titles.append(title.find('span', class_="entrytitle").find('a'))

    for a in range(len(authors)):
        print("name is %s and title is %s" % (authors[a].text, titles[a].text))


def savlog_individual(url, member_path):
    titles = []
    bodies = []
    days = []
    images = []

    # make individual member's folder or change current path to member path
    if os.path.isdir(member_path) == False:
        os.mkdir(member_path)
        #os.chmod(member_path, 0o777)

    soup = return_html(url)
    entrytitle = soup.find_all('span', class_='entrytitle')
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
        correct_sentence = re.sub(r'\s', '\n', sentence)
        bodies.append(correct_sentence)

        for img in body.find_all('img'):
            emoji_remover = re.search(r"gif", img['src'])
            if emoji_remover:
                print("絵文字は嫌い！")
            else:
                image.append(img['src'])
        each_images = '$'.join(image)
        images.append(each_images)

    # get each date
    for day in entrybottom:
        split_word = day.text.split()
        word = split_word[0]
        split_day = word.split('/')
        date = '_'.join(split_day)
        days.append(date)

    # the size of titles matches that of bodies and days
    if len(titles) == len(bodies) and len(bodies) == len(days) and len(days) == len(titles):
        os.chdir(member_path)
        for num in range(len(titles)):
            save_path = './' + days[num]
            if not os.path.isdir(save_path):
                os.mkdir(save_path)
                os.chdir(save_path)
            else:
                os.chdir(save_path)

            write_file = titles[num].text.replace('/', '_') + '.txt'
            with open(write_file, 'w', encoding='utf-8') as f:
                f.write(bodies[num])
                f.close()
            counter = 1
            # except for the empty case
            if images.count('') == 0:
                split_image = images[num].split('$')
                print(split_image)
                for save_image in split_image:
                    image = req.urlopen(save_image)
                    image_file = 'img' + str(counter) + '.jpg'
                    with open(image_file, 'wb') as f:
                        f.write(image.read())
                        f.close()
                    counter += 1
            os.chdir('../')

    os.chdir('../../')


def next_pages(url, search_url, name, member_path, year, month, date, pageNum):
    _url = url
    _search_url = search_url
    _name = name
    _member_path = member_path
    _year = year
    _month = month
    _date = date
    _pageNum = pageNum

    new_name = _name + "/?p=" + str(_pageNum) + "&d=" + _date
    nextsearch_url = _url + new_name

    # page 2 doesn't exsits
    counter = 0
    days1 = return_date2(_search_url)
    days2 = return_date2(nextsearch_url)
    a = len(days2) if len(days1) > len(days2) else len(days1)
    for i in range(a):
        if days1[i] == days2[i]:
            counter += 1

    if counter == a:
        _pageNum = 1
        calculated_month = int(_month) - 1

        # move to previous month
        if calculated_month == 0:
            print("next is previous year!")
            _year = str(int(_year) - 1)
            _month = str(12)
        elif calculated_month < 10:
            print("previous month!! still continuing!!")
            _month = str(0) + str(calculated_month)
        else:
            print("previous month")
            _month = str(calculated_month)
        return _year, _month

    # page 2 or more exists
    else:
        savlog_individual(nextsearch_url, _member_path)
        _pageNum += 1
        return next_pages(_url, _search_url, _name, _member_path, _year, _month, _date)
