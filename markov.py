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
import hashlib
import sqlite3
import random
import string
import tools
import nltk
import json
import sys
import re

class mkchain:
    def __init__(self,db,src,maxlen,ngramlen,chain=sqlite3.connect(':memory:')):
        if type(chain) is str:
            self._chain = sqlite3.connect(chain)
        else:
            self._chain = chain
        self._ngramlen = ngramlen
        self._table = 'chain_'+str(ngramlen)+'_'+hashlib.md5(src.encode('utf8')).hexdigest()+'_'+str(maxlen)
        if not next(self._chain.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?',(self._table,)),None):
            print('Please wait... generating ngram table')
            self._chain.execute('CREATE TABLE '+self._table+' ('+', '.join([chr(x+ord('a'))+' VARCHAR' for x in range(ngramlen)])+', count INTEGER)')
            self._chain.execute('CREATE UNIQUE INDEX ngram_'+self._table+' ON '+self._table+'('+(', '.join([chr(x+ord('a')) for x in range(ngramlen)]))+')')
            nick = 'src LIKE "'+src+'"' if src != 'ALL' else 'src != "*"'
            for i in db.get_iter(' AND '.join([nick])):
                thin = ' '.join([x.lower() for x in i.msg.split(' ') if len(x) <= maxlen])
                tokens = nltk.word_tokenize(thin)
                words = [x for x in tokens if len(x) <= maxlen]
                for n in range(1,len(words)-self._ngramlen+1):
                    cur = self._chain.execute('UPDATE '+self._table+' SET count = count+1 WHERE '+' AND '.join([chr(x+ord('a'))+'=?' for x in range(ngramlen)]),tuple([words[x] for x in range(n,n+ngramlen)]))
                    if cur.rowcount < 1:
                        self._chain.execute('INSERT INTO '+self._table+' VALUES('+','.join(['?' for x in range(ngramlen)])+',1)',tuple([words[x] for x in range(n,n+self._ngramlen)]))
            self._chain.commit()
                    
    def guess(self,seed):
        cur = self._chain.execute('SELECT total(count) FROM '+self._table+' WHERE '+' AND '.join([chr(x+ord('a'))+'=?' for x in range(self._ngramlen-1)]),seed)
        total = next(cur,(0,))
        rnd = random.randint(0,total[0])
        count = 0;
        for row in self._chain.execute('SELECT '+chr(ord('a')+self._ngramlen-1)+',count FROM '+self._table+' WHERE '+' AND '.join([chr(x+ord('a'))+'=?' for x in range(self._ngramlen-1)]),seed):
            count += row[1]
            if count >= rnd:
                return row[0]
                
    def expound(self,text,tries=1000):
        seed = list(nltk.word_tokenize((' '.join(sys.argv[5:])).lower()))
        random.shuffle(seed)
        for i in range(tries):
            random.shuffle(seed)
            msg = tuple(seed[0:ngramlen-1])
            cur = msg
            for i in range(10):
                cur = cur[1:]+(self.guess(cur),)
                if not cur[-1]:
                    break
                msg = msg + (cur[-1],)
            if len(msg) > 5 and len(msg) < 50:
                return msg
        return ()

random.seed()

if len(sys.argv) < 4:
    print('./wordprofile.py database ngramlen maxlen src')
    sys.exit(1)

db = tools.database(sys.argv[1])
ngramlen = int(sys.argv[2])
maxlen = int(sys.argv[3])

chain = mkchain(db,sys.argv[4],maxlen,ngramlen,'chain.db')     

print(' '.join(chain.expound(' '.join(sys.argv[5:]))))
            


