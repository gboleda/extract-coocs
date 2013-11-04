# created gbt, July 2011
# modified mcg, 2012/01/29
# modified gbt, November 2012
import sys

# classes and subs for distributional semantic work on malt-parsed corpora.

### classes ###

class Sentence:
    "Class for storing sentences (lists of nodes) and doing various operations with them"
    def __init__(self, idx=None):
        n = Node(nodetype='root') # ROOT node; index = 0, parent_index = -1
        self.nodelist = [n] # element 0 in nodelist: the ROOT node
        self.idx = idx

    def __str__(self):
        # ***mirar pprint
        sent = 'sent ' + str(self.idx) + ": "
        for i in self.nodelist[1:]: # we exclude the root node
            sent = sent + i.form + " "
        return sent

    def append_node(self,node):
        self.nodelist.append(node)

    def assign_parents(self):
        for node in self.nodelist:
            nid = int(node.parent_index)
            currentnode = self.nodelist[nid]
            node.set_parent(currentnode)

# ['The', 'the', 'DT', '1', '3', 'NMOD']
# ['major', 'major', 'JJ', '2', '3', 'NMOD']
# ['impact', 'impact', 'NN', '3', '4', 'SBJ']
# ['is', 'be', 'VBZ', '4', '0', 'ROOT']
# ['yet', 'yet', 'RB', '5', '7', 'ADV']
# ['to', 'to', 'TO', '6', '7', 'VMOD']
# ['come', 'come', 'VV', '7', '4', 'PRD']
# ['.', '.', 'SENT', '8', '4', 'P']
class Node:
    "Node class for storing nodes in MALT parser parsed sentences. Input: line in MALT parser format, except for nodetype root and empty. Output: Node object."

    def __init__(self, inputl=None, nodetype='token'):
        self.ntype=nodetype
        if inputl == None:
            if nodetype=='root':
                self.index = 0
                self.parent_index = -1
                self.form = ''
                self.lemma = ''
                self.POS = ''
                self.func = ''
            elif nodetype=='empty': # for empty nodes (type of node created for attribute self.parent below)
                self.form = "#empty" # for __str__ method in class Sentence
                self.parent_index = -1 # every node should have at least form and parent_index
            else:
                raise RuntimeError("Error: no attributes specified for this node of type " + str(nodetype) + ". Need a MALT-parsed line as input for those.\n")
        else:
            atts = inputl.split()
            ### Eg: etc.^K^KPlease  etc.^K^Kplease  NN      11      9       OBJ ###
            ### Split as: ['etc.', 'Please', 'etc.', 'please', 'NN', '11', '9', 'OBJ']
            if len(atts) == 8:
                self.form = atts[0] + atts[1]
                self.lemma = atts[2] + atts[3]
                self.POS = atts[4]
                self.index = atts[5]
                self.parent_index = atts[6]
                self.func = atts[7]
                self.parent = Node(nodetype='empty')

            elif len(atts) != 6:
                raise RuntimeError("Error: expecting 6 attributes\n\tAttributes: " + str(atts) + "\n")

            else:
                self.form = atts[0]
                self.lemma = atts[1]
                self.POS = atts[2]
                self.index = atts[3]
                self.parent_index = atts[4]
                self.func = atts[5]
                self.parent = Node(nodetype='empty')

    def __str__(self):
        mytype=self.ntype
        if mytype=='root' or mytype=='empty':
            return mytype
        else:
            return str(self.ntype + ": " + self.form + " " + self.lemma + " " + self.POS + " " + self.index + " " + self.parent_index + " " + self.func)

    def set_parent(self, parent_node):
        self.parent = parent_node


# classe PairAdj-Noun, ocurrencies
class Pair:
    "Pair class for storing Adj-Noun and #occurrences of these nodes in our corpus"
    
    def __init__(self, tup):
        if tup == None:
            sys.stderr.write("Error: no node for this node \n")
            return False
        else:
            self.tup = tup
            self.num = 1
    
    def __str__(self):
        return str(self.tup[0] + ";" + self.tup[1] + ";" + str(self.num))
    
    def getTup(self):
        return self.tup
    
    def add1(self):
        self.num = self.num + 1
        
    def getNum(self):
        return self.num

# General subs

def token_type(token):
    token_begin = token[:3]
    if token == "": # empty line
        return False
    elif token_begin == "<s>":
        return "sentencebegin"
    elif token_begin == "</s":
        return "sentenceend"
    elif token_begin == "<te":
        return "textbegin"
    elif token_begin == "</t":
        return "textend"
    else:
        return "word"

def ANsinSent(sent):
    '''Returns the list of pairs adj-noun in the sentence (adjective lemma, head noun lemma).'''
    olist = []
    for i in sent.nodelist[1:]:
        if i.POS[:2] == 'JJ' and i.func == "NMOD":
            if i.parent.POS[:2] == "NN":
                aux = i.lemma + "-j_" + i.parent.lemma + "-n"
                olist.append(aux) # for multiple occurrences of AN
        elif i.POS[:2] == 'JJ' and i.func == "COORD":
            if i.parent.parent.POS[:2] == "NN":
                aux = i.lemma + "-j_" + i.parent.parent.lemma + "-n"
                olist.append(aux)
    return olist

def buildAN(adjNode, parentNode, grandpaNode):
    aux = ''
    adjNode.set_shortPOS()
    parentNode.set_shortPOS()
    grandpaNode.set_shortPOS()
    a = adjNode.return_lemmapos()
    # in theory we already know that adjNode is an adj, but just in case
    if adjNode.shortPOS == 'j' and adjNode.func == "NMOD":
        if parentNode.shortpos == 'n':
            n = parentNode.return_lemmapos()
            aux = a + '_' + n
            if _debug ==1: print ('FOUND SIMPLE AN ', aux)
    elif adjNode.shortPOS == 'j' and adjNode.func == "COORD":
        if grandpaNode.shortpos == 'n':
            n = grandpaNode.lemma + "-n"
            aux = a + '_' + n
            if _debug ==1: print ('FOUND COORDINATED AN ', aux)

    return aux

def buildPhrase(nodelist):
    out = ''
    for node in nodelist:
        lp = node.return_lemmapos()
        out = out + '_' + lp
    return out
