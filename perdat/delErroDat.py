#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-25 03:08:47
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import codecs
import sys
import time
import shutil 


sys.path.append('../')

import numpy
import json

import nntensorflow

#将所有Excel文件转为xml文件
reload(sys)
sys.setdefaultencoding( "utf-8" )

def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

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
def getAllExtFile(path,fromatx = ".txt"):
    jsondir = path
    jsonfilelist = []
    for root, _dirs, files in os.walk(jsondir):
        for filex in files:          
            #print filex
            name,text = os.path.splitext(filex)
            if cmp(text,fromatx) == 0:
                jsonArr = []
                rootdir = path
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
    return jsonfilelist


def beifenErroLog(fpth):
    pass


def getAllNanDataID(linedats):
    pass

def getAllSmallDataID(lineDats,limitMin):
    pass

def saveRemoveNanDatsID(nanlines):

    pass

def saveRemoveSmallDatsID(smallLines):
    pass


def main():
    pass
    
        

def test():


    pass



if __name__ == '__main__':  
    main()
    # test()
    