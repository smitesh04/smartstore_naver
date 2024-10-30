import json
import urllib
from fake_useragent import UserAgent
import requests
from parsel import Selector

ua = UserAgent()

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
    token = "42e3e8686c3e4066a56b117cdf011af79cd986cac0e"
    scraper_token = "af6554d818a9a97545ecf42a0b335f36"
    targetUrl = urllib.parse.quote(url)
    request_url = url
    if 'smartstore.naver.com' in url:
        # request_url = f'http://api.scrape.do/?token={token}&geocode=kr&super=true&url={targetUrl}&forwardheaders=true&render=true'
        request_url = f'http://api.scraperapi.com?api_key={scraper_token}&url={url}&country_code=kr&keep_headers=true'
    if 'brand.naver.com' in url:
        # request_url = f'http://api.scrape.do/?token={token}&geocode=kr&super=true&url={targetUrl}&forwardheaders=true'
        request_url = f'http://api.scraperapi.com?api_key={scraper_token}&url={url}&country_code=kr&keep_headers=true'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': '_fwb=1480uNkSnh34uKp5O7HAoVF.1730187380015; NAC=O7GmBYAFi7lu',
        'user-agent': ua.random
    }

    response = requests.get(
        url=request_url, headers=headers
    )
    data = response.text
    response = Selector(data)

    jsn_raw = response.xpath("//script[contains(text(),'STATE__=')]/text()").get()
    jsn_raw = jsn_raw.replace("window.__PRELOADED_STATE__=", "")
    jsn_loaded = json.loads(jsn_raw)

    product_jsn = jsn_loaded['product']['A']
    channel_uid = product_jsn['channel']['channelUid']

    name = product_jsn['name']
    sale_price = product_jsn['salePrice']
    try:
        discounted_sale_price = product_jsn['benefitsView']['discountedSalePrice']
    except:
        discounted_sale_price = 'None'
    product_delivery_info = product_jsn['productDeliveryInfo']
    images = product_jsn['productImages']
    images_list = []
    if images:
        for img_dict in images:
            images_list.append(img_dict['url'])
    benefits_policy = product_jsn['benefitsPolicy']
    try:
        simple_options = product_jsn['simpleOptions']
    except:
        simple_options = "None"
    try:
        option_combinations = product_jsn['optionCombinations']
    except:
        option_combinations = "None"
    try:
        options = product_jsn['options']
    except:
        options = "None"
    supplements = product_jsn['supplements']
    product_id = product_jsn['id']
    error_view_message = "None"
    channel_product_status_type = product_jsn['channelProductStatusType']
    authentication_type = product_jsn['authenticationType']
    product_status_type = product_jsn['productStatusType']
    category_id = product_jsn['category']['categoryId']
    product_no = product_jsn['productNo']
    discounts = product_jsn['discounts']
    purchase_quantity_info = "None"
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
    output_jsn['options'] = options
    output_jsn['optionCombinations'] = option_combinations
    output_jsn['supplements'] = supplements
    output_jsn['benefitsPolicy'] = benefits_policy
    output_jsn['errorViewMessage'] = error_view_message
    output_jsn['purchaseQuantityInfo'] = purchase_quantity_info
    output_jsn['stockQuantity'] = stock_quantity

    coupon_response = coupon(product_no, channel_uid, category_id)
    coupon_dict = {}
    try:
        coupon_jsn = json.loads(coupon_response)
    except:
        coupon_jsn = ''
    if coupon_jsn:
        try:
            benefit_value = coupon_jsn['basicBenefits'][0]['benefitValue']
        except:
            benefit_value = "None"
        try:
            max_discount_amount = coupon_jsn['sortedHomeBenefits'][0]['maxDiscountAmount']
        except:
            max_discount_amount = "None"
        try:
            customer_manage_benefit_policy_no = coupon_jsn['basicBenefits'][0]['customerManageBenefitPolicyNo']
        except:
            customer_manage_benefit_policy_no = "None"
        try:
            coupon_kind_type = coupon_jsn['basicBenefits'][0]['couponKindType']
        except:
            coupon_kind_type = "None"
        try:
            coupon_name = coupon_jsn['basicBenefits'][0]['benefitPolicyName']
        except:
            coupon_name = "None"
        try:
            min_order_amount = coupon_jsn['basicBenefits'][0]['minOrderAmount']
        except:
            min_order_amount = "None"
        try:
            benefit_unit_type = coupon_jsn['sortedHomeBenefits'][0]['benefitUnitType']
        except:
            benefit_unit_type = "None"
        try:
            discount_type = ""  # todo
        except:
            discount_type = "None"
        try:
            discount_value = ""  # todo
        except:
            discount_value = "None"
        try:
            validity_day = coupon_jsn['sortedHomeBenefits'][0]['validityDay']
        except:
            validity_day = "None"
        try:
            benefit_start_date = coupon_jsn['sortedHomeBenefits'][0]['benefitStartDate']
        except:
            benefit_start_date = "None"
        try:
            benefit_end_date = coupon_jsn['sortedHomeBenefits'][0]['benefitEndDate']
        except:
            benefit_end_date = "None"
        coupon_dict['benefitValue'] = benefit_value
        coupon_dict['maxDiscountAmount'] = max_discount_amount
        coupon_dict['customerManageBenefitPolicyNo'] = customer_manage_benefit_policy_no
        coupon_dict['couponKindType'] = coupon_kind_type
        coupon_dict['coupon_name'] = coupon_name
        coupon_dict['minOrderAmount'] = min_order_amount
        coupon_dict['benefitUnitType'] = benefit_unit_type
        coupon_dict['discount_type'] = discount_type
        coupon_dict['discount_value'] = discount_value
        coupon_dict['validityDay'] = validity_day
        coupon_dict['benefitStartDate'] = benefit_start_date
        coupon_dict['benefitEndDate'] = benefit_end_date
    output_jsn['coupon'] = coupon_dict

    output_jsn_translated = translate_text(str(output_jsn), 'ko', 'en')
    output_jsn_translated_final = json.loads(output_jsn_translated)['translated_text'].replace(' ', '')

    return output_jsn_translated_final

def coupon(product_no, channel_uid, category_id):
    token = "42e3e8686c3e4066a56b117cdf011af79cd986cac0e"
    scraper_token = "af6554d818a9a97545ecf42a0b335f36"

    url = f'https://brand.naver.com/n/v2/channels/{channel_uid}/benefits/by-products/{product_no}?categoryId={category_id}'
    targetUrl = urllib.parse.quote(url)
    request_url = url
    if 'brand.naver.com' in url:
        # request_url = f'http://api.scrape.do/?token={token}&geocode=kr&super=true&url={targetUrl}&forwardheaders=true'
        request_url = f'http://api.scraperapi.com?api_key={scraper_token}&url={url}&country_code=kr&keep_headers=true'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': '_fwb=1480uNkSnh34uKp5O7HAoVF.1730187380015; NAC=O7GmBYAFi7lu',
        'user-agent': ua.random,
    }
    response = requests.get(request_url, headers=headers)
    return response.text


if __name__ == '__main__':
    # url = 'https://smartstore.naver.com/foodline7008/products/6664578952'
    # url = 'https://smartstore.naver.com/foodline7008/products/6664578952'
    # url = "https://smartstore.naver.com/mindbridge/products/11028585345"
    url = "https://brand.naver.com/mindbridge/products/11028585345"
    a = deal(url)
    print()
