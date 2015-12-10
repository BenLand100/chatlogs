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

import os
import glob
import pytz
import sqlite3
import datetime
import tarfile
import json
import statistics

class message:
    def __init__(self,when,src,dest,msg):
        self.src, self.dest, self.msg = src, dest, msg
        if type(when) is int:
            self.when = datetime.datetime.fromtimestamp(when,tz=datetime.timezone.utc)
        elif isinstance(when,datetime.datetime):
            self.when = when
        else:
            raise TypeError
    def __str__(self):
        return str(self.when)+' '+self.src+' '+self.dest+' '+self.msg
    def utc(self):
        return int(self.when.replace(tzinfo=datetime.timezone.utc).timestamp())
    def uid(self):
        return str(self.utc())+':'+str(self.src)+':'+str(self.dest)+':'+str(hash(self.msg))

class database:
    def __init__(self,db=':memory:'):
        self._db = sqlite3.connect(db)
        if self._table_exists('messages'):
            print('Creating database tables')
            self._db.execute('CREATE TABLE messages(timestamp INTEGER, src VARCHAR, dest VARCHAR, msg VARCHAR, PRIMARY KEY (timestamp,src,dest,msg) )')
    def __del__(self):
        self._db.close()
    def _table_exists(self,table):
        return not next(self._db.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?',(table,)),None)
    def commit(self):
        self._db.commit()
    def add(self,msg):
        try:
            self._db.execute('INSERT INTO messages VALUES(?,?,?,?)',(msg.utc(),msg.src,msg.dest,msg.msg))
            return True
        except:
            return False
    def count(self,where=None,args=()):
        row = next(self._db.execute('SELECT count(timestamp) FROM messages' + (' WHERE ' + where if where else ''),args),None)
        return row[0] if row else 0
    def get_iter(self,where=None,args=()):
        for row in self._db.execute('SELECT timestamp,src,dest,msg FROM messages' + (' WHERE ' + where if where else ''),args):
            yield message(row[0],row[1],row[2],row[3])
        
        

months = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
lines = 0
failed = 0

def parse_irc(db,path):
    global lines, failed
    base = os.path.basename(path).rsplit('.',1)[0]
    chan = base[base.find('#'):]
    tz = pytz.timezone('US/Eastern')
    with open(path,'r') as f:
        for line in f:
            lines = lines + 1
            try:
                line = line.strip(' \t\n\r\x00')
                if len(line) < 2:
                    continue
                elif line[0] == '*':
                    if 'BEGIN LOGGING' in line:
                        year = int(line.split(' ')[-1].strip('\t\n\r'))
                else:
                    parts = line.replace('\t',' ').split(' ',4)
                    if parts[0] == 'T':
                        dt = int(parts[1])
                    else:
                        tparts = list(map(int,parts[2].split(':')))
                        dt = datetime.datetime(year,months[parts[0]],int(parts[1]),tparts[0],tparts[1],tparts[2],0,tz)
                    msg = message(dt,parts[3].strip('<>'),chan,parts[4].strip('\t\r\n') if len(parts) == 5 else '')
                    db.add(msg)
            except Exception as e:
                failed = failed + 1
               

def process_hangouts(db,path):
    global lines, failed
    tar = tarfile.open(path,'r:*')
    f = tar.extractfile('Takeout/Hangouts/Hangouts.json')
    data = json.loads(f.read().decode())
    f.close()
    tar.close()
    for conversation in data["conversation_state"]:
        initial_timestamp = conversation["response_header"]["current_server_time"]
        conversation_id = conversation["conversation_id"]["id"]
        
        people = {}
        
        for participant in conversation["conversation_state"]["conversation"]["participant_data"]:
            gaia_id = participant["id"]["gaia_id"]
            chat_id = participant["id"]["chat_id"]
            try:
                name = participant["fallback_name"]
            except:
                name = 'UNKNOWN'
            people[gaia_id] = name

        for event in conversation["conversation_state"]["event"]:
            event_id = event["event_id"]
            sender_id = event["sender_id"] # has dict values "gaia_id" and "chat_id"
            timestamp = event["timestamp"]
            text = list()
            try:
                message_content = event["chat_message"]["message_content"]
                try:
                    for segment in message_content["segment"]:
                        if segment["type"].lower() in ("TEXT".lower(), "LINK".lower()):
                            text.append(segment["text"].strip())
                except KeyError:
                    pass 
            except KeyError:
                continue 
            msg = message(int(int(timestamp)/10**6),people[sender_id["gaia_id"]],'ME',' '.join(text))
            db.add(msg)
    db.commit()
