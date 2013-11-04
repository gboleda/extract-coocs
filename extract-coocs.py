#!/opt/python/bin/python2.7
###!/usr/bin/python
# -*- coding: utf-8 -*-

# program to extract co-occurrences between a given set of targets and dims
# in the malt-parsed bnc, ukwac, wackypedia corpora
# Takes corpus directory, targets, dims as arguments, outputs each cooc (target TAB dim) to stdout.
# created gbt, Oct 2012

### import
import sys
from datetime import datetime
from procmalt import Sentence, Node, token_type, buildPhrase
import math
import gzip
import os
import getopt
#import re

### functions ###

def usage():
    usage='''
Program to extract co-occurrences between a given set of targets and dims from malt-parsed corpora.
Arguments: [corpus-dir] [target-file] [dim-file] [target-type (W for 'lemma-shortpos', L for 'lemma', P for 'phrase')]
\tOptionally accepts -d or --debug flag (verbose output), -h or --help flags.
Processes all gz files in corpus-dir. Output to stdout, messages to stderr.
Output: each cooc token (target-pos TAB dim-pos / target TAB dim depending on options).
Example calls:
WORDS: python extract-coocs.py -d /mnt/cimec-storage-sata/users/marco.baroni/share/ukwac-maltparsing/data ../data/counts/targets.4Kj.8Kn ../data/counts/dims-with-freq.10300 W
PHRASES: python extract-coocs.py /mnt/cimec-storage-sata/users/marco.baroni/share/ukwac-maltparsing/data ../data/counts/ans /u/gboleda/resources/bnc-ukwac-wacky.10K.cols P
'''
    sys.stderr.write(usage)

# input example:
#provide-v_information-n
#provide-v_service-n

def findSSElems(sent):
    '''Returns a list of targets and a list of dims for a sentence'''
# todo: produce list of nodes instead of list of lemmas (such that we can move between lemma and lemma-pos level; now we're doing a hack)
    global _debug
    targets = []; diml = []
    if _debug == 1: print(sent)
    for i in sent.nodelist[1:]: # we exclude the root
        prototarget = ''; phrasePrototarget = ''; protodim=''
        s = i.return_shortPOS()
        if _debug == 1: print("\t"+str(i)+"\tshortpos: " + s)
        if s != None: # determiners etc do not have a shortpos for now (fix)
            prototarget = i.return_lemmapos() # build lemma-pos form (eg "small-j")
            protodim = prototarget # we only work with lemma-pos dims for the moment
            if targetType == 'P':
                # if s == 'j':
                #     phrasePrototarget = buildAN(i, i.parent, i.parent.parent)
                if s == 'n':
                    phrasePrototarget = buildVerbObject(i, i.parent)
            elif targetType == 'L':
                prototarget = i.lemma
        if protodim in dimSet:
            diml.append(protodim)

        if targetType == 'P': # targets are then adj-j_noun-n
            prototarget = phrasePrototarget

        if prototarget in targetSet:
            targets.append(prototarget)

    return(targets,diml)

def buildVerbObject(daughterNode, parentNode):
    '''Returns a verb-object phrase, if present, otherwise the empty string. Requires 2 args (node and its parent node).'''
    global _debug
    aux = ''
    nodesp = daughterNode.return_shortPOS()
    parentsp =parentNode.return_shortPOS()
    if nodesp == 'n' and daughterNode.func == "OBJ":
        if parentsp == 'v':
            aux = buildPhrase([parentNode, daughterNode])
    if _debug == 1:
        if aux != '': print("Phrase: " + aux)
    return aux

def buildAN(adjNode, parentNode, grandpaNode):
    '''Returns an AN phrase, if present, otherwise the empty string. Requires 3 args.'''
    global _debug
    aux = ''
    asp = adjNode.return_shortPOS()
    parentsp =parentNode.return_shortPOS()
    grandpasp = grandpaNode.return_shortPOS()
    # in theory we already know that adjNode is an adj when we call this, but just in case
    if asp == 'j' and adjNode.func == "NMOD":
        if parentsp == 'n':
            aux = buildPhrase([adjNode,parentNode])
    elif asp == 'j' and adjNode.func == "COORD":
        if grandpasp == 'n':
            aux = buildPhrase([adjNode,grandpaNode])
    if _debug == 1:
        if aux != '': print("Phrase: " + aux)
    return aux

def printCoocs(targ, dim):
    global _debug
    targetsinsent = {}
    if _debug == 1:
        print(" * targets: " + str(targ))
        print(" * dims: " + str(dim))

    for targetword in targ:
        tlist = []
        # I check coocs of something with itself based on the words, even if the targets are phrases
        if targetType == 'P': tlist = targetword.split('_')
        else: tlist = [targetword]
        if _debug==1: print("Discounting target elems " + str(tlist))

        for d in dim:
            #if _debug==1: print("dim=" + str(d))
            dimnopos=''
            isCooc = True
            if targetType == 'L':
                dimnopos = d.split('-')[0]
                #if _debug==1: print("\tdimnopos=" + str(dimnopos))
            for t in tlist:
                #if _debug==1: print("\ttarget=" + str(t))
                # cooc with itself are barred
                if targetType == 'L':
                    if dimnopos == t:
                        targetsinsent[t] = targetsinsent.get(t,0) + 1
                    # but only the first time (if multiple occ of target in sent, it is indeed a cooc)
                        if targetsinsent[t] == 1: isCooc = False
                        #if _debug==1: print("\t\tTarget = dim; occurrence number " + str(targetsinsent[t]))
                else:
                    if d == t:
                        targetsinsent[t] = targetsinsent.get(t,0) + 1
                    # but only the first time (if multiple occ of target in sent, it is indeed a cooc)
                        if targetsinsent[t] == 1: isCooc = False
            if isCooc == True:
                cooc = targetword+"\t"+d+"\n"
                sys.stdout.write(cooc)
        targetsinsent.clear()

def process(c):
    '''read corpus and output each cooc between elements in targetdir and dimdir in a sentence'''
    global _debug
    if _debug == 1: print("Corpus "+c)
    f = gzip.open(c)
    s_id = 0; i = 0
    within_sent = False
    # empty sentence to make sure it exists when first token is assigned
    newsent = Sentence(s_id)
    for line in f:
        i = i + 1
#        if _debug == 1: if s_id > 100: sys.exit()
        iamin = "token: " + str(i)+ "\n\t"
        if token_type(line) == "sentencebegin":
            if not within_sent == True: # errors in the corpus coding...
                s_id=s_id+1  # count sentences
                newsent = Sentence(s_id) # sentence id
                within_sent = True
                if s_id%50000 == 0:
                    sys.stderr.write("sentence: " + str(s_id) + " of corpus " + c +"\n")
        elif token_type(line) == "sentenceend": # process sentence and flush
            within_sent = False # finish sentence
            try:
                newsent.assign_parents() # and construct dependencies
            except IndexError, ierr: # when a node cannot be created in an otherwise ok sentence, it will raise an IndexError when assigning parents (cause it was not added to the sentence)
                sys.stderr.write(str(ierr) + "\n\t---in sentence " + str(newsent) + "\n")
            else: # if everything went well
                # here's where the action happens
                (targets,dims) = findSSElems(newsent)
                if not targets == []: # do not seek coocs in sentences with no targets
                    printCoocs(targets,dims)
        elif token_type(line) == "word":
            try:
                node = Node(inputl=line)
            except RuntimeError, err:
                sys.stderr.write(str(err))
            else:
                # we only append nodes to sentences which have a proper "begin" tag
                if within_sent == True:
                    newsent.append_node(node)
        elif token_type(line) == False:
            sys.stderr.write("* Reached EOF *\n")

### main ###
a = datetime.now()

### 0. Process command line arguments

_debug = 0
argv = sys.argv[1:] # we exclude the name of the script
try:
    opts, args = getopt.getopt(argv, "hd", ["help","debug"])
except getopt.GetoptError:
    usage()
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt in ('-d', '--debug'):
        _debug = 1
    else:
        sys.stderr.write("Error: unrecognized option: " + str(opt) + "\n")
        usage()
        sys.exit()

if len(args) != 4:
    sys.stderr.write("Error: Invalid number of arguments: ")
    sys.stderr.write(str(len(args))+"\n")
    usage()
    sys.exit()

corpusDir = args[0]
targetFile = args[1]
dimFile = args[2]
targetType = args[3]
if not (targetType == 'W' or targetType == 'P' or targetType == 'L'):
    sys.stderr.write("Error: Invalid target type: "+targetType)
    usage()
    sys.exit()

### 1. Load dim file
dimSet = set()
dimF = open(dimFile,"r")
for line in dimF.readlines():
    word = line.split("\n")[0].split("\t")[0]
    dimSet.add(word)
dimF.close()
sys.stderr.write("Dim file " + dimFile + " loaded\n")

### 2. Load target file
targetSet = set()
targetF = open(targetFile,"r")
for line in targetF.readlines():
    word = line.split("\n")[0].split("\t")[0]
    targetSet.add(word)
targetF.close()
sys.stderr.write("Target file " + targetFile + " loaded\n")

sys.stderr.write("Number of dims/columns: " + str(len(dimSet)) + "\n")
sys.stderr.write("Number of targets/rows: " + str(len(targetSet)) + "\n")

### 3. Process corpora
for corpusfile in os.listdir(corpusDir):
     if corpusfile.endswith(".gz"):
         s = os.path.join(corpusDir, corpusfile)
         sys.stderr.write("Processing file " + s + "\n")
         process(s)

b = datetime.now()
c = b - a
sys.stderr.write("Time spent (hours):" + str(c.seconds/3600) + "\n")
