# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'),
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    NN_list = []
    NNS_list = []
    unchanging_set = set()
    with open("sentences.txt", "r") as f:
        for line in f:
            for words in line.split():
                (word,tag) = words.split('|')
                if tag == "NN":
                    NN_list.append(word)
                elif tag == "NNS":
                    NNS_list.append(word)

    for nn_word in NN_list:
        if nn_word in NNS_list:
            unchanging_set.add(nn_word)
    return unchanging_set

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""
    vowel_s = "aeiou"
    noun = ""
    if s in unchanging_plurals_list:
        noun = s
    elif re.match(".*men$",s):
        noun = s[:-3] + "man"
    else:
        if re.match(".*ies$",s):
            if len(s) == 4 and not s[0] in vowel_s:
                noun = s[:-1]
            else:
                noun = s[:-3] + 'y'
        elif re.match(".*es$",s):
            if re.match(".*(o|x|sh|ch|ss|zz)es$",s):
                noun = s[:-2]
            elif re.match(".*[^(sxyz)]es$",s) and s[-4:-2] != "sh" and s[-4:-2] != "ch":
                noun = s[:-1]
            elif re.match(".*(([^s]s)|([^z]z))es$",s):
                noun = s[:-1]
        elif re.match(".*s$",s):
            if s[-2] == 'y' and s[-3] in vowel_s:
                noun = s[:-1]
            elif re.match(".*[^sxyz]s$",s) and s[-4:-2] != "sh" and s[-4:-2] != "ch":
                noun = s[:-1]
            elif s == "has":
                noun = "have"
        else:
            return ""

    return noun

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    tag_list = []
    for (word,tag) in function_words_tags:
        if word == wd:
            tag_list.append(tag)

    for word in lx.getAll('P'):
        if word == wd:
            tag_list.append('P')

    for word in lx.getAll('A'):
        if word == wd:
            tag_list.append('A')

    for word in lx.getAll('N'):
        if noun_stem(wd) == word:
            tag_list.append('Np')
        if wd == word:
            tag_list.append('Ns')

    for word in lx.getAll('I'):
        if verb_stem(wd) == word:
            tag_list.append('Is')
        if wd == word:
            tag_list.append('Ip')

    for word in lx.getAll('T'):
        if verb_stem(wd) == word:
            tag_list.append('Ts')
        if wd == word:
            tag_list.append('Tp')

    return tag_list


def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
