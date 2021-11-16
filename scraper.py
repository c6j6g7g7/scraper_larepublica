import requests
import lxml.html as html

import os
import datetime

HOME_URL = 'https://www.larepublica.co'

XPATH_LINK_TO_ARTICLE = '//div[contains(@class, "V")]/a[contains(@class,"kicker")]/@href'
XPATH_TITLE = '//div[@id="vue-container"]//div[contains(@class,"container")]//div[@class="mb-auto"]/h2/span/text()'
XPATH_SUMMARY = '//div[contains(@class,"article-wrapper")]/div/div[contains(@class, "news")]/div[@class="lead"]/p/text()'
XPATH_BODY = '//div[contains(@class,"article-wrapper")]/div/div[contains(@class, "news")]/div[@class="html-content"]/p[not(@class)]/text()'


def parse_notice(link, today):
    
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('UTF-8')
            parsed = html.fromstring(notice)

            try:
                #print(f'Paso-> {parsed.xpath(XPATH_TITLE)}')
                title = parsed.xpath(XPATH_TITLE)[0]
                print(f'title->{title}')
                title = title.replace('\"', '')
                title = title.replace('/', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError as ie:
                print(ie)
                return
            #with-> manejador contextual
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                print(f'Paso-> 3 write')
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('UTF-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print(links_to_notices)
            today = datetime.date.today().strftime('%d-%m-%Y')

            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                print(link)
                parse_notice(link, today)
                return

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
