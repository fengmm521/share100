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



def getAllNNoutDataID(dpth):
    fs = getAllExtFile(dpth,'.csv')
    print fs[0]
    ids = []
    for d in fs:
        ids.append(d[2])
    return ids


def getDicDatas(dirpth,ids):
    
    datdic = {}

    for d in ids:
        tmpfpth = dirpth + '/' + d + '.csv'
        f = open(tmpfpth,'r')
        lines = f.readlines()
        f.close()
        tmpdats = []
        for l in lines:
            tmpl = l.replace('\r','')
            tmpl = tmpl.replace('\n','')
            tmps = tmpl.split(',')
            tmpid = tmps[0]
            tmppencent = float(tmps[1])
            tmpminx = int(tmps[2])
            tmpmaxy = int(tmps[3])
            tmpminstr = tmps[4]
            tmpmaxstr = tmps[5]
            tmplines = [tmpid,tmppencent,tmpminx,tmpmaxy,tmpminstr,tmpmaxstr]
            tmpdats.append(tmplines)
        datdic[d] = tmpdats
    return datdic


def getOneList(datdic):

    outs = []

    for k in datdic.keys():
        tp = datdic[k][0][1]
        tmin = datdic[k][0][2]
        tmax = datdic[k][0][3]
        if tp > 1.2:
            outs.append([k,tp,tmin,tmax])

    return outs

def getSecendList(datdic):
    outs = []

    for k in datdic.keys():
        tp = datdic[k][1][1]
        tmin = datdic[k][1][2]
        tmax = datdic[k][1][3]
        if tp > 1.2:
            outs.append([k,tp,tmin,tmax])

    return outs

def getListWithMax(outs):

    tmplist = list(outs)

    tmplist.sort(key=lambda x:x[3], reverse=True)

    outlist = []
    for d in tmplist:
        if d[2] >= 5 and d[1] >= 10:
            outlist.append(d)
    return outlist


def getPencentMaxList(outs):
    tmplist = list(outs)

    tmplist.sort(key=lambda x:x[1], reverse=True)


    outlist = []

    for d in tmplist:
        if d[2] >= 5 and d[3] >= 9:
            outlist.append(d)
    return outlist

def getCrossLimitMin(fpth,lmin = 1.75):

    f = open(fpth,'r')
    lines = f.readlines()
    f.close()

    ids = []

    for l in lines:
        tmpl = l.replace('\r','')
        tmpl = tmpl.replace('\n','')
        tmps = tmpl.split(',')
        if lmin > float(tmps[1]) and float(tmps[1]) > 0.0:
            ids.append(tmps[0])

    return ids


def main():
    
    dirs = os.listdir('nnout')
    dirs.sort(reverse = True)
    print dirs
    dirpth = 'nnout/' + dirs[0]
    ids = getAllNNoutDataID(dirpth)

    eropth = 'erro/out/' + '20171108' + '/crosslog.csv'

    limitids = getCrossLimitMin(eropth,1.78)

    tmpids = []

    for i in ids:
        if i in limitids:
            tmpids.append(i)

    print 'tmpids count:',len(tmpids)

    datdic = getDicDatas(dirpth, tmpids)

    firstdats = getOneList(datdic)
    maxlist = getListWithMax(firstdats)
    penlist = getPencentMaxList(firstdats)

    tcount = 30

    max100 = maxlist[:tcount]
    pen100 = penlist[:tcount]

    secenddats = getSecendList(datdic)

    print 'secend count:%d'%(len(secenddats))

    maxlist2 = getListWithMax(secenddats)
    penlist2 = getPencentMaxList(secenddats)

    smax100 = maxlist2[:tcount]
    spen100 = penlist2[:tcount]

    print '----max%d----'%(tcount)
    print max100
    print '----pen%d----'%(tcount)
    print pen100
    print '----2max%d----'%(tcount)
    print smax100
    print '----2pen%d----'%(tcount)
    print spen100



def test():
    a = [1,'1','sss']
    print a

if __name__ == '__main__':  
    main()
    # test()
    