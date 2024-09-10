reset
set term post eps color solid enh
set termopt enhanced
set output "kn-scales.png"

#set size ratio 0.6
set size 1,0.72
#set multiplot layout 1,2

# Figure for openwhisk
set origin 0,0

# set key right top width -0.5 height 0.25 font ',20' box opaque # horizontal
set key outside center maxrow 2 top font ",17" width -3 height 0.25 # box opaque
set border black

set ylabel "Number" font ",24" offset character -2, -1, 0

set ytics font ",24"
set lmargin 13
set rmargin 8
set bmargin 6
set tmargin 4

set yrange [0: 500]
set xrange [0: 480]
set xtics 60 nomirror out font ",24" offset character 0, -0.5, 0
set xlabel "Time (second)"  font ",24" offset character 0, -1.5, 0
set datafile missing "?"
set mxtics 3

# Define the first timestamp to calculate relative time
first_timestamp = 1725844720038996

# 20->60
# set xtics add ("0" 1720524608076890)

# 50->100
# set xtics add ("0" 1720515560120330)

set style line 1 lt 1 lc rgb '#d39234' lw 4 pt 7 ps 1
set style line 2 lt 1 lc rgb "#3172ae" lw 4 pt 7 ps 1
set style line 3 lt 1 lc rgb "#949494" lw 4 pt 7 ps 1
set style line 4 lt 1 lc rgb "#344035" lw 4 pt 7 ps 1
set style line 5 lt 1 lc rgb "#DF6F58" lw 4 pt 7 ps 1
set style line 6 lt 1 lc rgb "#A99A97" lw 4 pt 7 ps 1
set grid

plot  'kn-scales.dat' u ($1 - first_timestamp) / 1e6:($2/1) with linespoints linestyle 3 ti "desired-pods", \
	                                         '' u ($1 - first_timestamp) / 1e6:($3/1) with linespoints linestyle 1 ti "running-pods", \
