#!/usr/bin/env python3

import tools
import statistics

def stats(db):
    nicks = ['BenLand100','Treebeard','TheDoctor','Colquhoun']
    lines = [db.count('src="'+nick+'" AND (dest="#srl" OR dest="#srl-thinktank")') for nick in nicks]
    grandtotal = db.count('NOT src="*" AND (dest="#srl" OR dest="#srl-thinktank")')

    print('All lines',grandtotal)
    print('Nicks',nicks)
    print('Line Counts',lines)
    print('Line Fractions',[line/grandtotal for line in lines])

    msglens = [[len(msg.msg) for msg in db.get_iter('src="'+nick+'" AND (dest="#srl" OR dest="#srl-thinktank")')] for nick in nicks]

    means = [statistics.mean(msglen) for msglen in msglens]
    stdev = [statistics.stdev(msglen) for msglen in msglens]

    print('Mean chars',means)
    print('Stdev chars',stdev)
    

db = tools.database(sys.argv[1])
stats(db)
