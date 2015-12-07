#!/usr/bin/env python3

import tools
import json
import sys

if len(sys.argv) < 3:
    print('./crunch.py database src [msg]')
    sys.exit(1)

db = tools.database(sys.argv[1])

nick = 'src LIKE "'+sys.argv[2]+'"'
msg = ('msg LIKE "'+sys.argv[3]+'"') if len(sys.argv) > 3 else '1=1'
data = [print(i.utc(),',',len(i.msg)) for i in db.get_iter(' AND '.join([nick,msg]))]

