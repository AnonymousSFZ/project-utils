# -*- coding: UTF-8 -*-
from os import listdir
from os.path import isfile, join, exists

# CHANGE TO YOUR OWN DIRECTORY
label_src = r'Labels\001'
image_src = r'Images\001'
# CHANGE TO UNIX IF YOU'RE USING MAC OR LINUX
file_path_format = 'WIN' # possible values('UNIX','WIN')

dst = label_src + '(YOLO).txt'
fdst = open(dst, 'w')
onlyfiles = [f for f in listdir(label_src) if isfile(join(label_src, f))]

if file_path_format == 'WIN':
    slash = '\\'
elif file_path_format == 'UNIX':
    slash = '/'
else:
    raise ValueError('Invalid value for file_path_format')

for file in onlyfiles:
    fsrc = open(label_src + '\\' + file)
    outputString = image_src + '\\' + file.split('.')[0] + '.jpg '
    for line in fsrc.readlines():
        numbers = line.split()
        if len(numbers) == 1:
            continue
        for number in numbers:
            outputString += '%d,' % int(number)
        outputString += '%d ' % 1
    fsrc.close()
    fdst.write(outputString + '\n')
fdst.close()
