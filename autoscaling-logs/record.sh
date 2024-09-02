#!/usr/bin/bash

server_exec() {
    ssh -oStrictHostKeyChecking=no -p 22 "$1" "$2";
}

WAIT_TIME=$1
DURATION=$2
shift 2

MASTER_NODE=$1
# to have workers in left args
shift

sleep $WAIT_TIME
echo "Start recording"

server_exec $MASTER_NODE ./record-master.sh 

for worker in "$@"; do
    server_exec $worker ./record-worker.sh
done

echo "Waiting for $DURATION seconds"
sleep $DURATION

server_exec $MASTER_NODE ./terminate-master.sh
for worker in "$@"; do
    server_exec $worker ./terminate-worker.sh
done

echo "Terminated all sessions"
