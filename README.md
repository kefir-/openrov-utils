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
script converts the raw .h264 files to .mp4 files. It also uses the `trident-metadata.py` tool to parse the db
in the .cbase2 folders in an attempt to fetch a timestamp, and uses this
timestamp to rename the files just like the OpenROV Cockpit app. It 
creates some additional file names, using symlinks, so that it's easier
(for me) to navigate many recordings. (The built in naming scheme is
also unpractical after you've done more than a year of recordings).

It also creates uses the `trident-metadata.py` tool to create a flat text file with telemetry data.

## trident-play.sh

Utility that may come in handy.
If you want to simply view a .h264 file, try the script
`trident-play.sh`, specifying the .h264 file as the first argument. This
script searches your PATH for vlc or ffplay, and plays the .h264 video
directly, at the correct frame rate, without doing any heavy
transcoding.

## trident-metadata.py

Utility used by the other tools.
The `trident-metadata.py` script uses the `forestdb_dump` command
from https://github.com/couchbase/forestdb.git to dump the contents
of the couchbase database, and parses the hex output from there to
recreate some json objects.

The simple first aim of this script is to fetch the timestamp of the
recording, and this is the default action. Use the options -l and -s 
to get the same format as the OpenROV app.

I've added some rudimentary support for dumping the entire telemetry
content to a simple flat file, which will hopefully be a lot easier to
use. Also, keep in mind that this is a proof of concept, it's not 
necessarily a perfect product. Now it's at least possible to access 
all the data that's there.

The way this tool works is in fact a 
hopeless cludge, but I've not had much help from either 
[Couchbase](https://forums.couchbase.com/t/export-or-query-data-from-cblite2-database/17066)
(not to be confused with Apache CouchDB, which is something
else) or OpenROV in finding a better solution for this. Hopefully
OpenROV will ditch Couchbase for something sensible in the future.

Telemetry data includes lots of stuff, like:

* yaw
* roll
* pitch
* depth
* pressure
* water temperature
* battery percentage
* battery voltage
* battery temperature

etc, and many appear to be logged every second or every few seconds.

You can see all of the unique telemetry tags that were logged in a particular session with a command like this:

    ./trident-metadata.py -a <pathTo>/db.forest.0|awk '{print $2}'|sort -u

## Usage on macOS ##

Script ``trident-metadata.py`` has been tested on macOS High Sierra and works fine. You'll have to install
forestdb_dump and snappy from source, or use your favorite package manager like Homebrew.

To pull the data off of your Android controller using a USB cable, you can use Google's [Android File Transfer 
utility (https://www.android.com/filetransfer/)](https://www.android.com/filetransfer/). You'll have to browse
manually and manage the file retrieval yourself.
