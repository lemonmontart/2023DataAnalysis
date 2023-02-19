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
place_num = 33445697

URL = 'https://map.naver.com/v5/entry/place/' + str(place_num)
driver.get(url=URL)
driver.switch_to.frame('entryIframe')
driver.implicitly_wait(time_to_wait=2)

def review_info():
    #가게마다 리뷰 위치가 달라서 하나하나 확인해봐야됨
    driver.get(url='https://pcmap.place.naver.com/restaurant/19513640/review/visitor?from=map&fromPanelNum=2&ts=1676846281561')

    while True:
        try:
            driver.find_element(By.CLASS_NAME, 'Tvx37').click()
        except:
            break

    #driver.find_element(By.CLASS_NAME, 'Tvx37').click()
    #driver.find_element(By.CLASS_NAME, 'Tvx37').click()

    review = []
    review1 = []
    review2 = []
    #review_select = driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(7) > div:nth-child(3) > div.place_section.no_margin.mdJ86 > div > div > div.k2tmh > ul')
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


print(review_info())