import json
import requests
import re
import urllib
from bs4 import *


HEADER = {
    "Host": " music.163.com",
    "User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
}


def get_html(url):
    '''获取页面'''
    request = urllib.request.Request(url, headers=HEADER)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8', 'ignore')
    return html


def get_info(html):
    '''解析歌词'''
    soup = BeautifulSoup(html, 'lxml')
    for item in soup.ul.children:
        # 取出歌单里歌曲的id
        song_id = item('a')[0].get("href", None)
        # 利用正则表达式提取出song_id的数字部分sid
        pat = re.compile(r'[0-9].*$')
        sid = re.findall(pat, song_id)[0]
        # 这里的url是真实的歌词页面
        url = "http://music.163.com/api/song/lyric?" + \
            "id=" + str(sid) + "&lv=1&kv=1&tv=-1"
        html = requests.post(url)
        json_obj = html.text
        # 解析歌词json对象
        j = json.loads(json_obj)
        try:
            lyric = j['lrc']['lyric']
        except KeyError:
            lyric = "无歌词"
        pat = re.compile(r'\[.*\]')
        lrc = re.sub(pat, "", lyric)
        lrc = lrc.strip()
        yield lrc


def save_info(html):
    '''写入本地文件'''
    with open('myfavoritesong.txt', 'a+', encoding='utf-8') as f:
        for lrc in get_info(html):
            f.write(lrc)


def main():
    url = "http://music.163.com/playlist?id=821745668"
    html = get_html(url)
    save_info(html)


if __name__ == '__main__':
    main()
