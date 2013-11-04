#!/lusr/bin/python
# -*- coding: utf-8 -*-

# program to extract phrases with given head, dependent, and dependency relation from
# the malt-parsed bnc, ukwac, wackypedia corpora
# head and dependent must be present in a given semantic space
# Takes corpus directory, target words, target phrases as arguments, 
# outputs each occurrence token (eg verb-v_noun-n TAB OBJ) to stdout.
# created gbt, Nov 2012

### import
import sys
from datetime import datetime
from procmalt import Sentence, Node, token_type
import math
import gzip
import os
import getopt
#import re

### functions ###

def usage():
    usage='''
Program to extract verb-object phrases with given Vs and Ns from malt-parsed corpora.
Arguments: [corpus-dir] [target-file] [dataset-file]
Computes all verb-object phrases where (1) verb AND noun are in target-file (2) verb OR noun is in dataset-file.
\tOptionally accepts -d or --debug flag (verbose output), -h or --help flags.
Processes all gz files in corpus-dir. Output to stdout, messages to stderr.
Output: each occurrence token (verb-v_noun-n).
Example call: python '''  + sys.argv[0] + ''' -d /scratch/cluster/gboleda/corpora/ /u/gboleda/resources/bnc-ukwac-wacky.min50.rows /u/gboleda/data/counts/targets.in.desai
'''
    sys.stderr.write(usage)

def outputPhrases(sent):
    global _debug
    if _debug == 1: print(sent)
    for i in sent.nodelist[1:]:
        aux = ''
        if _debug == 1: print(i)
        if i.POS[:2] == 'NN' and i.func == "OBJ":
            if i.parent.POS[0] == "V":
                dep = i.lemma + "-n"
                head = i.parent.lemma + "-v"
                aux = head + '_' + dep
                if head in targetSet and dep in targetSet:
                    if dep in datasetSet:
                        sys.stdout.write(aux + "\n")
                    elif head in datasetSet:
                        sys.stdout.write(aux + "\n")
                    if _debug == 1: print("SIMPLE in target:" + aux)
                else:
                    if _debug == 1:
                        print("SIMPLE NOT in target: " + aux)

def process(c):
    '''read corpus and output each occ of an Phrase with A and N in targetfile'''

    f = gzip.open(c)
    s_id = 0; i = 0
    within_sent = False
    # empty sentence to make sure it exists when first token is assigned
    newsent = Sentence(s_id)
    for line in f:
        i = i + 1
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
                outputPhrases(newsent)
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

### 0. Process command line flags and arguments

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
    elif opt == '-d':
        _debug = 1

if len(args) != 3:
    sys.stderr.write("Error: Invalid number of arguments: ")
    sys.stderr.write(str(len(args))+"\n")
    usage()
    sys.exit()

corpusDir = args[0]
targetFile = args[1]
datasetFile = args[2]

### 1. Load target file
targetSet = set()
targetF = open(targetFile,"r")
for line in targetF:
    word = line.split("\n")[0].split("\t")[0]
    targetSet.add(word)
targetF.close()
sys.stderr.write("Target file " + targetFile + " loaded\n")
#sys.stdout.write(str(targetSet))
sys.stderr.write("Number of targets/rows: " + str(len(targetSet)) + "\n")

### 2. Load dataset file
datasetSet = set()
datasetF = open(datasetFile,"r")
for line in datasetF:
    word = line.split("\n")[0].split("\t")[0]
    datasetSet.add(word)
datasetF.close()
sys.stderr.write("Dataset file " + datasetFile + " loaded\n")
#sys.stdout.write(str(datasetSet))
sys.stderr.write("Number of words in dataset: " + str(len(datasetSet)) + "\n")

### 3. Process corpora

for corpusfile in os.listdir(corpusDir):
     if corpusfile.endswith(".gz"):
         s = os.path.join(corpusDir, corpusfile)
         sys.stderr.write("Processing file " + s + "\n")
         process(s)

# s = os.path.join(corpusDir, corpusFile)
# sys.stderr.write("Processing file " + s + "\n")
# process(s)

