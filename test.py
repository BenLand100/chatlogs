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

import sys
from math import *
import tools
import statistics

def stats(db,like='%'):
    lines = db.count('src LIKE "'+like+'"')

    msglens = [len(msg.msg) for msg in db.get_iter('src LIKE "'+like+'"')]
    
    if len(msglens) > 1:
        mean = statistics.mean(msglens) 
        stde = statistics.stdev(msglens)
    else:
        mean,stde = 0,0
    rootnorm = lambda lst: sqrt(sum(lst))/sqrt(len(lst)) if len(lst) > 0 else 0
    rmshi = rootnorm([(msglen - mean)**2.0 for msglen in msglens if msglen > mean])
    rmslo = rootnorm([(msglen - mean)**2.0 for msglen in msglens if msglen < mean])

    print('Pattern',like)
    print('Line Counts',lines)
    print('Mean chars',mean)
    print('Stdev chars',stde)
    print('RMS hi/lo',rmshi,'/',rmslo)
    

db = tools.database(sys.argv[1])
stats(db,sys.argv[2] if len(sys.argv) == 3 else '%')
