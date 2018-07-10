#!/bin/bash
#
# (C) Ketil Froyn <ketil@froyn.name> 2018
#
# Script to plot telemetry data from OpenROV Trident using gnuplot
#
telemetry=$1
if [ -z $telemetry ]; then
    echo "You must specify a telemetry file as the first argument"
    exit 1
fi

dir=$(dirname "$telemetry")
file=$(basename "$telemetry" .telemetry)

out="$dir/$file"

grep depth: $telemetry | cut -d " " -f 1,3 > $out.depth
grep temp.water.temperature.temperature_ $telemetry | cut -d " " -f 1,3 > $out.water-temp

echo "DEBUG: Running gnuplot with output"

echo "Exiting, this doesn't work yet"
exit 1

# gnuplot doesn't accept this on stdin. Use arguments or declare variables
# to pass the filename instead

cat | gnuplot5 - <<EOF
set terminal png size 800,600 enhanced font "Helvetica,20"
set output "${out}-depth-temp.png"

set multiplot
set xdata time
set format x '%H:%M:%S'
set xtics rotate
set lmargin screen 0.3
set grid

# first plot
set ytics 1
set yrange[9:28]
set ylabel "Water temperature (C)" textcolor rgb "red"
plot '$out.water-temp' using (\$1):2 with lines linecolor rgb "red" notitle

# second plot
set ytics 1
set yrange[-1:18]
set ytics offset -8, 0
set ylabel "Depth (m)" offset -8, 0 textcolor rgb "green"
plot '$out.depth' using (\$1):2 with lines linecolor rgb "green" notitle
EOF

echo "Done"
