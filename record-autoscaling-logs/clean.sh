#!/usr/bin/bash

set -x

server_exec() {
    ssh -oStrictHostKeyChecking=no -p 22 "$1" "$2";
}

MASTER_NODE=$1

# just workers on params
shift

SCRIPT_PATH="~/control-plane-scripts/record-autoscaling-logs"

tmux kill-session -t "exp"

server_exec $MASTER_NODE "$SCRIPT_PATH/terminate-master.sh"
for worker in "$@"; do
    server_exec $worker "$SCRIPT_PATH/terminate-worker.sh"
done


