This repo contains a collection of scripts and utilities that I use in
my workflow for downloading and processing video recordings made with
my OpenROV Trident. There's no app and no pretty GUI, but it works
well and moves most processing from the cell phone/tablet to a computer.

## trident-fetch.sh

The first tool you may want to look at is `trident-fetch.sh`. This
script fetches any files from the OpenROV Cockpit app's folder that
haven't already been transferred. 

It expects you to run sweech on your phone, and that the sweech CLI has
been installed from github or using `pip install sweech-cli`. Have a
look at the script source code to see if you want to update any paths.

## convert-new.sh

The second tool you may want to look at is `convert-new.sh`. This 
script converts the raw .h264 files to .mp4 files. It also parses the db
in the .cbase2 folders in an attempt to fetch a timestamp, and uses this
timestamp to rename the files just like the OpenROV Cockpit app. It 
creates some additional file names, using symlinks, so that it's easier
(for me) to navigate many recordings. (The built in naming scheme is
also unpractical after you've done more than a year of recordings).

## trident-play.sh

If you want to simply view a .h264 file, try the script
`trident-play.sh`, specifying the .h264 file as the first argument. This
script searches your PATH for vlc or ffplay, and plays the .h264 video
directly, at the correct frame rate, without doing any heavy
transcoding.

## trident-metadata.py

The `trident-metadata.py` script uses the `forestdb_dump` command
from https://github.com/couchbase/forestdb.git to dump the contents
of the couchbase database, and parses the hex output from there to
recreate some json, with the final aim of fetching a timestamp. This
is a hopeless cludge, but I've not had much help from either 
Couchbase (not to be confused with Apache CouchDB, which is something
else) or OpenROV in finding a better solution for this. Hopefully
OpenROV will ditch Couchbase for something sensible in the future.

I aim to try to parse all the telemetry data from the database using
the same technique. There's lots of info in the DB, like
* yaw
* roll
* pitch
* depth
* pressure
* temperature
* battery percentage
* battery voltage
* battery temperature
etc, and many appear to be logged close to once per second.
