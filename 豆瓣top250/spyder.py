from bs4 import BeautifulSoup
import requests
import re


def get_html(web_url):
    '''获取HTML'''
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.5.1.15355"}
    html = requests.get(url=web_url, headers=header).text
    Soup = BeautifulSoup(html, "lxml")
    # 返回的信息筛选
    data = Soup.find("ol").find_all("li")
    return data


def get_info(all_move):
    '''解析页面'''
    for info in all_move:
        # 编号
        nums = re.findall(r'<em class="">\d+</em>', str(info), re.S | re.M)
        nums = re.findall(r'\d+', str(nums), re.S | re.M)
        num = nums[0]

        # 名字
        names = info.find("span")  # li span
        name = names.get_text()

        # 导演
        charactors = info.find("p")  # 第一个p标签
        charactor = charactors.get_text().replace(" ", "").replace("\n", "")
        charactor = charactor.replace("\xa0", "").replace("\xee", "").replace("\xf6", "").replace(
            "\u0161", "").replace("\xf4", "").replace("\xfb", "").replace("\u2027", "")

        charactor = charactor[0:30]  # 控制信息长度
        # 评语
        remarks = info.find_all("span", {"class": "inq"})
        if remarks:  # 判断电影是否有评语
            remark = remarks[0].get_text().replace("\u22ef", "")
            remark = remark[0:30]  # 控制信息长度
        else:
            remark = "此影片没有评价"

        # 评分
        scores = info.find_all("span", {"class": "rating_num"})
        score = scores[0].get_text()

        # 将抓取到的信息以按逗号分隔的规律存入本地
        f = open("douban.txt", "a")
        f.write(num + ",")
        f.write(name + ",")
        f.write(charactor + ",")
        f.write(remark + ",")
        f.write(score)
        f.write("\n")
    f.close()


def main():
    # # 初始化页数，TOP一共有250部   每页25部
    page = 0
    while page <= 225:
        web_url = "https://movie.douban.com/top250?start=%s&filter=" % page
        all_move = get_html(web_url)
        get_info(all_move)
        page += 25


if __name__ == '__main__':
    main()
