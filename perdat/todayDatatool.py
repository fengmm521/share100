#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-25 03:08:47
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import sys

sys.path.append('../')

import os
import codecs

import time
import shutil 


import numpy
import json

import nntensorflow

import DateTool
import pathtool


#将所有Excel文件转为xml文件
reload(sys)
sys.setdefaultencoding( "utf-8" )


dataDir = 'todaydata/tushare'

# tb ='-19,-17,-15,-13,-11,-9,-7,-5,-3,-2,-1,1,2,3,5,7,9,11,13,15,17,19'
tb = '-18,-14,-8,-5,-2,-1,1,2,5,8,14,18'

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
    fs = getAllExtFile(dataDir,'.csv')
    print fs[0]
    ids = []
    for d in fs:
        ids.append(d[2])
    return ids


def deSoftMaxFromLable(lab):
    pass




def getTureTableIndex(x,y,maxnum):
    n = (y*(2*maxnum + 1 - y))/2 + x
    return n


def getXYFromTureTable(idx,maxnum):

    dictab = {}
    for m in range(maxnum + 1):
        for n in range(maxnum + 1):
            if m >= n:
                tmp = getTureTableIndex(m, n, maxnum)
                dictab[tmp] = {'y':m,'x':n}
    # print dictab
    return dictab[idx]

def softMaxLable(mindown,maxup):
    #true table
    # tb ='-19,-17,-15,-13,-11,-9,-7,-5,-3,-2,-1,1,2,3,5,7,9,11,13,15,17,19'
    # tb = '-18,-14,-8,-5,-2,-1,1,2,5,8,14,18'
    truetables = tb.split(',')
    num = len(truetables)  #12x12=

    alllabnum = getTureTableIndex(num, num, num) + 1
    labs = [0]*alllabnum
    # print labs
    maxIndex = num
    minIndex = 0


    miny = min(mindown, maxup)
    maxx = max(mindown, maxup)

    mindown100 = miny*100
    maxup100 = maxx*100

    for n in range(num):
        tmpf = float(truetables[n])
        if minIndex == 0 and mindown100 < tmpf:
            minIndex = n
        if maxIndex == num and maxup100 < tmpf:
            maxIndex = n 
    # maxIndex += 1
    # minIndex += 1

    indx = getTureTableIndex(maxIndex, minIndex, num)

    labs[indx] = 1
    # print len(labs),alllabnum
    return labs

def getPerdatLable(onedat,labDayCount = 7):
    ldats = onedat[1]
    if not ldats:
        return None
    # print ldats
    maxclose = 0.0
    minclose = 99999.0
    for d in ldats:
        if d[1] > maxclose:
            maxclose = d[1]
        if d[2] < minclose:
            minclose = d[2]
    lastclose = onedat[0][-1][3]
    # print lastclose
    if lastclose <= 0:
        return None
    maxup = (maxclose - lastclose)/lastclose
    mindown = (minclose - lastclose)/lastclose

    labdat = softMaxLable(mindown, maxup)

    newperdat = []

    perdat = onedat[0]
    for d in perdat:
        tmp0 = (d[0] - lastclose)/(3*lastclose)
        if tmp0 >= 1.0:
            tmp0 = 1.0
        tmp1 = (d[1] - lastclose)/(3*lastclose)
        if tmp1 >= 1.0:
            tmp1 = 1.0
        tmp2 = (d[2] - lastclose)/(3*lastclose)
        if tmp2 >= 1.0:
            tmp2 = 1.0
        tmp3 = (d[3] - lastclose)/(3*lastclose)
        if tmp3 >= 1.0:
            tmp3 = 1.0
        tmpone = [tmp0,tmp1,tmp2,tmp3,d[4]]
        newperdat.append(tmpone)
    outdats = []
    outdats.append(newperdat)
    outdats.append(labdat)
    return outdats

def getPerdataWithOutLable(dat100,pDay):
    newperdat = []
    perdat = dat100
    if len(dat100) == 2:
        perdat = dat100[0]
    
    if len(perdat) != pDay:
        return

    lastclose = perdat[-1][3]
    if lastclose <= 0.0:
        return

    for d in perdat:
        tmp0 = (d[0] - lastclose)/(3*lastclose)
        if tmp0 >= 1.0:
            tmp0 = 1.0
        tmp1 = (d[1] - lastclose)/(3*lastclose)
        if tmp1 >= 1.0:
            tmp1 = 1.0
        tmp2 = (d[2] - lastclose)/(3*lastclose)
        if tmp2 >= 1.0:
            tmp2 = 1.0
        tmp3 = (d[3] - lastclose)/(3*lastclose)
        if tmp3 >= 1.0:
            tmp3 = 1.0
        tmpone = [tmp0,tmp1,tmp2,tmp3,d[4]]
        newperdat.append(tmpone)
    return newperdat


def saveListToFileWithJson(tpath,dats):
    savetxt = json.dumps(dats)
    f = open(tpath,'w')
    f.write(savetxt)
    f.close()

def loadListFromFileWithJson(tpth):
    f = open(tpth,'r')
    jsontxt = f.read()
    f.close()
    outlist = json.loads(jsontxt)
    return outlist


def getdataTypeList(handdat):

    tmphand = handdat.replace('\r','')
    tmphand = tmphand.replace('\n','')
    hands = tmphand.split(',')
    
    openidx = 0
    openstr = 'openPrice'

    highidx = 0
    highstr = 'highestPrice'

    lowidx = 0
    lowstr = 'lowestPrice'

    closeidx = 0
    closestr = 'closePrice'

    hslvidx = 0
    hslvstr = 'turnoverRate'

    for n in range(len(hands)):
        h = hands[n]
        if h.find(openstr) != -1:
            openidx = n
        if h.find(highstr) != -1:
            highidx = n
        if h.find(lowstr) != -1:
            lowidx = n
        if h.find(closestr) != -1:
            closeidx = n
        if h.find(hslvstr) != -1:
            hslvidx = n
    outs = [openidx,highidx,lowidx,closeidx,hslvidx]
    return outs

def createNNCOuntDayTmpData(tid,pDay,labDayCount):
    f = open(dataDir +'/' + tid + '.csv','r')
    datall = f.readlines()
    f.close()

    handidxs = getdataTypeList(datall[0])

    tmpd = datall[1:]
   
    if len(tmpd) < pDay:
        print '%s  data line number is not %d,is:%s:'%(tid,pDay,len(tmpd))
        return False


    #code,time,open,high,low,close,volume,turn,trate
    perdata = []   #per data is 100 lines,data from after to now
    lcount = len(tmpd)

    for n in range(len(tmpd)):
        if n+pDay <= lcount:
            ppdat = []
            for ln in range(n,n+pDay):
                tmpl = tmpd[ln]
                tmpl = tmpl.replace('\r','')
                tmpl = tmpl.replace('\n','')
                ds = tmpl.split(',')
                d1 = float(ds[handidxs[0]])
                d2 = float(ds[handidxs[1]])
                d3 = float(ds[handidxs[2]])
                d4 = float(ds[handidxs[3]])
                d5 = float(ds[handidxs[4]])
                ppdat.append([d1,d2,d3,d4,d5])
            perdata.append(ppdat)

    enddats = perdata[-1]
    zeroCount = 0
    for d in enddats:
        if d[0] == 0.0 and d[1] == 0.0 and d[2] == 0.0:
            zeroCount += 1


    if zeroCount >= 1:
        dirpth = 'todaydata/erro'
        if not os.path.exists(dirpth):
            os.mkdir(dirpth)
        saveerropth = dirpth + '/stopcode' + str(pDay) + '.txt'
        savestr = tid + ',' + str(zeroCount) +'\r\n'
        f = open(saveerropth,'a')
        f.write(savestr)
        f.close()
        if zeroCount > 3:
            print 'stop code is more than 3,tid:%s'%(tid)
            return False

    newsavedat = []

    for d in perdata:
        newppdat = getPerdataWithOutLable(d,pDay)
        if newppdat:
            newsavedat.append(newppdat)

    if not newsavedat:
        print 'not heave data to save:%s'%(tid)
        return False

    dirpath = '/media/mage/000FBF7E00093795/linuxfiles/perdata/todaydata/' + 'tmp' + str(pDay) + '_' + str(labDayCount)
    dirpath = 'todaydata/tmp' + str(pDay) + '_' + str(labDayCount)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    savepath = dirpath + os.sep + tid + '.txt'
    saveListToFileWithJson(savepath, newsavedat)


    dirpath = '/media/mage/000FBF7E00093795/linuxfiles/perdata/todaydata/' + 'pertmp' + str(pDay) + '_' + str(labDayCount)
    dirpath = 'todaydata/pertmp' + str(pDay) + '_' + str(labDayCount)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    savepath = dirpath + os.sep + tid + '.txt'
    saveListToFileWithJson(savepath, perdata)

    return True


def createNN100DayTmpData(tid,labDay = 5):
    return createNNCOuntDayTmpData(tid,100,labDay)


def createNN30DayTmpData(tid,labDay = 3):
    return createNNCOuntDayTmpData(tid,30,3)

def createNN10DayTmpData(tid,labDay = 3):
    return createNNCOuntDayTmpData(tid,10,3)
    
def conventXYToPecent(xydic):
    # tb = '-18,-14,-8,-5,-2,-1,1,2,5,8,14,18'
    x = xydic['x']
    y = xydic['y']
    
    out = ''
    tabs = tb.split(',')

    # print xydic
    # print len(tabs)

    if x == 0:
        out += 'min(-∞~%s%%),'%(tabs[x])
    elif x < len(tabs) - 1:
        out += 'min(%s%%~%s%%),'%(tabs[x-1],tabs[x])
    else:
        out += 'min(%s%%~+∞),'%(tabs[x-1])

    if y == 0:
        out += 'max(-∞~%s%%)'%(tabs[y])
    elif y < len(tabs) - 1:
        out += 'max(%s%%~%s%%)'%(tabs[y-1],tabs[y])
    else:
        out += 'max(%s%%~+∞)'%(tabs[y-1])

    return out

def trainTodayData(tid,pDay,lcount):

    opentxtdat = 'todaydata/tmp' + str(pDay) + '_' + str(lcount) + '/' + tid + '.txt'

    if not os.path.exists(opentxtdat):
        print 'not heave file:%s'%(opentxtdat)
        return

    f = open(opentxtdat,'r')    
    datstr = f.read()
    f.close()
    dats = json.loads(datstr)
    print len(dats)
    # print len(dats[0])
    # outdats = nntensorflow.getTrainResult(dats[-1], tid)
    outdats = nntensorflow.getTrainResultNewOP(dats[-1], tid)
    if outdats == None or (not outdats.size):
        print 'not train net data for tid:%s'%(tid)  
        dirpth = 'todaydata/erro'
        if not os.path.exists(dirpth):
            os.mkdir(dirpth)
        saveerropth = dirpth + '/notNetCode' + str(pDay) + '.txt'
        savestr = tid + ',notNetCode' +'\r\n'
        f = open(saveerropth,'a')
        f.write(savestr)
        f.close()
        return  

    outsort = []

    for n in range(len(outdats)):
        outsort.append([n,outdats[n]])
    # print outsort

    outsort.sort(key=lambda x:x[1], reverse=True)
    print outsort[0:3]

    outxy = []
    for d in outsort:
        otmp = getXYFromTureTable(d[0], 12)
        outpecent = conventXYToPecent(otmp)
        dpecent = '%.6f'%((d[1]/1.0)*100)
        outxy.append([tid,dpecent,otmp,outpecent])
    print outxy[0:3]


    outstr = ''
    for d in outxy:
        outstr += d[0] + ',' + d[1] + ',' + str(d[2]['x'])  + ',' +str(d[2]['y']) + ',' + str(d[3]) + '\n'

    todaynumdate = DateTool.getNowNumberDate()

    outpth = 'nnout/' + str(todaynumdate)
    if not os.path.exists(outpth):
        pathtool.makeDirs('.', outpth)

    savepth = outpth + '/' + tid + '.csv'
    
    f = open(savepth,'w')
    f.write(outstr)
    f.close()


def test2():
    trainTodayData('000050')

def test():
    createNN100DayTmpData('000050')

def main():
    ids = getAllQFQDataID()

    dirpth = 'todaydata/erro'
    if os.path.exists(dirpth):
        shutil.rmtree(dirpth)

    trainCount = 0

    index = 0
    for t in ids:
        index += 1
        print index,t
        if createNN100DayTmpData(t,5):
            time.sleep(0.2)
            trainTodayData(t,100,5)
            trainCount += 1

    print 'train count:',trainCount

def testWithID(tid):
    createNN100DayTmpData(tid,5)
    time.sleep(1)
    trainTodayData(tid,100,5)


if __name__ == '__main__':  
    main()
    # testWithID('002341')
    
    