# -*- coding:utf-8 -*-
from selenium import webdriver
import time
from multiprocessing import Pool
import pymongo
import csv

client = pymongo.MongoClient('localhost', 27017)
mydb = client['Qzone']
# 好友列表
QQ = mydb['QQ']
# 说说信息
qzone = mydb['qzone']

# 打开csv文件


def get_friends_list(path):
    fp = open(path, encoding='UTF-8')
    reader = csv.DictReader(fp)
    for row in reader:
        qq = row['电子邮件'].split('@')[0]
        QQ.insert_one({'qq': qq})
    fp.close()


def get_info(qq):
    driver.get('https://user.qzone.qq.com/{}/311'.format(qq))
    driver.implicitly_wait(10)
    # 登录
    try:
        driver.find_element_by_id('login_div')
        a = True
    except:
        a = False

    if a == True:
        driver.switch_to.frame('login_frame')
        driver.find_element_by_id('switcher_plogin').click()  # 账号密码登录
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys('1736734085')
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys('19970617qqqq')
        driver.find_element_by_id('login_button').click()
        time.sleep(3)
    driver.implicitly_wait(3)
    # 判断是否有查看的权限
    try:
        driver.find_element_by_id('QM_OwnerInfo_ModifyIcon')
        b = True
    except:
        b = False
        print('无法访问%s的空间，需要权限 ' % qq)

    if b == True:
        # 爬取内容
        driver.switch_to.frame('app_canvas_frame')
        next_page = 'page'
        page = 1
        try:
            # 爬取全部说说
            while next_page:
                print('正在抓取第%d页面内容······' % page)
                contents = driver.find_elements_by_css_selector('.content')
                times = driver.find_elements_by_css_selector(
                    '.c_tx.c_tx3.goDetail')
                for content, stime in zip(contents, times):
                    data = {
                        'qq': qq,
                        'time': stime.text,
                        'shuos': content.text
                    }
                    qzone.insert_one(data)
                    # print(data)
                next_page = driver.find_element_by_link_text('下一页')  # 文本定位
                next_page.click()
                time.sleep(3)  # 等待页面加载
                driver.implicitly_wait(3)
                page = page + 1
        except:
            print('抓取到%d页面结束' % page)



# driver = webdriver.PhantomJS()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.maximize_window()  # 窗口最大化

if __name__ == '__main__':
    get_friends_list('QQmail.csv')
    friends = [item['qq'] for item in QQ.find()]
    pool = Pool(processes=4)
    pool.map(get_info, friends)
