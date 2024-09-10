set terminal pngcairo size 800,600 enhanced font 'Verdana,10'
set output 'startup.png'

set title "Startup Latency"
set style data histogram
set style histogram cluster gap 1
set style fill solid border -1
set boxwidth 0.9

set xtics rotate by -45
set grid ytics
set ylabel "Latency (s)"
set xlabel "Range"

# Format the y-axis to display second
set format y "%.1f s"

# Automatically scale the y-axis to divide values by 10^6 (convert ns to ms)
set ytics nomirror

# Legend
set key inside top left

# Plot the data and convert y-values from nanoseconds to milliseconds
plot 'startup.dat' using ($2/1000000):xtic(1) title "p50", \
     '' using ($3/1000000) title "p80", \
#     '' using ($4/1000000) title "p90", \
#     '' using ($5/1000000) title "p99"
