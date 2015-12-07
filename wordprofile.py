#!/usr/bin/env python3

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
nick = 'src LIKE "'+sys.argv[4]+'"'
msg = ('msg LIKE "'+sys.argv[5]+'"') if len(sys.argv) > 5 else '1=1'

words = collections.Counter() 
for i in db.get_iter(' AND '.join([nick,msg])):
    words.update([x.upper() for x in re.findall(r"[\w']+", i.msg) if len(x) <= maxlen])
 
print(0,',',sum(words.values()))   
print(1,',',len(set(words)))
[print('"'+word[0]+'",',word[1]) for word in words.most_common(int(sys.argv[2]))]
