#!/usr/bin/env python3
import re
import sys
import os 
import subprocess
import json
import time
import getopt

def usage():
    print("You're doing it wrong. Use the source, Luke.")
    sys.exit(1)

def main():

    strftime_format = "%Y%m%d-%H%M%SZ"
    localtime = False

    opts, args = getopt.getopt(sys.argv[1:], 'hstluf:')

    for o, a in opts:
        if o == '-f':
            # specify strftime format 
            strftime_format = a
        elif o == '-h':
            # display help, then exit
            usage()
        elif o == '-s':
            # output standard Trident date string
            strftime_format = "Trident-%b-%d-%H%M%S"
        elif o == '-t':
            # Output seconds since epoch
            strftime_format = "%s"
        elif o == '-l':
            # use localtime (default is UTC / gmtime)
            localtime = True
        elif o == '-u':
            # use UTC / gmtime (default is UTC / gmtime)
            localtime = False

    dbdump_cmd=['''forestdb_dump''', '''--hex-key''', '''--hex-body''']

    try:
        dbfile=args[0]
    except IndexError:
        usage()

    try:
        command = dbdump_cmd + [dbfile]
        dump = subprocess.check_output(command).decode('utf-8')
    except Exception:
        print("Error running command, bailing out:", command, file=sys.stderr)
        sys.exit(1)

    # find the first document body in the forestdb_dump output
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
    # split to individual bytes and decode bytes to binary string
    b = re.split('''\s+''', body)
    raw = ''.join([chr(int(x, 16)) for x in b])

    # find the json string in the binary data
    result = re.search('''(\{[\w\s\"\{\}\[\]:\.,\-_]+\})''', raw)
    if not result:
        print("Couldn't recognize json in body data")
        sys.exit(1)
    j = result.group(1)

    # parse json and fetch timestamp
    data = json.loads(j)
    sec = data['rx_ts']['sec']

    timetuple = None
    if localtime:
        timetuple = time.localtime(sec)
    else:
        timetuple = time.gmtime(sec)

    ts_str = time.strftime(strftime_format, timetuple)
    print(ts_str)
    # print(time.asctime(time.localtime(sec)))
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user, exiting...", file=sys.stderr)

