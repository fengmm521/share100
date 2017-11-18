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


dapandatas = {}

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



def getAllQFQDataID():
    fs = getAllExtFile('qfqdata','.csv')
    print fs[0]
    ids = []
    for d in fs:
        ids.append(d[2])
    return ids

def getListAverage(plist):
    arrtmp = numpy.array(plist)
    return numpy.mean(arrtmp)

def getListDerivativeForMaxAndMin(plist):
    maxpoints = []
    minpoints = []
    datasize = len(plist)
    ks = []
    for n in range(len(plist)):
        if n - 1 >= 0:
            tmpk = plist[n] - plist[n - 1]
            ks.append(tmpk)
        else:
            ks.append(0)

    for n in range(len(ks)):
        if n - 1 >= 0:
            if ks[n - 1] > 0 and ks[n] < 0:
                maxpoints.append(n)
            elif ks[n-1] == 0 and n > 2 and ks[n - 2] > 0 and ks[n] < 0:
                maxpoints.append(n)
            if ks[n - 1] < 0 and ks[n] > 0:
                minpoints.append(n)
            elif ks[n-1] == 0 and n > 2 and ks[n-2] < 0 and ks[n] > 0:
                minpoints.append(n)
    return minpoints,maxpoints


def getDataListWithCountAverage(plist,paverage):
    averalist = []
    datasize = len(plist)
    lid = 0
    hid = 0
    if paverage%2 == 1:
        lid = (paverage - 1)/2
        hid = lid + 1
    else:
        lid = paverage/2
        hid = lid
    for n in range(len(plist)):
        if n - lid >= 0 and n + hid < datasize:
            averatmp = getListAverage(plist[n - lid:n + hid])
            averalist.append(averatmp)
        else:
            averalist.append(0)
    return averalist

def getDataListWithCountAverageMinAndMax(plist,paverage):
    averlist = getDataListWithCountAverage(plist, paverage)
    minpoints,maxpints = getListDerivativeForMaxAndMin(averlist)
    return minpoints,maxpints

def getDapanPencent():
    dapanpth = '../xlsx/000001.dapan'
    f = open(dapanpth,'r')
    lines = f.readlines()
    f.close()

    lines = lines[1:]

    # dapandic = {}

    for l in lines:
        tmpl = l.replace('\r','')
        tmpl = tmpl.replace('\n','')
        tmps = tmpl.split(',')
        pencenttmp = float(tmps[9])
        chpencent = (pencenttmp + 10.0)/20.0
        if chpencent < 0:
            chpencent = 0.0
        if chpencent > 1.0:
            chpencent = 1.0
        dapandatas[tmps[0]] = [pencenttmp,chpencent,int(tmps[11])]

    

def conventDataForLables(fpth):

    #code,time,openprice,highprice,lowprice,closeprice,value,marketvalue,changerate

    f = open(fpth,'r')
    lines = f.readlines()
    f.close()

    onedatas = []
    prices = []       #price = (open + close)/2;price = (high + low)/2;price = hight,low;price = max(open,close),min(open,close)


    lines = lines[1:]
    for n in range(len(lines)):
        l = lines[n]
        tmpl = l.replace('\r','')
        tmpl = tmpl.replace('\n','')
        tmps = tmpl.split(',')
        tid = tmps[0]                   #code id
        if len(tid) == 8:
            tid = tid[2:]
        pdate = tmps[1]                 #date
        popen = float(tmps[2])          #openprice
        phigh = float(tmps[3])          #highprice
        plow  = float(tmps[4])          #lowprice
        pclose = float(tmps[5])         #closeprice
        pvalue = int(tmps[6])           #value gu
        pmarketvalue = int(tmps[7])     #marketvalue yuan
        pchangerate = float(tmps[8])    #changerate
        onedatas.append([n,tid,pdate,popen,phigh,plow,pclose,pvalue,pmarketvalue,pchangerate,0,0,0,0,0,0,0,0,0,0,0,0,0,dapandatas[pdate][0],dapandatas[pdate][1],dapandatas[pdate][2]])
        tmppriceOC = (popen + pclose)/2
        tmppriceHL = (phigh + plow)/2
        prices.append([n,tmppriceOC,tmppriceHL,phigh,plow,max(popen,pclose),min(popen,pclose)])

    datasize = len(prices)

    ocdatas = [x[1] for x in prices]
    oc5min,oc5max = getDataListWithCountAverageMinAndMax(ocdatas, 5)
    oc10min,oc10max = getDataListWithCountAverageMinAndMax(ocdatas, 10)
    oc20min,oc20max = getDataListWithCountAverageMinAndMax(ocdatas, 20)
    
    hldatas = [x[2] for x in prices]
    hl5min,hl5max = getDataListWithCountAverageMinAndMax(hldatas, 5)
    hl10min,hl10max = getDataListWithCountAverageMinAndMax(hldatas, 10)
    hl20min,hl20max = getDataListWithCountAverageMinAndMax(hldatas, 20)

    phdatas = [x[3] for x in prices]
    _ph5min,ph5max = getDataListWithCountAverageMinAndMax(phdatas, 5)
    _ph10min,ph10max = getDataListWithCountAverageMinAndMax(phdatas, 10)
    _ph20min,ph20max = getDataListWithCountAverageMinAndMax(phdatas, 20)
    pldatas = [x[4] for x in prices]
    pl5min,_pl5max = getDataListWithCountAverageMinAndMax(pldatas, 5)
    pl10min,_pl10max = getDataListWithCountAverageMinAndMax(pldatas, 10)
    pl20min,_pl20max = getDataListWithCountAverageMinAndMax(pldatas, 20)

    ocmaxdatas = [x[5] for x in prices]
    _ocmax5min,ocmax5max = getDataListWithCountAverageMinAndMax(ocmaxdatas, 5)
    _ocmax10min,ocmax10max = getDataListWithCountAverageMinAndMax(ocmaxdatas, 10)
    _ocmax20min,ocmax20max = getDataListWithCountAverageMinAndMax(ocmaxdatas, 20)
    ocmindatas = [x[6] for x in prices]
    ocmin5min,_ocmin5max = getDataListWithCountAverageMinAndMax(ocmindatas, 5)
    ocmin10min,_ocmin10max = getDataListWithCountAverageMinAndMax(ocmindatas, 10)
    ocmin20min,_ocmin20max = getDataListWithCountAverageMinAndMax(ocmindatas, 20)

    for n in range(len(onedatas)):
        if n in oc5min:
            onedatas[n][10] = -1
        if n in oc5max:
            onedatas[n][10] = 1
        if n in oc10min:
            onedatas[n][11] = -1
        if n in oc10max:
            onedatas[n][11] = 1
        if n in oc20min:
            onedatas[n][12] = -1
        if n in oc20max:
            onedatas[n][12] = 1
        if n in hl5min:
            onedatas[n][13] = -1
        if n in hl5max:
            onedatas[n][13] = 1
        if n in hl10min:
            onedatas[n][14] = -1
        if n in hl10max:
            onedatas[n][14] = 1
        if n in hl20min:
            onedatas[n][15] = -1
        if n in hl20max:
            onedatas[n][15] = 1
        if n in pl5min:
            onedatas[n][16] = -1
        if n in ph5max:
            onedatas[n][16] = 1
        if n in pl10min:
            onedatas[n][17] = -1
        if n in ph10max:
            onedatas[n][17] = 1
        if n in pl20min:
            onedatas[n][18] = -1
        if n in ph20max:
            onedatas[n][18] = 1
        if n in ocmin5min:
            onedatas[n][19] = -1
        if n in ocmax5max:
            onedatas[n][19] = 1
        if n in ocmin10min:
            onedatas[n][20] = -1
        if n in ocmax10max:
            onedatas[n][20] = 1
        if n in ocmin20min:
            onedatas[n][21] = -1
        if n in ocmax20max:
            onedatas[n][21] = 1

    for n in range(len(onedatas)):
        d = onedatas[n]
        if d[10] == -1:
            findid = n
            mindat = 9999.9
            for i in range(3):
                if mindat > min(onedatas[n - i][3],onedatas[n - i][6]):
                    mindat = min(onedatas[n - i][3],onedatas[n - i][6])
                    findid = n - i
            onedatas[findid][22] = -1
        if d[10] == 1:
            findid = n
            maxdat = 0.0
            for i in range(3):
                if maxdat < max(onedatas[n - i][3],onedatas[n - i][6]):
                    maxdat = max(onedatas[n - i][3],onedatas[n - i][6])
                    findid = n - i
            onedatas[findid][22] = 1

    return onedatas

def conventListWithCSV(plist):
    outstr = ''
    for d in plist:
        line = ''
        for x in d:
            line += str(x) + ','
        line = line[:-1]
        outstr += line + '\r\n'
    return outstr

def create100DayDatasWithLables():

    savedir = 'tmpqfqdata'

    if not os.path.exists(savedir):
        os.mkdir(savedir)

    getDapanPencent()

    ids = getAllQFQDataID()
    print len(ids)

    count = 0
    for i in ids:
        count += 1
        tid = i
        if len(i) == 8:
            tid = i[2:]
        tmpfpth = 'qfqdata/' + i + '.csv'
        tmpsavepth = savedir + os.sep + tid + '.txt'

        if not os.path.exists(tmpsavepth):
            labdatas = conventDataForLables(tmpfpth)
            labdatas = conventDataForLables(fpth)
            # jsonstr = json.dumps(labdatas)
            outstr = conventListWithCSV(labdatas)
            f = open(tmpsavepth,'w')
            f.write(outstr)
            f.close()
        else:
            print '%s is saved..'%(tid)
        if count%100 == 0:
            print 'convent count:--------------%d-------------'%(count)

def main():
    
    create100DayDatasWithLables()
        

def test():

    getDapanPencent()

    savedir = 'tmpqfqdata'

    if not os.path.exists(savedir):
        os.mkdir(savedir)
    # avera = getListAverage([1,2,3,4])

    # print avera
    fpth = 'qfqdata/SZ002802.csv'
    labdatas = conventDataForLables(fpth)
    # jsonstr = json.dumps(labdatas)
    outstr = conventListWithCSV(labdatas)
    f = open('tmpqfqdata/002802.csv','w')
    # f.write(jsonstr)
    f.write(outstr)
    f.close()

def test2():
    getDapanPencent()
    print len(dapandatas.keys())

if __name__ == '__main__':  
    # main()
    test()
    