import json
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
import re


HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
}


def get_one_page(url):
    '''获取页面html'''
    try:
        response = requests.get(url=url, headers=HEADER)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    '''页面解析'''
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    '''解析结果写入文件'''
    with open('result.txt', 'a+', encoding='utf-8') as f:
        # json.dumps  将字典转为字符串
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
    pool.close()
    pool.join()
