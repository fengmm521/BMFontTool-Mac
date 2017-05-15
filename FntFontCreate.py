#!/usr/bin/python
#-*- coding: utf-8 -*-
import os,sys


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

images = []

class FntFontTool():
    """docstring for FTPTool"""
    def __init__(self,imagesPth, bmpFontName = "imagefont"):
        self.imageBasePth = imagesPth
        self.outFontPth = GetParentPath(imagesPth)
        self.imageSizes = {}			#所有文字图片大小,[长，宽]
        self.fontCodingIDs = {} 		#所有文字图片对应的uncode编码
        self.specialFontCodingIDs = {}  #不能作为文件名的文字编码，文件名将会使用这个字符的编码16进制数作为图片名
        self.allImagePths = {} 		    #所有文字的图片路径
        self.fonts = [] 				#要打包的文字
        self.outImageSize = None 		#要输出的字体图片大小,
        self.outImage = None  			#要输出的图片,png格式
        self.fontOutName = bmpFontName  #输出的字体名
        self.initAllDataWithImagePth()


    def getRealFontTxt(sefl,fileName):
        outtmp = ''
        if len(fileName) > 1 and fileName[:2] == '0x':
            pass
    #初始化转换数据
    def initAllDataWithImagePth(self):
    	ftmps = getAllExtFile(self.imageBasePth,".png")
    	nametmps = []       #图片名
        tmppath = []        #图片路径
        imagetmps = []      #图片内容
    	
    	for d in ftmps:
    		nametmps.append(d[2])
    	
    	print ftmps

    #初始化所有要打包的文字真名
    def conventImagePthToFont(self,imgPth): 
    	pass

    #计算最终生成图片大小
    def calcOutImageSize(self):
    	pass

    #生成fnt图片文字字体
    def createFntFont(self):
    	pass

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
    fontTool = FntFontTool(fpth,outName)
# qstr  = u"abc\u5023"
# qstr  = u"abc\u0041"
# qstr = u"abc\u6625"
# qstr = qstr.encode('utf-8')
# print qstr
# # qstr  = u"abc\u0032"
# qstr  = u"abc\u5023"
# qstr = qstr.encode('utf-8')
# print qstr

# x = 0x6625
# print x
# x = 0x5023
# print x

# a = u'我'
# tnu = repr(a)
# print 'tnu:' + tnu
# tin = str(tnu)
# print 'tin:' + tin
# print hex(ord(a))
# print ord(a)

# tmp = [u'零',u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九']
# for x in tmp:
# 	print repr(x) + ':%s'%(x.encode('utf-8'))
x = 0x6625
print repr(x)
print str(x)

