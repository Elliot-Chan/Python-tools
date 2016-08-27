#!/usr/bin/env python3
# coding=utf-8

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

red_color = "\x1B[%d;%d;%dm" %(7, 30 ,41)
url = "http://dict.youdao.com/w/"

def encode_word(word):
    return urllib.parse.quote(word)

def get_translate_page(word):
    global result
    keyword = encode_word(word)
    if not len(keyword):
        return
    html = urllib.request.urlopen(url+keyword)
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find(id="results-contents")
    error = result.findAll(class_="error-wrapper")
    if not len(error):
        return result.findAll(class_="trans-container")
    deal_error_result(result, keyword)
    return len(error)

def get_web_result():
    global result
    web = result.find(id="tWebTrans").find_all(class_="wordGroup")
    print("\nphrase:")
    for each in web:
        print(" ", each.contents[1].a.contents[0])
        print ("  ", str(each.contents[2]).replace("\n",'').replace(" ", ''))

def get_base_result(keyword, need_phrase):
    page = get_translate_page(keyword)
    if not isinstance(page, int):
        base_result = page[0]
        for child in base_result.findAll("li"):
            print("  ", end='')
            print(child.contents[0])
        has_addition = base_result.p
        if not has_addition:
            if need_phrase:
                get_web_result()
            return 
        addition = str(has_addition.contents[0]).strip('[').strip(']').replace(' ', '')
        count = 0
        for each in addition.split('\n'):
            if len(each):
                if count % 2:
                    print("  ", end='')
                    print(each.strip(" ") + ': ', end='')
                else:
                    print("  ", end='')
                    print(each.replace(" ",''))
            count += 1
        if need_phrase:
            get_web_result()
    else:
        pass


def deal_error_result(result, keyword):
    print("%s Not found word: %s\x1B[0m" % (red_color, keyword))
    print("Maybe you want to query follow words ")
    for rel in result.findAll(class_="typo-rel"):
        print("  ", end='')
        print(str(rel.contents[1].a.contents[0]), end=' ')
        print((str(rel.contents[2]).replace("\n", '').replace(" ",'')))


if __name__ == "__main__":
    print("Please use translate.py")
