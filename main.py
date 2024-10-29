import os.path

import requests
from common_func import  page_write, create_md5_hash
from fake_useragent import  UserAgent

ua = UserAgent()
import urllib.parse
token = "42e3e8686c3e4066a56b117cdf011af79cd986cac0e"

# import DrissionPage
# import time
from DrissionPage import ChromiumPage, ChromiumOptions, WebPage
from fake_useragent import UserAgent
import pyautogui
import re
from urllib.parse import unquote
import html
import pytesseract
from PIL import ImageGrab
proxyModeUrl = "http://{}:@proxy.scrape.do:8080.super=true".format(token)
proxies = {
    "http": proxyModeUrl,
    # "https": proxyModeUrl,
}

url = 'https://smartstore.naver.com/partyshow/products/348366901'
# url = 'https://smartstore.naver.com/dalutong/products/11032733784'
def request(url):
    url = "https://smartstore.naver.com/dalutong/products/9807449873"
    targetUrl = urllib.parse.quote(url)
    geocode = "il"
    url = "http://api.scrape.do?token={}&url={}&geoCode={}&super=true&render=true&sessionId=1234".format(token,
                                                                                                         targetUrl,
                                                                                                         geocode)

    payload = {}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'priority': 'u=0, i',
        'user-agent': ua.random
    }

    response = requests.get(url, headers=headers)
    print()
def drission(url):
    co = ChromiumOptions().set_proxy(proxies['http'])
    page = WebPage(chromium_options=co)
    page.get(url)
    hashid = create_md5_hash(url)
    pagesave_dir = rf"C:/Users/Actowiz/Desktop/pagesave/smartstore_naver/"
    file_name = fr"{pagesave_dir}/{hashid}.html"
    data = page.html

    if not os.path.exists(file_name) and '현재 서비스 접속이 불가합니다' not in str(data):
      page_write(pagesave_dir, file_name, data)

    # response = requests.request("GET", url, headers=headers, data=payload)


    print()


if __name__ == '__main__':
    url = 'https://smartstore.naver.com/partyshow/products/348366901'
    # drission(url)
    request(url)