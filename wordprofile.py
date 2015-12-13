#!/usr/bin/env python3
'''
 *  Copyright 2015 by Benjamin J. Land (a.k.a. BenLand100)
 *
 *  This file is part of chatlogs.
 *
 *  chatlogs is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  chatlogs is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with chatlogs. If not, see <http://www.gnu.org/licenses/>.
'''

import collections
import nltk
import string
import tools
import json
import sys
import re
import multiprocessing
import enchant

if len(sys.argv) < 5:
    print('./wordprofile.py database num splittype maxlen src+')
    print('\tsplittype can be one of: nltk, regex, respell')
    sys.exit(1)

db = tools.database(sys.argv[1])
maxlen = int(sys.argv[4])
query = ' OR '.join(['src LIKE ?' for i in range(len(sys.argv)-5)])
args = tuple(sys.argv[5:])

words = collections.Counter() 
if sys.argv[3] == 'nltk':
    for i in db.get_iter(query,args):
        thin = ' '.join([x.lower() for x in i.msg.split(' ') if len(x) <= maxlen])
        words.update(nltk.word_tokenize(thin))
elif sys.argv[3] == 'regex':
    wordtokregex = re.compile('([\w'']+|[\:\=][^ ])')
    for i in db.get_iter(query,args):
        thin = ' '.join([x.lower() for x in i.msg.split(' ') if len(x) <= maxlen])
        words.update([word for word in wordtokregex.findall(thin)])
elif sys.argv[3][0:7] == 'respell':
    try:
        maxdist = int(sys.argv[3].split(':')[1])
    except:
        maxdist = 0
    wordtokregex = re.compile('([\w\']+|[\:\=][^ ])')
    sgst = tools.suggester(maxdist)
    for i in db.get_iter(query,args):
        parts = ' '.join([x.upper() for x in i.msg.split(' ') if len(x) <= maxlen])
        parts = [word for word in wordtokregex.findall(parts)]
        parts = [sgst.suggest(word) for word in parts]
        words.update([word for word in parts if word])
 
print('"---total---"',',',sum(words.values()))   
print('"---unique---"',',',len(set(words)))
[print('"'+word[0]+'",',word[1]) for word in words.most_common(int(sys.argv[2]))]
