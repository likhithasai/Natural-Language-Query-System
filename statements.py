# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
        # word_list is a list for adding word stem
        self.word_list = []
    def add(self, stem, cat):
        # appends the stem and cat to word_list as a list
        self.word_list.append((stem,cat))
    def getAll(self, cat):
        # Make the word_list a set to remove duplications
        # and match the cat value to obtain all words
        w_lst = []
        set_word_list = set (self.word_list)
        for word_stem in set_word_list:
            if word_stem[1] == cat:
                add (w_lst,word_stem[0])
        return w_lst

class FactBase:
    """stores unary and binary relational facts"""
    def __init__(self):
        self.unary_facts = []
        self.binary_facts = []
    def addUnary(self,pred,e1):
        self.unary_facts.append((pred,e1))
    def addBinary(self, pred, e1, e2):
        self.binary_facts.append((pred,e1,e2))
    def queryUnary(self, pred, e1):
        flag = 0
        for ufact_list in self.unary_facts:
            if (ufact_list[0] == pred and ufact_list[1] == e1):
                flag = 1
        if flag == 0:
            return False
        else:
            return True
    def queryBinary(self,pred, e1, e2):
        flag = 0
        for bfact_list in self.binary_facts:
            if (bfact_list[0] == pred and bfact_list[1] == e1 and bfact_list[2] == e2):
                flag = 1
        if flag == 0:
            return False
        else:
            return True

import re
from nltk.corpus import brown
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    vowel_s = "aieou"
    verb = ""
    if re.match(".*ies$",s):
        if len(s) == 4 and not s[0] in vowel_s:
            verb = s[:-1]            #working
        else:
            verb = s[:-3] + 'y'      #working
    elif re.match(".*es$",s):
        if re.match(".*(o|x|sh|ch|ss|zz)es$",s):
            verb = s[:-2]
        elif re.match(".*[^(sxyz)]es$",s) and s[-4:-2] != "sh" and s[-4:-2] != "ch":
            verb = s[:-1]
        elif re.match(".*(([^s]s)|([^z]z))es$",s):
            verb = s[:-1]
    elif re.match(".*s$",s):
        if (s[-2] == 'y' and s[-3] in vowel_s): #working
            verb = s[:-1]
        elif re.match(".*[^sxyz]s$",s) and s[-4:-2] != "sh" and s[-4:-2] != "ch": #working
            verb = s[:-1]
        elif s == "has":        # working
            verb = "have"
    else:
        return s

    if not ((s,"VBZ") in brown.tagged_words() and (verb,"VB") in brown.tagged_words()):
        verb = ""
    return verb

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg

# End of PART A.
