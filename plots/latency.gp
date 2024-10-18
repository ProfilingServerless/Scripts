reset

# Usage: `gnuplot -e 'FIRST_TIMESTAMP=1720524608076890' -e 'DATA_FILE_PATH="plots/latency.txt"' -e 'OUTPUT_PATH="latency.eps"' plots/latency.gp` 
# OUTPUT_PATH is optional(default=latency.eps)

# Sample data(timestamp, duration):
#
# 1720524608076890	112048
# 1720524608126980	110927
# 1720524608177950	127066

# Variables
if (!exists("FIRST_TIMESTAMP")) {
    print "Error: The variable 'FIRST_TIMESTAMP' is not set. Please provide a value."
    exit
}
if (!exists("DATA_FILE_PATH")) {
    print "Error: The variable 'DATA_FILE_PATH' is not set. Please provide a value."
    exit
}
if (!exists("OUTPUT_PATH")) OUTPUT_PATH = "latency.eps"

# set term post "Times" eps color solid enh
set term post eps color solid enh
set output sprintf("%s", OUTPUT_PATH)

#set size ratio 0.6
set size 1,0.72
#set multiplot layout 1,2

# Figure for openwhisk
set origin 0,0

# Margins
set lmargin 13
set rmargin 8
set bmargin 6
set tmargin 1.5

# Ranges
set xrange [0: 240]
set yrange [0: 4]

# Ticks
set xtics 60 nomirror out font ",24" offset character 0, -0.5, 0
set mxtics 3
set ytics font ",24"

# Labels
set xlabel "Time (s)"  font ",24" offset character 0, -1.5, 0
set ylabel "Latency (s)" font ",24" offset character -2, -1, 0

# What are these?
set key right top width 0.25 height 0.25 font ',20' box opaque # horizontal
set border black
set datafile missing "?"


# Line Styles
set style line 1 lt 1 lc rgb '#d39234' lw 2 pt 3 ps 1.5
set style line 2 lt 1 lc rgb '#3172ae' lw 4 pt 7 ps 1.5
set style line 3 lt 1 lc rgb '#949494' lw 4 pt 11 ps 1.5
set style line 4 lt 1 lc rgb '#344035' lw 2 pt 8 ps 2
set style line 5 lt 1 lc rgb '#DF6F58' lw 4 pt 7 ps 2
set style line 6 lt 1 lc rgb '#A99A97' lw 4 pt 2 ps 2

# Grid
set grid

# Plot
plot DATA_FILE_PATH using ($1 - FIRST_TIMESTAMP) / 1e6:(int(100 * rand(0)) < 80 ? $2/1000000 : 1/0) with lines linestyle 1 title "actualDuration"
