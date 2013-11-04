#!/opt/python/bin/python2.7
###!/usr/bin/python
# -*- coding: utf-8 -*-

# created gbt, Nov 2012

### import
import sys
from datetime import datetime
import math
import gzip
import os
import getopt
import re

### functions ###

def usage():#
    usage='''
Arguments: [file-sm-format-gzipped] [file-with-space-dimensions]
Program to convert a gzipped file in sparse matrix (sm) format to Dan's format.
Outputs to stdout.
Example call: 
''' + sys.argv[0] + ''' /u/gboleda/resources/CORE_SS.bnc-ukwac-wacky.min50.10K.plmi.sm.gz /u/gboleda/resources/bnc-ukwac-wacky.10K.cols
'''
    sys.stderr.write(usage)

### main ###
a = datetime.now()

### 0. Subs

def loadFile(f,l):
    elemF = open(f,"r")
    for line in elemF.readlines():
        word = line.split("\n")[0].split("\t")[0]
        # if _debug == 1: print(word)
        l.append(word)
        elemF.close()
    sys.stderr.write("Elem file " + f + " loaded\n")
    return l


def flush(dL,w,dD,):
    sys.stdout.write(w)
    for dim in dL:
        if dim in dD:
            sys.stdout.write("\t"+dim+"\t"+str(dD[dim]))
        else:
            sys.stdout.write("\t\t")
    sys.stdout.write("\n")

### 1. Process command line flags and arguments

argv = sys.argv[1:] # we exclude the name of the script
if len(argv) != 2:
    sys.stderr.write("Error: Invalid number of arguments: ")
    sys.stderr.write(str(len(argv))+"\n")
    usage()
    sys.exit()

totransform = argv[0]
dims = argv[1]

### 2. Main

### Load element files

dimListEmpty = []
dimList = loadFile(dims,dimListEmpty)
sys.stderr.write("Pool of dims: " + str(len(dimList)) + "\n")

### convert

totransformF = open(totransform,"r")
#totransformF = gzip.open(totransform,"r")
sys.stderr.write("Transforming file " + totransform + "\n")

# year-n  recapture-v     339.753763
# year-n  seed-v  68.887226
# use-v   use-v   1852605.809716
oword=''
dimDict = {}
for line in totransformF:
    (word, dim, score) = line.split("\n")[0].split("\t")
    if word == oword:
        dimDict[dim] = score
    else:
        # reset
        if oword != '':
            flush(dimList,oword,dimDict)
        dimDict.clear()
        # begin new word
        oword = word
        dimDict[dim] = score
flush(dimList,oword,dimDict)
totransformF.close()
sys.stderr.write("Done!\n")
