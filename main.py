#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from pageInfo import return_date
from savlog import savlog_general, savlog_individual, next_pages
import argparse
import sys
import codecs
import io
import re
import os
import os.path


def main():
    parser = argparse.ArgumentParser(description='save blog data')
    parser.add_argument('--name', '-n', type=str, default='')
    args = parser.parse_args()

    # convert us-ascii to utf-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    umask = os.umask(0)
    if os.path.isdir('./members/') == False:
        os.mkdir('./members/', 0o777)
        #os.chmod('./members/', 0o777)
        os.umask(umask)

    url = "http://blog.nogizaka46.com/"
    name = ""
    today = datetime.now()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    current_date = year + month
    date = current_date
    pageNum = 1
    #date = str(2012) + str(0) + str(3)

    if args.name == '':
        savlog_general(url)
    else:
        if args.name == "秋元真夏":
            name = "manatsu.akimoto/"
        elif args.name == "生田絵梨花":
            name = "erika.ikuta/"
        elif args.name == "伊藤かりん":
            name = "karin.itou/"
        elif args.name == "伊藤純奈":
            name = "junna.itou/"
        elif args.name == "伊藤理々杏":
            name = "riria.ito/"
        elif args.name == "井上小百合":
            name = "sayuri.inoue/"
        elif args.name == "岩本蓮加":
            name = "renka.iwamoto/"
        elif args.name == "梅澤美波":
            name = "minami.umezawa/"
        elif args.name == "衛藤美彩":
            name = "misa.eto/"
        elif args.name == "大園桃子":
            name = "momoko.ozono/"
        elif args.name == "川後陽菜":
            name = "hina.kawago/"
        elif args.name == "北野日奈子":
            name = "hinako.kitano/"
        elif args.name == "久保史緒里":
            name = "shiori.kubo/"
        elif args.name == "齋藤飛鳥":
            name = "asuka.saito/"
        elif args.name == "斉藤優里":
            name = "yuuri.saito/"
        elif args.name == "阪口珠美":
            name = "tamami.sakaguchi/"
        elif args.name == "桜井玲香":
            name = "reika.sakurai/"
        elif args.name == "佐々木琴子":
            name = "kotoko.sasaki/"
        elif args.name == "佐藤楓":
            name = "kaede.sato/"
        elif args.name == "白石麻衣":
            name = "mai.shiraishi/"
        elif args.name == "新内眞衣":
            name = "mai.shinuchi/"
        elif args.name == "鈴木絢音":
            name = "ayane.suzuki/"
        elif args.name == "高山一実":
            name = "kazumi.takayama/"
        elif args.name == "寺田蘭世":
            name = "ranze.terada/"
        elif args.name == "中田花奈":
            name = "kana.nakada/"
        elif args.name == "中村麗乃":
            name = "reno.nakamura/"
        elif args.name == "西野七瀬":
            name = "nanase.nishino/"
        elif args.name == "能條愛未":
            name = "ami.noujo/"
        elif args.name == "樋口日奈":
            name = "hina.higuchi/"
        elif args.name == "星野みなみ":
            name = "minami.hoshino/"
        elif args.name == "堀未央奈":
            name = "miona.hori/"
        elif args.name == "松村沙友理":
            name = "sayuri.matsumura/"
        elif args.name == "向井葉月":
            name = "haduki.mukai"
        elif args.name == "山崎怜奈":
            name = "rena.yamazaki/"
        elif args.name == "山下美月":
            name = "miduki.yamashita/"
        elif args.name == "吉田綾乃クリスティー":
            name = "ayano.christie.yoshida/"
        elif args.name == "与田祐希":
            name = "yuuki.yoda"
        elif args.name == "若月佑美":
            name = "yumi.wakatsuki/"
        elif args.name == "渡辺みり愛":
            name = "miria.watanabe/"
        elif args.name == "和田まあや":
            name = "maaya.wada/"
        else:
            sys.stderr.write("There is no member! ")

    member_path = './members/' + name
    first_url = url + name
    roop_counter = 1
    fake_counter = 0

    while True:
        print('search date is ' + date)
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
            # suspicious_month = str(0) + str(int(month) - 1)
            # 1月サーチの場合 前年12月にブログ記事があるかチェック
            if int(month) == 1:
                suspicious_month = str(12)
                suspicious_year = str(int(year) - 1)
            # 前年に繰越にならない場合
            else:
                suspicious_month = str(
                    int(month) - 1) if int(month) > 10 else str(0) + str(int(month) - 1)
                suspicious_year = year
            suspicious_date = suspicious_year + suspicious_month
            suspicious_url = url + name + "?d=" + suspicious_date
            suspicious_days = return_date(suspicious_url)
            print('suspicious date is ' + suspicious_date)
            for i in range(len(suspicious_days)):
                if first_url_days[i] == suspicious_days[i]:
                    counter += 1
            # not updated blog for two conecutive months -> there is no article cuz it is too previous year
            if counter == len(first_url_days) == len(suspicious_days):
                print('nothing!! do more previous articles exist?')
                fake_counter += 1
                if fake_counter < 12:
                    month = suspicious_month
                    year = suspicious_year
                    date = suspicious_date
                else:
                    break
            else:
                month = suspicious_month
                year = suspicious_year
                date = suspicious_date

        else:
            print('start')
            # processing when page number is 1
            search_url = url + name + "?d=" + date
            savlog_individual(search_url, member_path)
            pageNum += 1
            print('pagenum 0 finished!')

            next_year, next_month = next_pages(
                url, search_url, name, member_path, year, month, date, pageNum)
            year = next_year
            month = next_month
            date = year + month
            print('round' + str(roop_counter) + 'finished!!')

    print('saving is finished!!')


if __name__ == '__main__':
    main()
