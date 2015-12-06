#!/usr/bin/env python3

import tools
import json
import sys

if len(sys.argv) != 3:
    print('./crunch.py database nicklike')
    sys.exit(1)

db = tools.database(sys.argv[1])

nick = sys.argv[2]
lines = db.count('src LIKE "'+nick+'"')
data = [print(msg.utc(),',',len(msg.msg)) for msg in db.get_iter('src LIKE "'+nick+'"')]

