import nltk
import re
from nltk.corpus import brown

s = raw_input("Enter a word:")
verb = ""
vowel_s = "aieou"

if re.match(".*ies$",s):
	if len(s) == 4 and not s[0] in vowel_s:
		verb = s[:-1]
	else:
		verb = s[:-3] + 'y'
elif re.match(".*es$",s):
	if re.match(".*(o|x|ch|ss|zz)es$",s):
		verb = s[:-2]
	elif re.match(".*[^(sxioz)]es$",s) and s[-4:-2] != "sh" and s[-4:-2] != "ch":
		verb = s[:-1]
	elif re.match(".*(s|z)es$",s) and s[-4:-1] != "sse" and s[-4:-1] != "zze":
		verb = s[:-1]
elif re.match(".*s$",s):
	if (s[-2] == 'y' and s[-3] in vowel_s):
		verb = s[:-1]
	elif re.match(".*[^sxyz]s$",s) and s[-4:-2] != "sh" and s[-4:-2] != "ch" and not s[-2] in vowel_s:
		verb = s[:-1]
	elif s == "has":
		verb = "have"
else:
	verb = s
print verb

if not ((stem,"VB") in set(nltk.corpus.brown.tagged_words()) and (s,"VBZ") in set(nltk.corpus.brown.tagged_words())):
	verb = ""
return verb
