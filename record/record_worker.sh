#!/usr/bin/bash

mkdir -p ~/outs && rm ~/outs/*

declare -A sessions
sessions=(
    ["first_seen"]="sudo journalctl -f -u kubelet | grep --line-buffered -E 'Receiving a new pod' > ~/outs/first_seen.txt"
    ["sandbox"]="sudo journalctl -f -u kubelet | grep --line-buffered -E 'Creating PodSandbox for pod|Created PodSandbox for pod' > ~/outs/sandbox.txt"
    ["container"]="sudo journalctl -f -u kubelet | grep --line-buffered -E 'Creating container in pod' > ~/outs/container.txt"
    ["startup_duration"]="sudo journalctl -f -u kubelet | grep --line-buffered -E 'Observed pod startup duration' > ~/outs/startup_duration.txt"
)

for session in "${!sessions[@]}"; do
    tmux kill-session -t "$session"
    tmux new-session -d -s "$session" "${sessions[$session]}"
    echo "Started tmux session '$session'"
done
