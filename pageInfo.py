#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request as req


def return_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
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
