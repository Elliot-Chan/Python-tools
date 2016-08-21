#!/usr/bin/env python
# coding=utf-8
import subprocess

url = ''
with open("link", 'r') as f:
    for url in f.readlines():
        download = "axel -n 16 " + url.strip('\n')
        print(str(download))
        subprocess.call(str(download), shell=True)
