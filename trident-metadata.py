#!/usr/bin/env python3
import re
import sys
import os 
import subprocess
import json
import time

def usage():
    print("You're doing it wrong. Use the source, Luke.")
    sys.exit(1)

def main():

    dbdump_cmd=['''forestdb_dump''', '''--hex-key''', '''--hex-body''']

    try:
        dbfile=sys.argv[1]
    except IndexError:
        usage()

    dump = subprocess.check_output(dbdump_cmd + [dbfile]).decode('utf-8')
    result = re.search('''\nDoc ID:.*?\n\s+Body:\s\(hex\)\s*\n(.*?)\n\n''', dump, flags=re.DOTALL|re.MULTILINE)
    body = None
    if not result:
        print("Error: Couldn't recognize output from forestdb_dump")
        sys.exit(1)
    body = result.group(1)

    # strip leading space on each line
    body = re.sub('''^\s+''', '', body, flags=re.MULTILINE)
    # strip trailing space and interpreted bytes on each line
    body = re.sub('''\s{3}.*$''', '', body, flags=re.MULTILINE)
    # split to individual bytes
    b = re.split('''\s+''', body)
    raw = ''.join([chr(int(x, 16)) for x in b])
    result = re.search('''(\{[\w\s\"\{\}\[\]:\.,\-_]+\})''', raw)
    if not result:
        print("Couldn't recognize json in body data")
        sys.exit(1)
    j = result.group(1)
    data = json.loads(j)
    sec = data['rx_ts']['sec']
    ts_str = time.strftime("%Y-%m-%dT%H%M%SUTC", time.gmtime(sec))
    print(ts_str)
    # print(time.asctime(time.localtime(sec)))
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user, exiting...", file=sys.stderr)

