#!/bin/bash
BASE=$HOME/openrov/data
for fdb in $BASE/s_*.cblite2/db.forest.?; do
    id=$(echo "$fdb" | sed 's/^.*s_//; s/.cblite2.*$//')
    # echo "$id:$fdb";
    if [ ! -e $BASE/$id.h264 ]; then
        echo "Got couchbase DB, but no matching .h264 video: $id"
        continue
    fi
    if [ ! -e $BASE/$id.mp4 ]; then
        echo "Parsing metadata for $id"
        ts=$(trident-metadata.py -l -s "$fdb")
        ts2=$(trident-metadata.py "$fdb")
        trident-metadata.py -a "$fdb" > $BASE/$id.telemetry
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
