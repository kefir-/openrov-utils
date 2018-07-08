#!/bin/bash
BASE=$HOME/openrov/data
for fdb in $BASE/s_*.cblite2/db.forest.?; do
    id=$(echo "$fdb" | sed 's/^.*s_//; s/.cblite2.*$//')
    echo "$id:$fdb";
    if [ ! -e $BASE/$id.mp4 ]; then
        ts=$(trident-metadata.py -l -s "$fdb")
        ffmpeg -r 30 -i $BASE/$id.h264 -c copy -r 30 $BASE/$ts.mp4
        if [ $? -eq 0 ]; then
            ln -sv $BASE/$ts.mp4 $BASE/$id.mp4
        fi
    fi
done
