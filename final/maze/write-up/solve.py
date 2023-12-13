#!/usr/bin/env python

import re
import requests
import binascii

def xget(path,liste):

    request = requests.get(path).text

    if "flag" in request:
        liste.append(path)
        return

    for match in re.finditer(r'href=\"(\w+)/\"', request):
        regex = match.group(1)
        new_path = path + "/" + regex

        if regex not in path: #traitement des liens symboliques
            xget(new_path,liste)


liste = []
xget("http://127.0.0.1:1234", liste)

liste.sort(key=len) # trie croissant sur la longueur des items de liste

flag = ""

for x in liste:
    path = x + "/flag.txt"
    request = requests.get(path)
    txt = request.text
    flag = flag + txt

print(binascii.unhexlify(flag))

