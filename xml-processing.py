# -*- coding: UTF-8 -*-
import re
import xml.etree.ElementTree as ET
from os import listdir, rename, mkdir
from os.path import isfile, join, exists

def add_prefix(string, prefix):
    return string.split('.j')[0] + prefix + '.jpg'

src = 'Labels/Images1.0/003'
prefixs = ['(bright30)', '(dark30)', '(gauss)']

for prefix in prefixs:
        if not exists(src + prefix):
            mkdir(src + prefix)

onlyfiles = [f for f in listdir(src) if isfile(join(src, f))]
for file in onlyfiles:
    if re.match(r'.*\.xml', file, re.I):
        for prefix in prefixs:
            tree = ET.parse(src + '/' + file)
            root = tree.getroot()
            root[1].text = add_prefix(root[1].text, prefix)
            root[2].text = add_prefix(root[2].text, prefix)
            tree.write(src + '/' + file.split('.')[0] + prefix + '.xml')
