import csv
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import re
from urllib.request import urlopen
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError
import json

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
options.add_argument('window-size=1920,1080')
driver = webdriver.Chrome(executable_path='chromedriver', options=options)
driver.implicitly_wait(time_to_wait=5)

"""place_num에 원하는 상호의 가게 번호 입력하기"""
place_num = 19513640
URL = 'https://map.naver.com/v5/entry/place/' + str(place_num)
driver.get(url=URL)
driver.switch_to.frame('entryIframe')
driver.implicitly_wait(time_to_wait=2)


def using_api(address):
    x, y = None, None
    api_id = '1pgydi1iow'
    api_pw = 'oge4K33xEtDC18ZwzEl52lQxzBExlcNURQTzq8FZ'
    api_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='

    add_urlenc = parse.quote(address)
    url = api_url + add_urlenc

    request = Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', api_id)
    request.add_header('X-NCP-APIGW-API-KEY', api_pw)

    try:
        response = urlopen(request)

    except HTTPError as e:
        print('HTTP Error')

    else:
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read().decode('utf-8')
            response_body = json.loads(response_body)

            if response_body['addresses'] == []:
                print('No result')
            else:
                x = response_body['addresses'][0]['x']
                y = response_body['addresses'][0]['y']
                print('Success')
        else:
            print(f'Response error, rescode:{rescode}')
            x, y = None, None

    return [x, y]


def basic_info():
    basic = []
    try:
        place = driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm.f7aZ0')
        place = place.find_elements(By.TAG_NAME, 'span')
        for i in place:
            basic.append(i.text)

        try:
            star = driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div.place_section.OP4V8 > div.zD5Nm.f7aZ0 > div.dAsGb > span.PXMot.LXIwF > em')
            star = star.text
            basic.append(star)
        except:
            basic.append('0')
        return basic
    except:
        return 'basic_error'

def address_info():
    try:
        adrs = []
        address = driver.find_element(By.CSS_SELECTOR,
                                      '#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin.vKA6F > div > div > div.O8qbU.tQY7D > div')
        dis_from_station = address.find_elements(By.TAG_NAME, 'em')
        dis_from_station = dis_from_station[0].text
        address = address.find_elements(By.TAG_NAME, 'span')

        for i in address:
            adrs.append(i.text)
        adrs.remove('')
        adrs = list(dict.fromkeys(adrs))
        adrs.append(dis_from_station)

        address = adrs[0]
        xy = using_api(address)
        adrs.append(xy[0])
        adrs.append(xy[1])

        return adrs
    except:
        return 'address_error'

def review_info():
    try:
        driver.get(
            url='https://pcmap.place.naver.com/restaurant/'+str(place_num)+'/review/visitor?from=map&fromPanelNum=2&ts=1676846281561')
        while True:
            try:
                driver.find_element(By.CLASS_NAME, 'Tvx37').click()
            except:
                break
        review = []
        review1 = []
        review2 = []
        review_select = driver.find_element(By.CLASS_NAME, 'k2tmh')
        review_select1 = review_select.find_elements(By.CLASS_NAME, 'nWiXa')

        for i in review_select1:
            review1.append(i.text)
        for i, word in enumerate(review1):
            review1[i] = word.strip('"')
        review_select2 = review_select.find_elements(By.CLASS_NAME, 'TwM9q')
        review_num = driver.find_element(By.CLASS_NAME, '_Wmab')
        review_num = review_num.text
        review_num = review_num.split('회')[0]
        review_num = int(review_num)
        for i in review_select2:
            review2.append(i.text)
        for i, word in enumerate(review2):
            review2[i] = word.strip('이 키워드를 선택한 인원\n')
            review2[i] = round(int(review2[i]) / review_num, 4)

        review = list(zip(review1, review2))
        review.sort(key=lambda x: x[0])
        # 키워드 선택이 객관적인 비교 지표가 될 수 있을거라 생각했는데, 업종별로 선택 가능 키워드가 조금씩 다름(ex. 음식점, 카페 등)
        # 업종별로 모아서 분류를 해야 비교 가능할듯 / 물론 겹치는 키워드들도 다수 존재(ex. 매장의 크기 청결도 등)
        return review

    except:
        return 'review_error'


#def popularity():


basic = basic_info()
if basic == 'basic_error':
    basic = ['', '', '']
address = address_info()
if address == 'address_error':
    address = ['', '', '']
review = review_info()
if review == 'review_error':
    review = ['', '', '']

map_review = 0
blog_review = 0

for i in basic:
    if '방문자리뷰' in i:
        map_review = re.sub(r'[^0-9]', '', i)
    if '블로그리뷰' in i:
        blog_review = re.sub(r'[^0-9]', '', i)

data = pd.read_csv('review_data.csv', encoding='utf-8', index_col=0)
new_data = pd.DataFrame({
    'name': basic[0],
    'type': basic[1],
    'star': basic[-1],
    'address': address[0],
    'x': address[-2],
    'y': address[-1],
    'subway': str(address[1:-3]),
    #자료 형태가 안맞아서 몇호선들이 지나가는지 정수형으로 못넣고, 딕셔너리 형태 자체를 통으로 문자열로 받아서 넣음
    'dis': address[-3],
    'select_review': str(review),
    # 자료 형태가 안맞아서 딕셔너리 형태 자체를 통으로 문자열로 받아서 넣음
    'map_review': int(map_review),
    'blog_review': int(blog_review)
},
    index=[place_num])

data = pd.concat([data, new_data], axis=0)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
data.drop_duplicates()

data.to_csv('review_data.csv', index=True)

driver.close()