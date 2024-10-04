#!/usr/bin/bash

set -x

# The experiment is for 480 seconds
# No warmup, starts with steady 20 RPS load. 
# Then the truoghput will change at 240th second and logs are recorded for 90 seconds.
# so we start recording and 240 for 120s to ensure we coverd all proccess. (5 second setup time and 10 seconds hold time)

./clean.sh mghgm@ms1006.utah.cloudlab.us mghgm@ms0830.utah.cloudlab.us mghgm@ms1045.utah.cloudlab.us mghgm@ms0802.utah.cloudlab.us mghgm@ms0916.utah.cloudlab.us

tmux new-session -d -s "exp" "cd ~/loader && go run cmd/loader.go --config=cmd/config.json"

# waiting for load generator to start
sleep 5

./record.sh 240 150 mghgm@ms1006.utah.cloudlab.us mghgm@ms0830.utah.cloudlab.us mghgm@ms1045.utah.cloudlab.us mghgm@ms0802.utah.cloudlab.us mghgm@ms0916.utah.cloudlab.us

