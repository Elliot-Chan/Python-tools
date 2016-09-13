#!/usr/bin/env python3
# coding=utf-8
import hashlib

src = input("Input: ")
key = input("Key: ")
password = []
m = str(hashlib.md5(src.encode('utf-8')).hexdigest())
for each in m:
    password.append(chr((ord(each) + int(key)) % 122))

for each in range(15):
    print(password[each], end='')
print()
