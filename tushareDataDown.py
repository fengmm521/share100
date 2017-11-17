#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-25 03:08:47
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import codecs
import sys
import xlrd
import time
import urllib2
import socket  
import shutil 

import IDManger
import pathtool

import random

import tushare as ts

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


import tushare as ts


tudataDir = 'perdat/tudata'
sdate = '20000101'
edate = '20171025'

gdates = ['20000101','20021231','20051231','20081231','20111231','20141231','20171025']

def makeTudataDir():
    if not os.path.exists(tudataDir):
        pathtool.makeDir('.', 'perdat/tudata')

def createSNDates():
    outs = []
    for n in range(len(gdates)):
        if n+1 < len(gdates):
            s = gdates[n]
            e = gdates[n+1]
            s = s[0:4] + '-' + s[4:6] + '-' + s[6:]
            e = e[0:4] + '-' + e[4:6] + '-' + e[6:]
            outs.append([s,e])
    return outs

#all QFQ data
def getAllIDsHFQData():
    makeTudataDir()
    sndates = createSNDates()
    print sndates

    ids = IDManger.getAllIDs()

    isSNstart = False

    for d in ids:
        cvsfilename = tudataDir + os.sep + d + '.csv'
        print cvsfilename
        isSNstart = False
        for sn in sndates:
            print sn
            dat = ts.get_h_data(d,start=sn[0], end=sn[1]) #qian复权

            dat = dat.reset_index().sort_values('date',ascending=True)

            if os.path.exists(cvsfilename):
                dat = dat[1:]
                dat.to_csv(cvsfilename,mode='a',header=None)
            else:
                dat.to_csv(cvsfilename)
            time.sleep(random.randint(250, 350))
        time.sleep(random.randint(1, 5))

def main():

    #shutil.rmtree(dbDir)#删除目录下所有文件
    # dat = ts.get_hist_data('600848')
    # dat = ts.get_h_data('002337', autype='hfq') #后复权
    # dat = ts.get_industry_classified()            #获取行业分类
    # dat = ts.get_stock_basics()     #获取所有股票业绩
    # dat.to_excel('xlsx/tusharedat.xlsx')
    getAllIDsHFQData()



def test():
    for s in range(10):
        t = random.randint(1, 100)
        print t
    
if __name__ == '__main__':
    main()
