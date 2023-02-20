import csv
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
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
place_num = 170899606

URL = 'https://map.naver.com/v5/entry/place/' + str(place_num)
driver.get(url=URL)
driver.switch_to.frame('entryIframe')
driver.implicitly_wait(time_to_wait=2)

def popularity():
    action = ActionChains(driver)
    male = driver.find_element(By.XPATH, '//*[@id="_datalab_chart_donut1_0"]/svg/g[1]/g[3]/g[4]/g[2]/text[2]')
    male = male.find_element(By.TAG_NAME, 'text')
    print(male.text)


popularity()