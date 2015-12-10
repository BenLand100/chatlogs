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
import string
import tools
import json
import sys
import re

if len(sys.argv) < 4:
    print('./wordprofile.py database num maxlen src [msg]')
    sys.exit(1)

db = tools.database(sys.argv[1])
maxlen = int(sys.argv[3])
if len(sys.argv) > 5:
    query = 'src LIKE ? AND msg LIKE ?'
    args = (sys.argv[4],sys.argv[5])
else:
    query ='src LIKE ?'
    args = (sys.argv[4],)

words = collections.Counter() 
for i in db.get_iter(query,args):
    words.update([x.upper() for x in re.findall(r"[\w']+", i.msg) if len(x) <= maxlen])
 
print('"---total---"',',',sum(words.values()))   
print('"---unique---"',',',len(set(words)))
[print('"'+word[0]+'",',word[1]) for word in words.most_common(int(sys.argv[2]))]
