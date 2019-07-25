# -*- coding: UTF-8 -*-
import re
import xml.etree.ElementTree as ET
from os import listdir, rename, mkdir
from os.path import isfile, join, exists

src = 'Images1.0/003'
path = 'images/train'

onlyfiles = [f for f in listdir(src) if isfile(join(src, f))]
for file in onlyfiles:
    if re.match(r'.*\.xml', file, re.I):
        tree = ET.parse(src + '/' + file)
        root = tree.getroot()
        filename = file.split('.xml')[0] + '.jpg'
        # root[1] - file name
        root[1].text = filename
        # root[2] - path
        root[2].text = path + '/' + filename
        tree.write(src + '/' + file)
