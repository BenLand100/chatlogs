#!/usr/bin/env python3

import sys
from math import *
import tools
import statistics

def stats(db,like='%'):
    lines = db.count('src LIKE "'+like+'"') 

    msglens = [len(msg.msg) for msg in db.get_iter('src LIKE "'+like+'"')]

    mean = statistics.mean(msglens) 
    stde = statistics.stdev(msglens)
    rootnorm = lambda lst: sqrt(sum(lst))/sqrt(len(lst))
    rmshi = rootnorm([(msglen - mean)**2.0 for msglen in msglens if msglen > mean])
    rmslo = rootnorm([(msglen - mean)**2.0 for msglen in msglens if msglen < mean])

    print('Pattern',like)
    print('Line Counts',lines)
    print('Mean chars',mean)
    print('Stdev chars',stde)
    print('RMS hi/lo',rmshi,'/',rmslo)
    

db = tools.database(sys.argv[1])
stats(db,sys.argv[2] if len(sys.argv) == 3 else None)
