#!/usr/bin/env python
# coding=utf-8
import sys
import youdao
import os

def is_chinese(char):
    return char >= u'\u4e00' and char <= u'\u9fa5'

def is_alpha(char):
    return (char >= u'\u0041' and char<=u'\u005a') or (char >= u'\u0061' and char<=u'\u007a')

def is_digit(char):
    return char >= u'\u0030' and char<=u'\u0039'

def phrase(keyword):
    return keyword == "+"

if __name__ == "__main__":
    default_dir = "/home/Elliot/Python-tools/Translate/"
    if not os.path.exists(default_dir + "words"):
        os.makedirs(default_dir + "words")
    word = sys.argv[1]
    if len(sys.argv) == 3:
        if sys.argv[2] == "r":
            youdao.tr(default_dir, word, True)
        else:
            print("Only support "r" options now")
    else:
        try:
            with open(default_dir+"words/"+word+".time","r") as f:
                times = f.read()
                f.close()
        except FileNotFoundError:
            times = '0'
        finally:
            pass
        with open(default_dir+"words/"+word+".time","w") as f:
            times = str(int(times) + 1)
            f.write(times)
        youdao.tr(default_dir, word, False)
