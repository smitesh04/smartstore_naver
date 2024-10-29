import json
import urllib

import requests
from parsel import Selector


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

def deal(url):
    # file = open("C:/Users/Actowiz/Desktop/pagesave/smartstore_naver/6c45e6d1d6f5669b41e65d9e5b5a5de8.html", 'r', encoding='utf-8')
    # file = open("naver_html.html", 'r', encoding='utf-8')
    # data = file.read()
    # file.close()
    token = "42e3e8686c3e4066a56b117cdf011af79cd986cac0e"
    targetUrl = urllib.parse.quote(url)

    response = requests.get(
        f'http://api.scrape.do/?token={token}&geocode=kr&super=true&url={targetUrl}&forwardheaders=true&render=true',
        # cookies=cookies,
        # headers=headers
    )

    data = response.text
    
    response = Selector(data)
    jsn_raw = response.xpath("//script[contains(text(),'STATE__=')]/text()").get()
    jsn_raw = jsn_raw.replace("window.__PRELOADED_STATE__=", "")
    jsn_loaded = json.loads(jsn_raw)
    
    product_jsn = jsn_loaded['product']['A']
    
    name = product_jsn['name']
    sale_price = product_jsn['salePrice']
    discounted_sale_price = product_jsn['benefitsView']['discountedSalePrice']
    product_delivery_info = product_jsn['productDeliveryInfo']
    images = product_jsn['productImages']
    images_list = []
    if images:
        for img_dict in images:
            images_list.append(img_dict['url'])
    benefits_policy = product_jsn['benefitsPolicy']
    try:simple_options = product_jsn['simpleOptions']
    except:simple_options = None
    try:option_combinations = product_jsn['optionCombinations']
    except:option_combinations = None
    try:options = product_jsn['options']
    except:options = None
    supplements = product_jsn['supplements']
    product_id = product_jsn['id']
    error_view_message = None
    channel_product_status_type = product_jsn['channelProductStatusType']
    authentication_type = product_jsn['authenticationType']
    product_status_type = product_jsn['productStatusType']
    category_id = product_jsn['category']['categoryId']
    product_no = product_jsn['productNo']
    discounts = product_jsn['discounts']
    purchase_quantity_info = None
    stock_quantity = product_jsn['stockQuantity']

    output_jsn = {}
    output_jsn['id'] = product_id
    output_jsn['productNo'] = product_no
    output_jsn['productStatusType'] = product_status_type
    output_jsn['channelProductStatusType'] = channel_product_status_type
    output_jsn['authenticationType'] = authentication_type
    output_jsn['category'] = {}
    output_jsn['category']['categoryId'] = category_id
    output_jsn['name'] = name
    output_jsn['productImages'] = images_list
    output_jsn['discountedSalePrice'] = discounted_sale_price
    output_jsn['discounts'] = discounts
    output_jsn['productDeliveryInfo'] = product_delivery_info
    output_jsn['simpleOptions'] = simple_options
    output_jsn['optionCombinations'] = option_combinations
    output_jsn['options'] = options
    output_jsn['supplements'] = supplements
    output_jsn['benefitsPolicy'] = benefits_policy
    output_jsn['errorViewMessage'] = error_view_message
    output_jsn['purchaseQuantityInfo'] = purchase_quantity_info
    output_jsn['stockQuantity'] = stock_quantity

    output_jsn_translated = translate_text(str(output_jsn), 'ko', 'en')
    output_jsn_translated_final = json.loads(output_jsn_translated)['translated_text']


    return output_jsn_translated_final

    
if __name__ == '__main__':
    url = 'https://smartstore.naver.com/cocorynn/products/9880451043'
    a = deal(url)
    print()
