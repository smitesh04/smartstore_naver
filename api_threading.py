import hashlib
import json
import os
import urllib
from fake_useragent import UserAgent
import requests
from parsel import Selector
from concurrent.futures import ThreadPoolExecutor, as_completed

ua = UserAgent()
def page_write(pagesave_dir, file_name, data):
    if not os.path.exists(pagesave_dir):
        os.makedirs(pagesave_dir)
    file = open(file_name, "w", encoding='utf8')
    file.write(data)
    file.close()
    return "Page written successfully"
def create_md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()

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
        request_url = f'http://api.scraperapi.com?api_key={scraper_token}&url={url}&country_code=kr&keep_headers=true'
    if 'brand.naver.com' in url:
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
    hashid = create_md5_hash(url)
    pagesave_dir = rf"C:/Users/Actowiz/Desktop/pagesave/smartstore_naver/test/"
    file_name = fr"{pagesave_dir}/{hashid}.html"

    data = response.text
    if not os.path.exists(file_name):
        page_write(pagesave_dir, file_name, data)
    response = Selector(data)

    # Parsing logic here remains unchanged
    # Example of product details parsing
    try:
        jsn_raw = response.xpath("//script[contains(text(),'STATE__=')]/text()").get()
        jsn_raw = jsn_raw.replace("window.__PRELOADED_STATE__=", "")
        jsn_loaded = json.loads(jsn_raw)
    except Exception as e:
        return f"Error parsing JSON data: {e}"

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
        # coupon_dict['discount_type'] = discount_type
        # coupon_dict['discount_value'] = discount_value
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
    hashid = create_md5_hash(url)
    pagesave_dir = rf"C:/Users/Actowiz/Desktop/pagesave/smartstore_naver/test/"
    file_name = fr"{pagesave_dir}/{hashid}.json"

    data = response.text
    if not os.path.exists(file_name):
        page_write(pagesave_dir, file_name, data)

    return data


def process_urls(urls):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        future_to_url = {executor.submit(deal, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append((url, result))
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
    return results

if __name__ == '__main__':
    urls = [
        # "https://brand.naver.com/mindbridge/products/11028585345",
        # Add up to 100 URLs for testing

        "https://smartstore.naver.com/keytotheworld/products/6731553972",
        "https://smartstore.naver.com/cocorynn/products/6707275517",
        "https://smartstore.naver.com/foodline7008/products/6664578952",
        "https://smartstore.naver.com/emaum/products/6651185983",
        "https://smartstore.naver.com/healingparts/products/6612245300",
        "https://smartstore.naver.com/felticsstore/products/6594750525",
        "https://smartstore.naver.com/charis99/products/6579849361",
        "https://smartstore.naver.com/doublecompany/products/6567236520",
        "https://smartstore.naver.com/patyroom/products/6562334666",
        "https://smartstore.naver.com/stitcheese/products/6542857506",
        "https://smartstore.naver.com/flat28/products/6504155411",
        "https://smartstore.naver.com/chennybb/products/6457454827",
        "https://smartstore.naver.com/4989_mall/products/6440767259",
        "https://smartstore.naver.com/valetcook/products/6412293778",
        "https://smartstore.naver.com/costcutmall/products/9977468739",
        "https://smartstore.naver.com/brggomaket/products/8231580912",
        "https://smartstore.naver.com/livmom/products/6630523813",
        "https://smartstore.naver.com/dingdongfactory/products/6312909157",
        "https://smartstore.naver.com/anystore2019/products/6209313970",
        "https://smartstore.naver.com/plannymall/products/6136079589",
        "https://smartstore.naver.com/greennatural/products/599791528",
        "https://smartstore.naver.com/barunpet/products/5979477852",
        "https://smartstore.naver.com/namju/products/5965058491",
        "https://smartstore.naver.com/lvclass/products/5943925954",
        "https://smartstore.naver.com/daon-ato/products/5885986885",
        "https://smartstore.naver.com/happyhomemart/products/5869136387",
        "https://smartstore.naver.com/bonie/products/5855302863",
        "https://smartstore.naver.com/drhauschka/products/5828788607",
        "https://smartstore.naver.com/sabimart/products/5804295680",
        "https://smartstore.naver.com/new-deal-motors/products/5787442087",
        "https://smartstore.naver.com/hoin6332/products/5729462103",
        "https://smartstore.naver.com/ohtworep/products/5627047135",
        "https://smartstore.naver.com/hdglobal/products/5606864965",
        "https://smartstore.naver.com/foodsystem/products/5557572041",
        "https://smartstore.naver.com/feelgoodhome/products/5518775475",
        "https://smartstore.naver.com/namdaleun/products/5505736576",
        "https://smartstore.naver.com/hyungchang/products/5493845994",
        "https://smartstore.naver.com/funnymomm/products/5447629615",
        "https://smartstore.naver.com/dangolfood/products/5439569468",
        "https://smartstore.naver.com/life-plusshop/products/5417598211",
        "https://smartstore.naver.com/samupia/products/5331195129",
        "https://smartstore.naver.com/edisontree/products/5296008333",
        "https://smartstore.naver.com/flintec/products/5253684418",
        "https://smartstore.naver.com/pajubeverage/products/5184055301",
        "https://smartstore.naver.com/sbliving/products/5290079643",
        "https://smartstore.naver.com/sssq/products/5279604116",
        "https://smartstore.naver.com/diyagit/products/5258648881",
        "https://smartstore.naver.com/ocook/products/5240340273",
        "https://smartstore.naver.com/scolon/products/5219673450",
        "https://smartstore.naver.com/just_one1/products/5201530979",
        "https://smartstore.naver.com/sparkle/products/5184947696",
        "https://smartstore.naver.com/knitlove/products/5160854160",
        "https://smartstore.naver.com/taekstores/products/5132897636",
        "https://smartstore.naver.com/sheetnara/products/5115184977",
        "https://smartstore.naver.com/jalko/products/5095855976",
        "https://smartstore.naver.com/gonup/products/5051323692",
        "https://smartstore.naver.com/foodsystem/products/5370797877",
        "https://smartstore.naver.com/animontage/products/5351584409",
        "https://smartstore.naver.com/moongufactory/products/5292188413",
        "https://smartstore.naver.com/atosafe/products/5226208926",
        "https://smartstore.naver.com/itshome/products/5173583593",
        "https://smartstore.naver.com/mcdb/products/5133378128",
        "https://smartstore.naver.com/hellojj/products/5070927222",
        "https://smartstore.naver.com/dadam-mall/products/5048251785",
        "https://smartstore.naver.com/yeogilo/products/5034127387",
        "https://smartstore.naver.com/n09holding/products/4989099340",
        "https://smartstore.naver.com/dulle80/products/4956483646",
        "https://smartstore.naver.com/ncib/products/4936432161",
        "https://smartstore.naver.com/bekjang/products/5453264601",
        "https://smartstore.naver.com/chulmin/products/5406330067",
        "https://smartstore.naver.com/izikorea/products/5384806853",
        "https://smartstore.naver.com/chungahdang/products/5357493491",
        "https://smartstore.naver.com/itdda/products/5294624154",
        "https://smartstore.naver.com/jueunfood/products/5264780519",
        "https://smartstore.naver.com/ottogimall/products/522771512",
        "https://smartstore.naver.com/sportzone/products/5013352270",
        "https://smartstore.naver.com/rs/products/4966146824",
        "https://smartstore.naver.com/amen3/products/4944940748",
        "https://smartstore.naver.com/davansa/products/4930021421",
        "https://smartstore.naver.com/awins/products/4902019531",
        "https://smartstore.naver.com/eelfish/products/4871333501",
        "https://smartstore.naver.com/ajumungu/products/5012525219",
        "https://smartstore.naver.com/itshoe/products/4996910801",
        "https://smartstore.naver.com/getnudge/products/4972244952",
        "https://smartstore.naver.com/florahome/products/4935772334",
        "https://smartstore.naver.com/xeonic/products/4883498889",
        "https://smartstore.naver.com/kanh/products/4875461620",
        "https://smartstore.naver.com/inmarket/products/4866120609",
        "https://smartstore.naver.com/namdaemunmarket/products/4852518097",
        "https://smartstore.naver.com/jwstore2017/products/4843420839",
        "https://smartstore.naver.com/woorispom/products/4832674155",
        "https://smartstore.naver.com/dadreammall1094/products/4799105847",
        "https://smartstore.naver.com/healthbell/products/4772444842",
        "https://smartstore.naver.com/aircareplus/products/5110918207",
        "https://smartstore.naver.com/hoho9846/products/5049156349",
        "https://smartstore.naver.com/foodwarehouse/products/5035625036",
        "https://smartstore.naver.com/audrk/products/4993690886",
        "https://smartstore.naver.com/soeasyshop/products/4918428895",
        "https://smartstore.naver.com/congsap/products/4872413095",
        "https://smartstore.naver.com/semodisplay/products/4858822546"

    ]
    results = process_urls(urls)
    for url, result in results:
        print(f"URL: {url} - Result: {result}")
