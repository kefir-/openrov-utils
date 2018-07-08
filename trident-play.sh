#!/bin/bash
VLC="$(which vlc)"
FFPLAY="$(which ffplay)"

if [ -z $VLC ] && [ -z $FFPLAY ]; then
    echo "Can't find vlc or ffplay, giving up"
    exit 1
fi
if [ -e "$VLC" ]; then
    echo "DEBUG: Launching VLC"
    exec vlc -f --demux h264 --h264-fps 30 "$@"
elif [ -e "$FFPLAY" ]; then
    echo "DEBUG: Launching FFPLAY"
    exec ffplay -fs -f h264 -vf 'setpts=N/(30*TB)' "$@"
fi
