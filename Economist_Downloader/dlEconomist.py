#! /usr/bin/python3
# coding=utf-8
import urllib.request
from bs4 import BeautifulSoup

front_url = "http://www.kekenet.com/Soft/"
download_link_front = "http://u1.kekenet.com/index.php?m=content&c=down&articleid="
download_link = []


# 得到所有下载列表页面的数目
def get_total_number():
    html = urllib.request.urlopen(front_url + 'economist')
    soup = BeautifulSoup(html, 'html.parser')
    next_page_html = soup.select('.page')[-1].find_all('a')[0]['href']
    next_page = next_page_html.split('_')[-1]
    total = next_page.split('.')[0]
    return total


# 得到所有下载列表的页面网址
def get_all_downloadlist_page():
    total = int(get_total_number())
    download_page = [front_url+'economist/']
    page_number = list(range(1, total+1))
    for each in page_number:
        download_page.append(front_url + 'economist/List_' +  str(each) + '.shtml')
    return download_page


# 得到下载页面链接的地址
def get_download_url(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.select('.dl_title')
    for each in container:
        link = str(each).split('><')[1].split("\"")[1].split("/")[-1].split('.')[0]
        download_link.append(download_link_front + link)


# 写入下载页面的链接
def get_download_page_link():
    downloadlist_url = get_all_downloadlist_page()
    for url in downloadlist_url:
        print("URL: " + url)
        get_download_url(url)
    with open('link.txt','w') as f:
        print("开始写入文件\n")
        for each in download_link:
            html = urllib.request.urlopen(each)
            soup = BeautifulSoup(html, 'html.parser')
            script = soup.find_all('script')[-3]
            link = str(script).split("getHDLinkProtectUrl(\'")[1].split('\')')[0]
            print(link)
            f.write(str(link) + '\n')
        f.close()

get_download_page_link()
