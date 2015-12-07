#!/usr/bin/env python3

import collections
import random
import sqlite3
import string
import tools
import json
import sys
import re

class mkchain:
    def __init__(self,db,src,maxlen,ngramlen):
        nick = 'src LIKE "'+src+'"'
        self._ngramlen = ngramlen
        self._chain = sqlite3.connect(':memory:')
        self._chain.execute('CREATE TABLE chain ('+', '.join([chr(x+ord('a'))+' VARCHAR' for x in range(ngramlen)])+', count INTEGER)')
        self._chain.execute('CREATE UNIQUE INDEX ngram ON chain('+(', '.join([chr(x+ord('a')) for x in range(ngramlen)]))+')')
        for i in db.get_iter(' AND '.join([nick])):
            words = [x.upper() for x in re.findall(r"[\w']+", i.msg) if len(x) <= maxlen]
            for n in range(1,len(words)-self._ngramlen+1):
                cur = self._chain.execute('UPDATE chain SET count = count+1 WHERE '+' AND '.join([chr(x+ord('a'))+'=?' for x in range(ngramlen)]),tuple([words[x] for x in range(n,n+ngramlen)]))
                if cur.rowcount < 1:
                    self._chain.execute('INSERT INTO chain VALUES('+','.join(['?' for x in range(ngramlen)])+',1)',tuple([words[x] for x in range(n,n+self._ngramlen)]))
        self._chain.commit()
                    
    def guess(self,seed):
        cur = self._chain.execute('SELECT total(count) FROM chain WHERE '+' AND '.join([chr(x+ord('a'))+'=?' for x in range(self._ngramlen-1)]),seed)
        total = next(cur,(0,))
        rnd = random.randint(0,total[0])
        count = 0;
        for row in self._chain.execute('SELECT '+chr(ord('a')+self._ngramlen-1)+',count FROM chain WHERE '+' AND '.join([chr(x+ord('a'))+'=?' for x in range(self._ngramlen-1)]),seed):
            count += row[1]
            if count >= rnd:
                return row[0]
    

if len(sys.argv) < 4:
    print('./wordprofile.py database maxlen src [msg]')
    sys.exit(1)

db = tools.database(sys.argv[1])
maxlen = int(sys.argv[2])

chain = mkchain(db,'BenLand100%',15,4)     
            
seed = ('GOING','TO','GET')
for j in range(10):
    msg = seed
    cur = seed
    for i in range(10):
        cur = cur[1:]+(chain.guess(cur),)
        msg = msg + (cur[-1],)
    print(msg)

