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


def get_documents(dump):
    rest = dump
    while len(rest) > 100:
        # find the first document body in the forestdb_dump output
        result = re.search('''\nDoc ID:\s([^\n]+).*?\n\s+Body:\s\(hex\)\s*\n(.*?)\n\n''', rest, flags=re.DOTALL|re.MULTILINE)
        body = None
        if not result:
            return
        docid = result.group(1)
        raw_body = result.group(2)
        rest = rest[result.end():]

        if docid in ["privateUUID", "publicUUID"]:
            continue

        # strip leading space on each line
        body = re.sub('''^\s+''', '', raw_body, flags=re.MULTILINE)
        # strip trailing space and interpreted bytes on each line
        body = re.sub('''\s{3}.*$''', '', body, flags=re.MULTILINE)
        # split to individual bytes and decode bytes to binary string
        b = re.split('''\s+''', body)
        raw = ''.join([chr(int(x, 16)) for x in b])

        # find the json string in the binary data
        result = re.search('''(\{[\w\s\"\{\}\[\]:\.\?,\-_]{10,}\})''', raw)
        if not result:
            print("Couldn't recognize json in body data:", raw_body)
            sys.exit(1)
        j = result.group(1)

        # parse json and fetch timestamp
        try:
            data = json.loads(j)
        except json.decoder.JSONDecodeError:
            print("Got error while parsing json:", j)
            sys.exit(1)

        try:
            docid = docid.split(":")[1]
        except IndexError:
            pass

        yield((docid, data))

def print_time(data, localtime, strftime_format):
    sec = data['rx_ts']['sec']

    timetuple = None
    if localtime:
        timetuple = time.localtime(sec)
    else:
        timetuple = time.gmtime(sec)

    ts_str = time.strftime(strftime_format, timetuple)
    print(ts_str)

def main():

    strftime_format = "%Y%m%d-%H%M%SZ"
    localtime = False
    dump_all = False
    output_time = True

    opts, args = getopt.getopt(sys.argv[1:], 'ahstTeluf:')

    for o, a in opts:
        if o == '-f':
            # specify strftime format 
            strftime_format = a
        elif o == '-a':
            dump_all = True
            output_time = False
        elif o == '-h':
            # display help, then exit
            usage()
        elif o == '-s':
            # output standard Trident date string
            strftime_format = "Trident-%b-%d-%H%M%S"
        elif o == '-t':
            output_time = True
        elif o == '-T':
            output_time = False
        elif o == '-e':
            # Output seconds since epoch
            strftime_format = "%s"
        elif o == '-l':
            # use localtime (default is UTC / gmtime)
            localtime = True
        elif o == '-u':
            # use UTC / gmtime (default is UTC / gmtime)
            localtime = False

    dbdump_cmd=['''forestdb_dump''', '''--hex-body''']

    try:
        dbfile=args[0]
    except IndexError:
        usage()

    try:
        command = dbdump_cmd + [dbfile]
        dump = subprocess.check_output(command).decode('utf-8')
    except FileNotFoundError:
        print("forestdb_dump not available. Compile from https://github.com/couchbase/forestdb.git")
        print("and make sure the executable is in your PATH.")
        sys.exit(1)
    except Exception:
        print("Error running forestdb_dump, bailing out:", command, file=sys.stderr)
        sys.exit(1)

    data = None

    for i, d in get_documents(dump):
        # print("Got document:", i, d)
        # if i != d["topic"]:
        #     print("ID different from topic:", i, d["topic"])
        if output_time:
            print_time(d, localtime, strftime_format)
            output_time = False
        if not dump_all:
            break
        if d["topic"] == "FlightCameraH264Message":
            continue
        else:
            print("{2}.{3} {0}: {1}".format(d["topic"], d["data"], d["rx_ts"]["sec"], d["rx_ts"]["nanosec"]))

    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user, exiting...", file=sys.stderr)

