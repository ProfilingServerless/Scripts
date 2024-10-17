#!/usr/bin/bash

sudo journalctl -f -u kubelet | grep --line-buffered -E "Processing pod event|Processing pod event done" > ~/sync_pods.txt
