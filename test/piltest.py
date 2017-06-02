#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
from PIL import Image

#创建图片，默认为png格式图片,RGBA,创建的图为透明图片
def createNewImage(w,h): 
    nimg = Image.new('RGBA',(w,h),(0,0,0,0))
    return nimg
#将一张小图粘贴到一张大图中
def copyImgToOutImg(bigimg,inputimg,point):
    x = point[0]
    y = point[1]
    box = (0,0,inputimg.size[0],inputimg.size[1])
    offset = (x,y,x + inputimg.size[0], y + inputimg.size[1])
    region = inputimg.crop(box)
    bigimg.paste(region, offset)

im = Image.open("image/ziti_0.png")
nimg = createNewImage(1024,1024)

copyImgToOutImg(nimg, im, (500,150))
nimg.save('test.png')