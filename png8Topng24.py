#!/usr/bin/python
#-*- coding: utf-8 -*-
#png8图片批量转png24
import os
import sys
from PIL import Image
import shutil
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

def conventImgFromPng8ToPng24(imgPth,outPth):
    img = Image.open(imgPth)
    outimg = img.convert("RGBA")
    outimg.save(outPth)

def main(fpth,outPth):
    if os.path.exists(outPth):
        shutil.rmtree(outPth)
    os.mkdir(outPth)
    createDirs(fpth,outPth)
    imgpths = getAllExtFile(fpth,".png")
    print imgpths
    for p in imgpths:
      ipth = fpth + p[0]
      opth = outPth + os.sep + p[0]
      conventImgFromPng8ToPng24(ipth, opth)

if __name__ == '__main__':
    args = sys.argv
    fpth = ''
    outName = 'imagefont'
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
        main('numberImage','png24out')
    else:
        main(fpth,outName)