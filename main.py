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
    # url = "https://smartstore.naver.com/dalutong/products/9807449873"
    targetUrl = urllib.parse.quote(url)
    import requests

    cookies = {
        '_fwb': '1480uNkSnh34uKp5O7HAoVF.1730187380015',
        'NAC': 'O7GmBYAFi7lu',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': '_fwb=1480uNkSnh34uKp5O7HAoVF.1730187380015; NAC=O7GmBYAFi7lu',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://smartstore.naver.com/cocorynn/products/6707275517',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-client-version': '20241024110650',
    }

    response = requests.get(
        f'http://api.scrape.do/?token={token}&geocode=kr&super=true&url={targetUrl}&forwardheaders=true&render=true',
        # cookies=cookies,
        # headers=headers
    )

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
    # url = 'https://smartstore.naver.com/partyshow/products/348366901'
    url = 'https://smartstore.naver.com/cocorynn/products/9880451043'
    # drission(url)
    request(url)
