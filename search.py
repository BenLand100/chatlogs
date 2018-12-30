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

import tools
import json
import argparse
import sys

parts = ['src','msg','timestamp','dest']

parser = argparse.ArgumentParser()
parser.add_argument('--db',default='chats.db')
for part in parts:
    parser.add_argument('--'+part)

cmdargs = parser.parse_args()

db = tools.database(cmdargs.db)

cmdargs = vars(cmdargs)
query = []
args = []
for part in parts:
    if cmdargs[part] is None:
        continue
    query.append(part+' LIKE ?')
    args.append(cmdargs[part])
query = ' AND '.join(query)
args = tuple(args)

print(query,args)

if len(query) == 0:
    [print(i.when,i.utc(),i.src,i.dest,i.msg) for i in db.get_iter()]
else:
    [print(i.when,i.utc(),i.src,i.dest,i.msg) for i in db.get_iter(query,args)]

