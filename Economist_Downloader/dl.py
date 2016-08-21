#! /usr/bin/python3
# coding=utf-8
import urllib.request
import threading, time, random
from bs4 import BeautifulSoup

front_url = "http://www.kekenet.com/Soft/"
download_link_front = "http://u1.kekenet.com/index.php?m=content&c=down&articleid="
download_link = []
SHARE_QUEUE = []
CONDITOIN = threading.Condition()
THREAD_P = []
done = 0
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
    global Download_link
    total = int(get_total_number())
    download_link = [front_url+'economist/']
    page_number = list(range(1, total+1))
    for each in page_number:
        download_link.append(front_url + 'economist/List_' +  str(each) + '.shtml')
    return download_link


# 得到下载页面链接的地址
def get_download_url(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.select('.dl_title')
    for each in container:
        link = str(each).split('><')[1].split("\"")[1].split("/")[-1].split('.')[0]
        download_link.append(download_link_front + link)
    return download_link


# 写入下载页面的链接
def get_download_link(url):
    with open('link','a') as f:
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find_all('script')[-3]
        link = str(script).split("getHDLinkProtectUrl(\'")[1].split('\')')[0]
        print("**********************" + str(link))
        f.write(str(link) + '\n')
        f.close()


class Producer(threading.Thread):
    def run(self):
        products = get_all_downloadlist_page()
        global SHARE_QUEUE, done
        while True:
            CONDITOIN.acquire()
            if len(SHARE_QUEUE) == 5:
                print("page_list queue is full")
                CONDITOIN.wait()
                print("Consumer have comsumed something")
            if len(products) != 0:
                product = products.pop()
                # print("Product: " + product + " remain: " + str(len(products)))
                SHARE_QUEUE.append(product)
                CONDITOIN.notify()
                CONDITOIN.release()
                time.sleep(random.random())
            else:
                if not done:
                    done = 1
                    print("Producer's work is done!")
                CONDITOIN.release()


class Consumer(threading.Thread):
    def run(self):
        global SHARE_QUEUE, done
        while not done or len(SHARE_QUEUE) != 0:
            CONDITOIN.acquire()
            if len(SHARE_QUEUE) == 0:
                print(" Queue is empty")
                CONDITOIN.wait()
                print(" Producer have producted something")
            else:
                print("Consumer leave" + str(SHARE_QUEUE))
                product = SHARE_QUEUE.pop()
                get_download_url(product)
            CONDITOIN.notify()
            CONDITOIN.release()
            time.sleep(random.random())
        print("Consumer's work is done!")

meat_collect_done = False

class Meat(threading.Thread):
    def run(self):
        global download_link, done, SHARE_QUEUE, meat_collect_done, begin, end
        while not meat_collect_done:
            CONDITOIN.acquire()
            if len(download_link):
                get_download_link(download_link.pop())
            else:
                print("  Download list is empty")
                CONDITOIN.wait()
                print("  Meats is on the way")
                if len(SHARE_QUEUE):
                    CONDITOIN.notify()
                    CONDITOIN.release()
                    time.sleep(0.05)
                if len(download_link) == 0 and done and len(SHARE_QUEUE) == 0:
                   #  print("Size: " + str(len(download_link))+ " " + str(len(SHARE_QUEUE)))
                    print("!!!!!!meat_collect_done")
                    meat_collect_done = True
                    print("begin: " + str(begin) + "end:" + str(time.ctime()))


def main():
    producer = Producer()
    consumer = Consumer()
    meat = Meat()
    # producer.daemon = True
    # consumer.daemon = True
    meat.daemon = True
    #main.daemon = True
    producer.start()
    consumer.start()
    meat.start()

if __name__ == "__main__":
    global begin
    begin = time.ctime()
    main()
