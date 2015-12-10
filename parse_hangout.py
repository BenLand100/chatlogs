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
import tools

if len(sys.argv) != 3:
    print('./parse_hangout.py dbfile hangoutfile')
    sys.exit(1)

db = tools.database(sys.argv[1])
tools.process_hangouts(db,sys.argv[2])

