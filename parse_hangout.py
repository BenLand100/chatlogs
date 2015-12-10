#!/usr/bin/env python3

import sys
import tools

if len(sys.argv) != 3:
    print('./parse_hangout.py dbfile hangoutfile')
    sys.exit(1)

db = tools.database(sys.argv[1])
tools.process_hangouts(db,sys.argv[2])

