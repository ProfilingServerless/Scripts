#!/usr/bin/bash

function i_kubelet_loglevel () {
    KUBELET_CONFIG_FILE="/etc/default/kubelet"
    sed -i 's/--v=[0-9]\+/--v=4/' "$KUBELET_CONFIG_FILE" 
    systemctl daemon-reload
    systemctl restart kubelet
}

i_kubelet_loglevel
