#!/usr/bin/bash

cd ~ 

declare -A pods
pods=(
    ["bind"]="$(kubectl -n kube-system get pods -l component=kube-scheduler -o jsonpath='{.items[0].metadata.name}')"
    ["create"]="$(kubectl -n kube-system get pods -l component=kube-controller-manager -o jsonpath='{.items[0].metadata.name}')"
    ["dec"]="$(kubectl -n knative-serving get pods -l app=autoscaler -o jsonpath='{.items[0].metadata.name}')"
    ["patch"]="$(kubectl -n knative-serving get pods -l app=autoscaler -o jsonpath='{.items[0].metadata.name}')"
    ["ticks"]="$(kubectl -n knative-serving get pods -l app=autoscaler -o jsonpath='{.items[0].metadata.name}')"
)

mkdir -p outs && rm ~/outs/*

declare -A sessions
sessions=(
    ["bind"]="kubectl -n kube-system logs --since=30s -f ${pods[bind]} | grep 'Pod Scheduled Successfully' > outs/bind"
    ["create"]="kubectl -n kube-system logs --since=30s -f ${pods[create]} | grep 'Controller created pod' > outs/create"
    ["dec"]="kubectl -n knative-serving logs --since=30s -f ${pods[dec]} | grep -E 'For=.* PodCount=.*' | jq '.' > outs/dec"
    ["patch"]="kubectl -n knative-serving logs --since=30s -f ${pods[patch]} | grep -E 'Successfully scaled to' | jq '.' > outs/patch"
    ["ticks"]="kubectl -n knative-serving logs --since=30s -f ${pods[ticks]} | grep -E 'For=.*Ticked' | jq '.' > outs/ticks"
)

for session in "${!sessions[@]}"; do
    tmux new-session -d -s "$session" "${sessions[$session]}"
    echo "Started tmux session '$session' for pod '${pods[$session]}'"
done

echo "All logs are being stored in the 'outs' directory."
