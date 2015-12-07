#!/usr/bin/env python3

import collections
import random
import sqlite3
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
        self._table = 'chain_'+str(ngramlen)+'_'+src+'_'+str(maxlen)
        if not next(self._chain.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="'+self._table+'"'),None):
            self._chain.execute('CREATE TABLE '+self._table+' ('+', '.join([chr(x+ord('a'))+' VARCHAR' for x in range(ngramlen)])+', count INTEGER)')
            self._chain.execute('CREATE UNIQUE INDEX ngram_'+self._table+' ON '+self._table+'('+(', '.join([chr(x+ord('a')) for x in range(ngramlen)]))+')')
            nick = 'src LIKE "'+src+'"'
            for i in db.get_iter(' AND '.join([nick])):
                tokens = nltk.word_tokenize(i.msg.lower())
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
        for i in range(tries):
            random.shuffle(seed)
            msg = tuple(seed[0:ngramlen-1])
            cur = msg
            for i in range(10):
                cur = cur[1:]+(chain.guess(cur),)
                if not cur[-1]:
                    break
                msg = msg + (cur[-1],)
            if len(msg) > 5 and len(msg) < 50:
                return msg
    

if len(sys.argv) < 4:
    print('./wordprofile.py database ngramlen maxlen src')
    sys.exit(1)

db = tools.database(sys.argv[1])
ngramlen = int(sys.argv[2])
maxlen = int(sys.argv[3])

chain = mkchain(db,sys.argv[4],maxlen,ngramlen,'chain.db')     

print(chain.expound(' '.join(sys.argv[5:])))
            


