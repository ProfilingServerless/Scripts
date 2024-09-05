#!/usr/bin/bash

set -x

server_exec() {
    ssh -oStrictHostKeyChecking=no -p 22 "$1" "$2";
}

mkdir -p ~/outs && rm ~/outs/*

WAIT_TIME=$1
DURATION=$2
SCRIPT_PATH="~/control-plane-scripts/record-autoscaling-logs"
shift 2

common_init() {
    server_exec $1 "rm -rf ~/control-plane-scripts && cd ~ && git clone https://github.com/ProfilingServerless/control-plane-scripts.git"
} 

for node in "$@"; do
    common_init $node
done

MASTER_NODE=$1
# to have workers in left args
shift

sleep $WAIT_TIME
echo "Start recording"

server_exec $MASTER_NODE "$SCRIPT_PATH/record-master.sh" 

for worker in "$@"; do
    server_exec $worker "$SCRIPT_PATH/record-worker.sh"
done

echo "Waiting for $DURATION seconds"
sleep $DURATION

server_exec $MASTER_NODE "$SCRIPT_PATH/terminate-master.sh"
server_exec $MASTER_NODE "cd ~ && tar czf outs.tar.gz --directory=outs ."
scp $MASTER_NODE:/users/mghgm/outs.tar.gz ~/outs/master.tar.gz 

i=1
for worker in "$@"; do
    server_exec $worker "$SCRIPT_PATH/terminate-worker.sh"
    server_exec $worker "cd ~ && tar czf outs.tar.gz --directory=outs ."
    scp $worker:/users/mghgm/outs.tar.gz ~/outs/worker-$i.tar.gz
    ((i+=1))
done
echo "Terminated all sessions"
