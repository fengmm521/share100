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
import json

sys.path.append('../')
sys.path.append('../../')
import DateTool


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





def getAllCrossLogData(fdat):
    fpth = fdat[0]
    fname = fdat[1]
    f = open(fpth,'r')
    lines = f.readlines()
    f.close()

    datdic = {}
    csvout = ''
    for l in lines:
        tmpl = l.replace('\n','')
        tmpl = tmpl.replace('\r','')
        tid = tmpl.split('-')[0]
        tfloat = tmpl.split(':')[1]
        if tfloat == 'nan':
            datdic[tid] = 0.0
            csvout += tid + ',0.0' + '\r\n'
        else:
            datdic[tid] = float(tfloat)
            csvout += tid + ',' + tfloat + '\r\n'

    print len(datdic.keys())

    nandic = {}
    big2dic = {}
    d1p75_2 = {}
    d1p5_1p75 = {}
    smal1p5dic = {}

    for k in datdic.keys():
        tmpf = datdic[k]
        if tmpf >=2:
            big2dic[k] = tmpf
        elif tmpf <2 and tmpf >=1.75:
            d1p75_2[k] = tmpf
        elif tmpf < 1.75 and tmpf >= 1.5:
            d1p5_1p75[k] = tmpf
        elif tmpf < 1.5 and tmpf > 0.0:
            smal1p5dic[k] = tmpf
        else:
            nandic[k] = tmpf

    print '> 2 count       :',len(big2dic.keys())
    print '[1.75,2.0),count:',len(d1p75_2.keys())
    print '[1.5,1.75),count:',len(d1p5_1p75.keys())
    print '(0,1.5),   count:',len(smal1p5dic.keys())
    print 'nan count    :',len(nandic.keys())

    todaynumdate = DateTool.getNowNumberDate()
    savepth = 'out/' + str(todaynumdate)
    if not os.path.exists(savepth):
        os.mkdir(savepth)
        cmd = 'cp %s %s\n'%(fpth,savepth)
        os.system(cmd)

    f = open(savepth + os.sep + fname + '.csv','w')
    f.write(csvout)
    f.close()

def getNoEnoughTIDs(fdat):
    fpth = fdat[0]
    fname = fdat[1]
    f = open(fpth,'r')
    lines = f.readlines()
    f.close()

    datdic = {}
    csvout = ''

    for l in lines:
        tmpl = l.replace('\n','')
        tmpl = tmpl.replace('\r','')
        tid = tmpl.split(',')[0]
        if len(tid) == 8:
            tid = tid[2:]
        count = int(tmpl.split(':')[1])
        datdic[tid] = count
        csvout += tid + ',' + str(count) + '\r\n'

    print len(datdic.keys())

    c1_30 = {}
    c30_100 = {}
    c100_300 = {}
    c300_600 = {}
    c600_900 = {}

    for k in datdic.keys():
        ctmp = datdic[k]
        if ctmp >= 600:
            c600_900[k] = ctmp
        elif ctmp < 600 and ctmp >= 300:
            c300_600[k] = ctmp
        elif ctmp < 300 and ctmp >= 100:
            c100_300[k] = ctmp
        elif ctmp <100 and ctmp >= 30:
            c30_100[k] = ctmp
        else:
            c1_30[k] = ctmp

    print '[600,900) count:',len(c600_900.keys())
    print '[300,600) count:',len(c300_600.keys())
    print '[100,300) count:',len(c100_300.keys())
    print '[30,100)  count:',len(c30_100.keys())
    print '[1,30)    count:',len(c1_30.keys())

    todaynumdate = DateTool.getNowNumberDate()
    savepth = 'out/' + str(todaynumdate)
    if not os.path.exists(savepth):
        os.mkdir(savepth)
        cmd = 'cp %s %s\n'%(fpth,savepth)
        os.system(cmd)

    f = open(savepth + os.sep + fname + '.csv','w')
    f.write(csvout)
    f.close()

def getAllFilesFromPth(dirPth = '.'):

    crossfs = []
    enenoughfs = []

    txts = getAllExtFile('.','.txt')

    for t in txts:
        if t[2].find('crosslog') != -1:
            tmppth = '.' + t[0]
            crossfs.append([tmppth,t[2]])

        elif t[2].find('noEnough') != -1:
            tmppth = '.' + t[0]
            enenoughfs.append([tmppth,t[2]])
    return crossfs,enenoughfs

def main():
    
    crofs,noefs = getAllFilesFromPth()


    print crofs
    print noefs
    
    if (crofs or noefs) and (not os.path.exists('out')):
        os.mkdir('out')

    for c in crofs:
        getAllCrossLogData(c)

    for n in noefs:
        getNoEnoughTIDs(n)


if __name__ == '__main__':  
    main()