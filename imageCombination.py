#!/usr/bin/python
#-*- coding: utf-8 -*-
#png8图片批量转png24
import os
import sys
from PIL import Image
import shutil
import math
#获取脚本路径
def cur_file_dir():
    pathx = sys.argv[0]
    tmppath,_file = os.path.split(pathx)
    if cmp(tmppath,'') == 0:
        tmppath = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(tmppath):
        return tmppath
    elif os.path.isfile(tmppath):
        return os.path.dirname(tmppath)
    
#获取父目录
def GetParentPath(strPath):
    if not strPath:
        return None;
    lsPath = os.path.split(strPath);
    if lsPath[1]:
        return lsPath[0];
    lsPath = os.path.split(lsPath[0]);
    return lsPath[0];

#获取所有界面的json文件列表
def getAllExtFile(pth,fromatx = ".erl"):
    jsondir = pth
    jsonfilelist = []
    for root, _dirs, files in os.walk(jsondir):
        for filex in files:          
            #print filex
            name,text = os.path.splitext(filex)
            if cmp(text,fromatx) == 0:
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
            elif fromatx == ".*" :
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
    return jsonfilelist


def getAllLevelDirs(dirpths):
    dirleves = []
    dirtmp = ''
    for d in dirpths:
        dirtmp += '/' + d
        dirleves.append(dirtmp)
    return dirleves

#创建ftp服务器目录，是否使用服务器决对路径
def makeDir(outpth,ndir,isTruePath = False):
    tmpdir = ''
    if ndir[0] == '/':
        tmpdir = outpth + ndir
    else:
        tmpdir = outpth + '/' + ndir
    print tmpdir
    if not os.path.exists(tmpdir):
        os.mkdir(tmpdir)

# 创建一个目录下的所有子目录到另一个目录
def createDirs(spth,tpth):
    files = getAllExtFile(spth,'.*')
    makedirstmp = []
    isOK = True
    # 分析所有要创建的目录
    tmpfpth = fpth
    for d in files:
        if d[1] != '/' and (not d[1] in makedirstmp): #创建未创建的目录层级
            tmpdir = d[1][1:]
            tmpleves = tmpdir.split('/')
            alldirs = getAllLevelDirs(tmpleves)
            for dtmp in alldirs:
                if not dtmp in makedirstmp:
                    makeDir(tpth,dtmp)
                    makedirstmp.append(dtmp)


#获取图片大小，isNoAlph，是否只读取非透明像素区域大小
def getImageRact(img,isNoAlph = True):
    w = img.size[0]
    h = img.size[1]
    ract = {'x':0,'y':0,'width':w,'height':h}
    if isNoAlph:
        tmpimg = list(img.convert('RGBA').getdata())
        tmpx0 = w
        tmpy0 = h
        tmpx1 = 0
        tmpy1 = 0
        for x in range(w):
            for y in range(h):
                if tmpimg[w*y + x][3] != 0:
                    if x <= tmpx0:
                        tmpx0 = x
                    if x >= tmpx1:
                        tmpx1 = x
                    if y <= tmpy0:
                        tmpy0 = y
                    if y >= tmpy1:
                        tmpy1 = y
        ract = {'x':tmpx0,'y':tmpy0,'width':tmpx1 - tmpx0 + 1,'height':tmpy1 - tmpy0 + 1,'w':w,'h':h}
    print ract
    return ract


#获取应该生成的大图面积
def getBigWidthAndHeightWithArea(area,maxw,maxh):
    tmpwh = math.sqrt(area)
    tmpx = 0
    eage = 1
    while True:
        if tmpwh > eage:
            tmpx += 1
            eage = 2 ** tmpx  #2的指数次
        else:
            break
    halfEage = eage // 2
    if maxw <= eage and maxh < eage:
        if area < halfEage * eage:
            return eage,halfEage,tmpx,tmpx-1
        else:
            return eage,eage,tmpx,tmpx
    elif maxw > eage:
        tmpx = 0
        eage = 1
        while True:
            if maxw > eage:
                tmpx += 1
                eage = 2 ** tmpx  #2的指数次
            else:
                break
        tmpy = tmpx
        halfEage = eage
        while True:
            if area // eage > halfEage:
                tmpy -= 1
                halfEage = 2 ** tmpy
            elif area // eage == halfEage:
                break
            else:
                tmpy += 1
                halfEage = 2 ** tmpy
                break
        return eage,halfEage,tmpx,tmpy
    elif maxh > eage:
        tmpx = 0
        eage = 1
        while True:
            if maxh > eage:
                tmpx += 1
                eage = 2 ** tmpx  #2的指数次
            else:
                break
        tmpy = tmpx
        halfEage = eage
        while True:
            if area // eage > halfEage:
                tmpy -= 1
                halfEage = 2 ** tmpy
            elif area // eage == halfEage:
                break
            else:
                tmpy += 1
                halfEage = 2 ** tmpy
                break
        return halfEage,eage,tmpy,tmpx
    else:
        return eage,eage,tmpx,tmpx

#创建图片，默认为png格式图片,RGBA
def createNewImage(w,h): 
    nimg = Image.new('RGBA',(w,h),(0,0,0,0))
    return nimg

#复制一张图到大图中,box为小图在大图中的坐标，要求小图的box大小正好等于要帖贴的小图大小
def copyImgToOutImg(bigimg,inputimg,point):
    x = point[0]
    y = point[1]
    box = (0,0,inputimg.size[0],inputimg.size[1])
    offset = (x,y,x + inputimg.size[0], y + inputimg.size[1])
    region = inputimg.crop(box)
    bigimg.paste(region, offset)

#由所有图片的大小估算合成大图后小图片坐标,合成图会去掉透明像素,以减小合成图大小
def calculateImagesPoint(imgSizeDics,isNoAlph = True):
    bigImgSize = {'width':0,'height':0}
    newImgRects = {}    #新的小图在大图中的相对坐标和长宽,实际图片的长宽和有效像素坐标
    imgAreas = {}       #图片面积
    totalArea = 0       #计算所有图片总面积
    for k in imgSizeDics.keys():
        w = imgSizeDics[k]['width']
        h = imgSizeDics[k]['height']
        tmpArea = w * h
        imgAreas[k] = tmpArea
        totalArea += tmpArea

    imgAreasList = sorted(imgAreas.iteritems(), key=lambda d:d[1], reverse = True)        #图片按面积从大到小排序
    imgWList = sorted(imgSizeDics.iteritems(), key=lambda d:d[1]['width'], reverse = True)       #图片按宽度从大到小排序
    imgHList = sorted(imgSizeDics.iteritems(), key=lambda d:d[1]['height'], reverse = True)       #图片按长度从大到小排序

    imgOKList = []      #已放入大图中的图片列表
    print '总面积:',totalArea
    
    print 128*256
    print '面积排序'
    print imgAreasList
    print '宽度排序'
    print imgWList
    print '高度排序'
    print imgHList
    print '生成大图长宽'
    weage,heage,w2,h2 = getBigWidthAndHeightWithArea(totalArea, imgWList[0][1]['width'], imgHList[0][1]['height'])
    print weage,heage,w2,h2



def combinationImages(imgdicpths):
    imgs = {}
    imgsizes = {}
    for k in imgdicpths.keys():
        img = Image.open(imgdicpths[k])
        imgs[k] = img
        imgsizes[k] = getImageRact(img)
    print imgsizes
    calculateImagesPoint(imgsizes)


def getAllImagePath(dirpth):
    outpths = {}
    allimgs = getAllExtFile(dirpth,'.png')
    for d in allimgs:
        tmp = dirpth + d[0]
        outpths[d[2]] = tmp
    print outpths
    return outpths

def main(fpth,outPth):
    if os.path.exists(outPth):
        shutil.rmtree(outPth)
    os.mkdir(outPth)
    createDirs(fpth,outPth)
    imgpths = getAllImagePath(fpth)
    combinationImages(imgpths)

if __name__ == '__main__':
    args = sys.argv
    fpth = ''
    outName = 'numberFnt'
    if len(args) == 2 :
        if os.path.isdir(args[1]) and os.path.exists(args[1]):
            fpth = args[1]
        else:
            print '输入图片路径出错'
    elif len(args) == 3 and os.path.isdir(args[1]) and os.path.exists(args[1]):
        fpth = args[1]
        outName = args[2]
        
    else:
        print '参数错误'
    print fpth
    print outName
    if fpth == '':
        main('fntimage','comImgOut')
    else:
        main(fpth,outName)