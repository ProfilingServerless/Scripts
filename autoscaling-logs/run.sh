#!/usr/bin/bash

# The experiment is for 480 seconds
# No warmup, starts with steady 20 RPS load. 
# Then the truoghput will change at 300th second and logs are recorded for 90 seconds.
# so we start recording and 295th for 105s to ensure we coverd all proccess. (5 second setup time and 10 seconds hold time)


tmux new-session -d -s "exp" "go run ~/loader/cmd/loader.go --config=~/loader/cmd/config.json"
# waiting for load generator to start
sleep 5
./record.sh 295 105 mghgm@hp167.utah.cloudlab.us mghgm@hp164.utah.cloudlab.us mghgm@hp196.utah.cloudlab.us mghgm@hp197.utah.cloudlab.us mghgm@hp166.utah.cloudlab.us


