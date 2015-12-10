#!/usr/bin/env python3

import sys
import tools

if len(sys.argv) != 3:
    print('./parse_hangout.py dbfile [he]xchatlogfile')
    sys.exit(1)

db = tools.database(sys.argv[1])
tools.process_irc(db,sys.argv[2])

