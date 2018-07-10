#!/bin/bash
#
# (C) Ketil Froyn <ketil@froyn.name> 2018
#
# Sample wrapper to fetch OpenROV Trident files from the
# device they were recorded on. Depends on the device running
# the Sweech app.
#

SWEECH_URL=""
TARGET_PATH="$HOME/openrov/"

if [ ! -e "$TARGET_PATH" ]; then
    mkdir -p "$TARGET_PATH"
fi

if [ ! -z "$1" ]; then
    SWEECH_URL="$1";
fi

# Find where the URL has been set
if [ -z $SWEECH_URL ] && [ ! -e $HOME/.config/sweech.json ]; then
    echo "No SWEECH_URL given, and $HOME/.config/sweech.json doesn't exist."
    echo "Please specify the URL somehow."
    exit 1
fi
echo "DEBUG: SWEECH_URL=$SWEECH_URL (config file used if blank)"

# Find the sweech.py or sweech command
SWEECH_CMD="$HOME/git/sweech-cli/sweech.py"
if [ ! -e "$SWEECH_CMD" ]; then
    SWEECH_CMD="$(which sweech)"
    if [ ! -e "$SWEECH_CMD" ]; then
        echo "Can't find sweech.py, please fetch it from github or install it with 'pip install sweech-cli'"
        exit 1
    fi
fi
echo "DEBUG: Got sweech command: $SWEECH_CMD"

# A bit of a hack to extract the base path of the internal storage on the device
MOBILE_BASE="$("$SWEECH_CMD" info | grep -A3 "^Internal storage" | grep ^[[:space:]]*Path: | awk '{print $2}')"
echo "DEBUG: MOBILE_BASE=$MOBILE_BASE"
echo "DEBUG: TARGET_PATH=$TARGET_PATH"

SOURCE="$MOBILE_BASE/Android/data/com.openrov.cockpit/files/data"
echo "DEBUG: SOURCE=$SOURCE"

exec "$SWEECH_CMD" pull --keep "$SOURCE" "$TARGET_PATH"
