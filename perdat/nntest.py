#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-24 09:29:05
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
sys.path.append('../')

import json
import pathtool

import math
import numpy

import tensorflow as tf

from numpy.random import RandomState

batch_size = 100

hidlayerCount = 350

def runNN(inport,outport,dats,tid): #500,529

    
    datasize = len(dats)
    

    w1 = tf.Variable(tf.truncated_normal([inport,hidlayerCount],stddev = 0.1),name='w1')
    b1 = tf.Variable(tf.zeros([hidlayerCount]),name='b1')

    w2 = tf.Variable(tf.truncated_normal([hidlayerCount,outport]),name='w2')
    b2 = tf.Variable(tf.zeros([outport]),name='b2')

    x = tf.placeholder(tf.float32,[None,inport])

    keep_prob = tf.placeholder(tf.float32)

    hidden1 = tf.nn.relu(tf.matmul(x,w1) + b1)

    hidden1_drop = tf.nn.dropout(hidden1, keep_prob)

    y = tf.nn.softmax(tf.matmul(hidden1_drop,w2) + b2)

    y_ = tf.placeholder(tf.float32,[None,outport])


    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y),reduction_indices=[1]))
    # cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y)))

    train_step = tf.train.GradientDescentOptimizer(0.05).minimize(cross_entropy)
    # train_step = tf.train.AdamOptimizer(0.0001,epsilon=1e-08).minimize(cross_entropy)


    saver = tf.train.Saver({"w1":w1,"b1":b1,"w2":w2,"b2":b2})


    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)


        cross_entropy_log = ''


        STEPS = 40000
        for i in range(STEPS):
            start = (i * batch_size) % datasize
            end = min(start + batch_size,datasize)

            batch_xtmps = dats[start:end]
            batch_xs = []
            batch_ys = []
            for d in batch_xtmps:
                tmpxs = []
                for xx in d[0]:
                    tmpxs +=xx
                batch_xs.append(tmpxs)
                tmpys = [float(yi) for yi in d[1]]
                batch_ys.append(tmpys)
            sess.run(train_step,feed_dict={x:batch_xs,y_:batch_ys,keep_prob:0.75})

            if i % 1000 == 0:

                tbatch_xs = []
                tbatch_ys = []

                for td in dats:
                    tmpxs2 = []
                    for xx2 in td[0]:
                        tmpxs2 += xx2
                    tbatch_xs.append(tmpxs2)
                    tmpys2 = [float(yi2) for yi2 in td[1]]
                    tbatch_ys.append(tmpys2)

                total_cross_entropy = sess.run(cross_entropy,feed_dict={x:tbatch_xs,y_:tbatch_ys,keep_prob:1.0})
                print "After %d training step(s),cross entropy on all data is %g"%(i,total_cross_entropy)
                cross_entropy_log = "After %d training step(s),cross entropy on all data is:%g"%(i,total_cross_entropy)
                if math.isnan(total_cross_entropy):
                    break
        cross_entropy_log = tid + '->' + cross_entropy_log + '\n'

        f = open('erro/crosslog.txt','a')
        f.write(cross_entropy_log)
        f.close()
        savedirpth = 'nndata/' + tid

        if os.path.exists(savedirpth):
            pathtool.removeDirTree(savedirpth)
        if not os.path.exists(savedirpth):
            pathtool.makeDirs('.', savedirpth)
        savepth = savedirpth + '/' + tid + '.ckpt'
        savedpth = saver.save(sess, savepth)
        saveinout = savedirpth + '/' + tid + '.inout'


        outstr = str(inport) + ',' + str(outport)
        f = open(saveinout,'w')
        f.write(outstr)
        f.close()

        print 'Model %s saved in file:'%(tid),savedpth

        sess.close()


def testnn():

    # datasize = len(dats)

    # savedirpth = 'nndata/' + tid
    
    # inoutpth = savedirpth + '/' + tid + '.inout'
    # if not os.path.exists(inoutpth):
    #     print 'not save in and out p count:%s'%(inoutpth)
    #     return

    # f = open(inoutpth,'r')
    # tmpstr = f.read()
    # f.close()

    # inouts = tmpstr.split(',')
    # inport = int(inouts[0])
    # outport = int(inouts[1])

    inlist = [[3.0, 3.0, 3.0, 3.0, 3.0], [3.0, 3.0, 3.0, 3.0, 3.0]]

    indat = numpy.array(inlist)

    inx = tf.constant(indat,dtype=tf.float32)

    alist = [1,1,1,1,1,1,1,1,1,1]

    w1 = tf.constant(alist,shape=[2,5],dtype=tf.float32)

    blist = [2,2,2,2,2,2,2,2,2,2]

    b1 = tf.constant(blist,shape=[2,5],dtype=tf.float32)

    addout1 = tf.add(w1, b1)


    addout = tf.add(addout1, inx)
    # w1 = tf.Variable(tf.truncated_normal([inport,hidlayerCount],stddev = 0.1),name='w1')
    # b1 = tf.Variable(tf.zeros([hidlayerCount]),name='b1')

    # w2 = tf.Variable(tf.truncated_normal([hidlayerCount,outport]),name='w2')
    # b2 = tf.Variable(tf.zeros([outport]),name='b2')


    # batch_xtmps = dats

    # batch_xs = []

    # for d in batch_xs:
    #     tmpxs = []
    #     for xx in d:
    #         tmpxs +=xx
    #     batch_xs.append(tmpxs)


    # x = tf.constant(batch_xs,shape=[1,inport],dtype=tf.float32)

    # hidden1 = tf.nn.relu(tf.matmul(x,w1) + b1)

    # # hidden1_drop = tf.nn.dropout(hidden1, keep_prob)

    # y = tf.nn.softmax(tf.matmul(hidden1,w2) + b2)


    # # saver = tf.train.Saver()
    # tf.train.Saver({"w1":w1,"b1":b1,"w2":w2,"b2":b2})


    with tf.Session() as sess:
        wout = sess.run(addout)
        # savepth = savedirpth + '/' + tid + '.ckpt'
        # if not os.path.exists(savepth + '.meta'):
        #     print 'file (%s) is not existsis,not save model for tid:%s'%(savepth,tid)
        #     return

        # saver.restore(sess, savepth)

        # yout = sess.run(y)
        # saveoutpth = savedirpth + '/' + tid + '.txt'
        # if not os.path.exists('nnout'):
        #     os.mkdir('nnout')
        # f = open(saveoutpth,'w')
        # f.write(str(yout))
        # f.close()
        return wout


def main():
    a = testnn()
    print a
    print type(a)
    
if __name__ == '__main__':  
    main()
    # test()