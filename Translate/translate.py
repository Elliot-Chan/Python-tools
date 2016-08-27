#!/usr/bin/env python
# coding=utf-8
import sys
import el_youdao

def is_chinese(char):
    if char >= u'\u4e00' and char <= u'\u9fa5':
        return True
    else:
        return False

def is_alpha(char):
    if (char >= u'\u0041' and char<=u'\u005a') or (char >= u'\u0061' and char<=u'\u007a'):
        return True
    else:
        return False

def is_digit(char):
    if char >= u'\u0030' and char<=u'\u0039':
        return True
    else:
        return False

def phrase(keyword):
    return keyword == "+"

if __name__ == "__main__":
    need_phrase= phrase(sys.argv[-1]) 
    for word in sys.argv[1:]:
        if word != sys.argv[-1] or not need_phrase:
            print(word)
            if not is_alpha(word) and not is_digit(word):
                print("Only support en-cn now!")
                if is_chinese(word):
                    print('')
                    print("Chinese to English is not avaliable now!")
                    print('')
                continue
            else:
                el_youdao.get_base_result(word, need_phrase)
                print("*********************************************")
