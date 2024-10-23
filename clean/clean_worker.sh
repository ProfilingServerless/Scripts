#/usr/bin/bash

# pod_name,first_seen
awk -F' ' '{print $NF","$7}' ~/outs/first_seen.txt | sed 's/pod="\([^"]*\)"/\1/' > first_seen_clean.csv

# pod_name,e2e_duration,watch_observe_running_time
awk -F' ' '{ print $14","$16","$35}' ~/outs/startup_duration.txt | sed -E 's/pod="([^"]*)",podStartE2EDuration="([0-9.]+)s",([0-9:]+)/\1,\2,\3/' > startup_duration_clean.csv

# pod_name,start_creation,type
awk -F' ' '/Name:queue-proxy/ { print $NF","$7",queue" } /Name:user-container/ { print $NF","$7",user" }' ~/outs/container.txt | sed 's/pod="\([^"]*\)"/\1/' > container_clean.csv

# pod_name,timestamp,end/start
awk -F' ' '/Creating/ { print $NF","$7",start" } /Created/ { print $NF","$7",end" }' ~/outs/sandbox.txt | sed 's/pod="\([^"]*\)"/\1/' > sandbox_clean.csv
