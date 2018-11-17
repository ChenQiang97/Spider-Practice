import requests
from PIL import Image
import datetime
import time
import os
from os import system


def download_img(url, img_save_path):
    '''爬取图片并保存到本地'''
    header = {
        "User_Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    img = requests.get(url=url, headers=header).content
    with open(img_save_path, "wb") as f:
        f.write(img)
        print(img_save_path, "图片下载成功")


def fill_img(img, img_save_path):
    '''设置图片大小,空白部分以黑色填充'''
    width, height = 1920, 1080
    new_img = Image.new(img.mode, (width, height), color='black')
    new_img.paste(img, (int(width / 2 - 250), int(height / 2 - 250)))
    new_img.save(img_save_path)
    print(img_save_path, "图片合成成功")


def get_img_url(img_base_url):
    '''构造图片url'''
    # 获取格林威治时间
    now_utc_datetime = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
    # 时间格式化
    now_utc_datetime = now_utc_datetime.strftime("%Y/%m/%d/%H%M")
    time_list = list(now_utc_datetime)
    time_list[-1] = '0'
    now_utc_datetime = "".join(time_list)
    img_url = img_base_url + now_utc_datetime + "00_0_0.png"
    img_name = now_utc_datetime.replace("/", "_") + "00_0_0.png"
    return img_url, img_name


def main():
    base_url = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/"
    url, name = get_img_url(base_url)
    img_save_path = "Download_Picture/" + name
    new_img_save_path = "Wallpaper/new_" + name
    download_img(url, img_save_path)
    img = Image.open(img_save_path)
    fill_img(img, new_img_save_path)
    img_url = os.getcwd() + "/" + new_img_save_path
    if not system("gsettings set org.gnome.desktop.background picture-uri %s" % img_url):
        print(new_img_save_path, "壁纸设置成功")


if __name__ == '__main__':
    '''每隔15min执行一次'''
    if not os.path.exists("Download_Picture"):
        system("mkdir Download_Picture Wallpaper")
        print("创建图片路径成功")
    while True:
        main()
        time.sleep(15 * 60)
