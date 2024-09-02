#!/usr/bin/bash

cd ~ 
mkdir -p ~/outs && rm ~/outs/*

declare -A sessions
sessions=(

    ["e2e"]="sudo journalctl --since \""$(date -d "30 seconds ago" +"%Y-%m-%d %H:%M:%S")"\" -f -u kubelet | grep E2E > outs/e2e"
)

# Loop through the sessions array
for session in "${!sessions[@]}"; do
    # Create a new tmux session and run the command
    tmux new-session -d -s "$session" "${sessions[$session]}"
    
    echo "Started tmux session '$session' with command: ${sessions[$session]}"
done

echo "All tmux sessions have been created and detached."
