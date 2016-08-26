#!/usr/bin/env python
# coding=utf-8
import sys
import el_youdao

def is_chinese(char):
    if char >= u'\u4e00' and char <= u'\u9fa5':
        return True
    else:
        return False

if __name__ == "__main__":
    for word in sys.argv[1:]:
        print(word)
        if is_chinese(word):
            print('')
            print("Chinese to English is not avaliable now!")
            print('')
            continue
        el_youdao.get_base_result(word)
