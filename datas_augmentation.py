# -*- coding: UTF-8 -*-
import cv2, re
import numpy as np
from os import listdir, mkdir
from os.path import isfile, join, exists

# IMAGE SOURCE AND DESTINATION
src_dir = r'Images\002'
flip_dir = src_dir + '(flip)'
gauss_dir = src_dir + '(gauss)'

def add_gauss_noise(image, mean=0, var=0.001):
    image = np.array(image/255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    low_clip = -1. if out.min() < 0 else 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out*255)
    return out

for dst_dir in [flip_dir, gauss_dir]:
    if not exists(dst_dir):
        mkdir(dst_dir)
onlyfiles = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]
for file in onlyfiles:
    if re.match(r'.*\.(jpg|jpeg)', file, re.I):
        img = cv2.imread(src_dir + '\\' + file)
        # flip
        flip_img = cv2.flip(img, 1)
        cv2.imwrite(flip_dir + '\\' + file.split('.')[0] + '(flip).jpg', flip_img)
        # gauss
        gauss_img = add_gauss_noise(img)
        cv2.imwrite(gauss_dir + '\\' + file.split('.')[0] + '(gauss).jpg', gauss_img)
