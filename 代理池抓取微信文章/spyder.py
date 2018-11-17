from urllib.parse import urlencode
import pymongo
import requests
from lxml.etree import XMLSyntaxError
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq

max_count = 5

MONGO_URI = 'localhost'
MONGO_DB = 'weixin'

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]

keyword = '风景'
base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'IPLOC=CN1401; SUID=7C4E313B2013940A000000005AFD2D97; SUV=1526541721465182; ABTEST=0|1526541740|v1; weixinIndexVisited=1; sct=1; JSESSIONID=aaaJyJXwxhkcMgeRoAjnw; ppinf=5|1526542016|1527751616|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTklQTMlOEUlRTQlQkYlQTElRTUlQUQlOTB8Y3J0OjEwOjE1MjY1NDIwMTZ8cmVmbmljazoyNzolRTklQTMlOEUlRTQlQkYlQTElRTUlQUQlOTB8dXNlcmlkOjQ0Om85dDJsdURRRmdwUUhSWHRDZmtKR25RR2diRzRAd2VpeGluLnNvaHUuY29tfA; pprdig=a4M8A6BlmVW3QI5ZPC06EgIg73YKBkA9IXwMLEBm53SRysSD8o-jB-zE_31LTp8SOfeclM-iuNVO6fYmPb7K_CEedQATmIqgSAcmRhr6Sws1Mrjy6-YqC7eoCcsgifphIJNJpxoeqtTNlqZMkj-lkWaeMzsLS82ESrkA2zVfQKI; sgid=10-35092221-AVr9LsCeNibOSBicCD52W3PrI; ppmdig=152654201600000033f6fe228ded8379823afeed80ae3278; PHPSESSID=tf6ed1lo5oanolhaon6vmdval5; SUIR=7D4C303902046E63B32BDAAC021F5B69; SNUID=22106C665E58323F89DBBC785ED8CBD0; pgv_pvi=8293783552; pgv_si=s4770388992',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}

proxy_pool_url = 'http://127.0.0.1:5555/random'
# 获取代理


def get_proxy():
    try:
        response = requests.get('http://127.0.0.1:5555/random')
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


proxy = None  # 是否使用代理，默认关闭


def get_html(url, count=1):

    print('Crawling Count', url)
    print('Trying Count', count)

    global proxy

    if count >= max_count:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(
                url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(
                url, allow_redirects=False, headers=headers)

        if response.status_code == 200:
            return response.text

        if response.status_code == 302:
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                # 更换IP，重新爬取
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


def get_index(keyword, page):
    '''获取索引页'''
    data = {'query': keyword, 'type': 2, 'page': page}
    # 编码，转为get请求参数格式
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def parse_index(html):
    '''解析索引页'''
    doc = pq(html)
    # 得到链接的生成器
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')


def get_detail(url):
    '''获取详情页'''
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def parse_detail(html):
    '''解析详情页'''
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('#profileBt > a').text()
        date = doc('#publish_time').text()
        nickname = doc('#js_profile_qrcode > div > strong').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title': title,
            'content': content,
            'date': date,
            'nickname': nickname,
            'wechat': wechat
        }
    except XMLSyntaxError:
        return None


def save_to_mongo(data):
    '''保存到mongodb'''
    if db['articles'].update({'title': data['title']}, {'$set': data}, True):
        print('Saved to Mongo', data['title'])
    else:
        print('Saved to Mongo Failed', data['title'])


def main():
    for page in range(1, 100):
        html = get_index(keyword, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    print(article_data)
                    if article_data:
                        save_to_mongo(article_data)


if __name__ == '__main__':
    main()
