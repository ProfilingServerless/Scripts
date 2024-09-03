#!/usr/bin/bash

set -x

# The experiment is for 480 seconds
# No warmup, starts with steady 20 RPS load. 
# Then the truoghput will change at 300th second and logs are recorded for 90 seconds.
# so we start recording and 295th for 105s to ensure we coverd all proccess. (5 second setup time and 10 seconds hold time)

./clean.sh mghgm@pc40.cloudlab.umass.edu mghgm@pc27.cloudlab.umass.edu mghgm@pc31.cloudlab.umass.edu mghgm@pc30.cloudlab.umass.edu mghgm@pc38.cloudlab.umass.edu mghgm@pc26.cloudlab.umass.edu

tmux new-session -d -s "exp" "cd ~/loader && go run cmd/loader.go --config=cmd/config.json"

# waiting for load generator to start
sleep 5

./record.sh 250 150 mghgm@pc40.cloudlab.umass.edu mghgm@pc27.cloudlab.umass.edu mghgm@pc31.cloudlab.umass.edu mghgm@pc30.cloudlab.umass.edu mghgm@pc38.cloudlab.umass.edu mghgm@pc26.cloudlab.umass.edu

