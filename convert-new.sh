#!/bin/bash
#
# (C) Ketil Froyn <ketil@froyn.name> 2018
#
# Script that automates several steps of my standard workflow
# when working with the OpenROV Trident
#
BASE=$HOME/openrov/data
for fdb in $BASE/s_*.cblite2/db.forest.?; do
    id=$(echo "$fdb" | sed 's/^.*s_//; s/.cblite2.*$//')
    if [ ! -e $BASE/$id.telemetry ]; then
        echo "Parsing metadata for $id"
        trident-metadata.py -a "$fdb" > $BASE/$id.telemetry
    fi
    if [ ! -e $BASE/$id.h264 ]; then
        echo "Got couchbase DB, but no matching .h264 video: $id"
        continue
    fi
    if [ ! -e $BASE/$id.mp4 ]; then
        epoch_ts=$(trident-metadata.py -l -e "$fdb")
        # LANG=en_US forces the language, otherwise locale settings may give different month names
        ts=$(LANG=en_US date +Trident-%b-%d-%H%M%S -d @$epoch_ts)
        ts2=$(date -u +%Y%m%d-%H%M%SZ -d @$epoch_ts)
        echo $epoch_ts > $BASE/$id.timestamp
        echo $ts >> $BASE/$id.timestamp
        echo $ts2 >> $BASE/$id.timestamp
        # create the mp4 file if it hasn't already been done. Standardize on the
        # format used internally by the OpenROV Cockpit app, for compatibility.
        if [ ! -e $BASE/$ts.mp4 ]; then
            echo "Converting $id.h264 to $ts.mp4 (alias $ts2.mp4)"
            ffmpeg -v fatal -r 30 -i $BASE/$id.h264 -c copy -r 30 $BASE/$ts.mp4
        fi
        ln -s $BASE/$ts.mp4 $BASE/$id.mp4
        ln -s $BASE/$ts.mp4 $BASE/$ts2.mp4
    fi
done

# To clean up and reprocess everything:
# find $HOME/openrov/data -type l | xargs rm -v
