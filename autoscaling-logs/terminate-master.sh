#!/usr/bin/bash

declare -A sessions
sessions=(
    ["bind"]=""
    ["create"]=""
    ["dec"]=""
    ["patch"]=""
    ["ticks"]=""
)

echo "Terminating all log collection tmux sessions..."
for session in "${!sessions[@]}"; do
    tmux send-keys -t "$session" C-c
    sleep 1
    tmux kill-session -t "$session"
    echo "Terminated tmux session '$session'"
done
echo "All log collection sessions have been terminated."

