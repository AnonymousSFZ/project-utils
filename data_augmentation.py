# -*- coding: UTF-8 -*-
import cv2, re
import numpy as np
from os import listdir, mkdir
from os.path import isfile, join, exists

# IMAGE SOURCE AND DESTINATION
src_dir = r'Images\004'
gauss_dir = src_dir + '(gauss)'
bright_dir = src_dir + '(bright30)'
dark_dir = src_dir + '(dark30)'
crop_dir = src_dir + '(crop)'

def add_gauss_noise(image, mean=0, var=0.001):
    image = np.array(image/255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    low_clip = -1. if out.min() < 0 else 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out*255)
    return out

def increase_brightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    if value > 0:
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
    else:
        v[v + value < 0] = 0
        v[v != 0] -= value*-1
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def resize_img(img, _height = 600):
    height, width, channels = img.shape
    if height != _height:
        ratio = _height / height
        img = cv2.resize(img, (0,0), fx=ratio, fy=ratio) 
    return img

def crop_and_resize(img):
    height, width, channels = img.shape
    crop1 = img[int(height*0.1):, :int(width*0.9), :]
    crop2 = img[:int(height*0.9), int(width*0.1):, :]
    crop1 = resize_img(crop1)
    crop2 = resize_img(crop2)
    return crop1, crop2

def main():
    # check for dst dir
    for dst_dir in [gauss_dir, bright_dir, dark_dir, crop_dir]:
        if not exists(dst_dir):
            mkdir(dst_dir)
    # flip
    safe = True
    onlyfiles = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]
    for file in onlyfiles:
        if not re.match(r'.*(flip).*', file):
            img = cv2.imread(src_dir + '\\' + file)
            img = resize_img(img)
            # flip
            flip_img = cv2.flip(img, 1)
            cv2.imwrite(src_dir + '\\' + file.split('.')[0] + '.jpg', img)
            cv2.imwrite(src_dir + '\\' + file.split('.')[0] + '(flip).jpg', flip_img)
    # gauss, cropped, etc
    onlyfiles = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]
    for file in onlyfiles:
        if re.match(r'.*\.(jpg|jpeg)', file, re.I):
            img = cv2.imread(src_dir + '\\' + file)
            # gauss
            gauss_img = add_gauss_noise(img)
            cv2.imwrite(gauss_dir + '\\' + file.split('.')[0] + '(gauss).jpg', gauss_img)
            # bright
            bright_img = increase_brightness(img, 30)
            cv2.imwrite(bright_dir + '\\' + file.split('.')[0] + '(bright30).jpg', bright_img)
            # dark
            dark_img = increase_brightness(img, -30)
            cv2.imwrite(dark_dir + '\\' + file.split('.')[0] + '(dark30).jpg', dark_img)
            # crop
            crop_img1, crop_img2 = crop_and_resize(img)
            cv2.imwrite(crop_dir + '\\' + file.split('.')[0] + '(crop1).jpg', crop_img1)
            cv2.imwrite(crop_dir + '\\' + file.split('.')[0] + '(crop2).jpg', crop_img2)
        
if __name__ == "__main__":
    main()
