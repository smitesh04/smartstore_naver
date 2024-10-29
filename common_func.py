import datetime
import hashlib
import json
import os

import requests
from fake_useragent import UserAgent
ua = UserAgent()


def create_md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()
def page_write(pagesave_dir, file_name, data):
    if not os.path.exists(pagesave_dir):
        os.makedirs(pagesave_dir)
    file = open(file_name, "w", encoding='utf8')
    file.write(data)
    file.close()
    return "Page written successfully"

def headers():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': ua.random,
        # 'Content-Type': 'application/json',

    }
    return headers

def translate_text(text, input_lang, output_lang):
    """Translates given text using the Google Translate API."""
    params = {
        'client': 'gtx',
        'sl': input_lang,
        'tl': output_lang,
        'dt': 't',
        'q': text,
    }
    response = requests.get('https://translate.googleapis.com/translate_a/single', params=params)
    print('RESPONSE_STATUS', response.status_code)
    result = response.json()
    translated_text = ''.join([item[0] for item in result[0]])
    return json.dumps({'RESPONSE_STATUS': response.status_code, 'translated_text': translated_text})

today_date = datetime.datetime.today().strftime('%d_%m_%Y')