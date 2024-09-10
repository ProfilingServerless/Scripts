set terminal pngcairo size 800,600 enhanced font 'Verdana,10'
set output 'decisions.png'

set title "Decision Latency"
set style data histogram
set style histogram cluster gap 1
set style fill solid border -1
set boxwidth 0.9

set xtics rotate by -45
set grid ytics
set ylabel "Latency (microseconds)"
set xlabel "Throughput"

# Legend
set key inside top left

# Define the column labels
plot 'decision.dat' using 2:xtic(1) title "p50", \
     '' using 3 title "p80", \
#     '' using 4 title "p90", \
#     '' using 5 title "p99"
