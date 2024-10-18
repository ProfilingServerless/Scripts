#/usr/bin/bash

# pod_name,first_seen
awk -F' ' '{print $NF","$7}' ~/outs/first_seen.txt | sed 's/pod="\([^"]*\)"/\1/' > first_seen_clean.csv

# pod_name,e2e_duration,watch_observe_running_time
awk -F' ' '{ print $14","$16","$35}' ~/outs/startup_duration.txt | sed -E 's/pod="([^"]*)",podStartE2EDuration="([0-9.]+)s",([0-9:]+)/\1,\2,\3/' > startup_duration_clean.csv
