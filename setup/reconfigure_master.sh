#!/usr/bin/bash

# The script is written in a way to keep idempotency


function i_set_activator_image {
    kubectl -n knative-serving patch deployment activator -p '{"spec": {"template": {"spec": {"containers": [{"name": "activator", "image": "lkondras/activator-ecd51ca5034883acbe737fde417a3d86:rr-policy"}]}}}}'
    if [ $? -eq 0 ]; then
        echo "Changed activator image to round-robin policy"
    else
        echo "Failed to change activator image"
        exit 1
    fi
}

function ii_scheduler_loglevel {
    MANIFEST_PATH="/etc/kubernetes/manifests/kube-scheduler.yaml"
    LOG_LEVEL=$(yq e '.spec.containers[].command[] | select(. == "--v=5")' "$MANIFEST_PATH")
    if [[ -z "$LOG_LEVEL" ]]; then
        yq e -i '.spec.containers[].command += ["--v=5"]' "$MANIFEST_PATH"
    fi
    unset LOG_LEVEL 
    unset MANIFEST_PATH
}

function iii_controller_manager_loglevel {
    MANIFEST_PATH="/etc/kubernetes/manifests/kube-scheduler.yaml"
    LOG_LEVEL=$(yq e '.spec.containers[].command[] | select(. == "--v=5")' "$MANIFEST_PATH")
    if [[ -z "$LOG_LEVEL" ]]; then
        yq e -i '.spec.containers[].command += ["--v=5"]' "$MANIFEST_PATH"
    fi
    unset LOG_LEVEL 
    unset MANIFEST_PATH
}

function iv_autoscaler_loglevel {
    LOG_LEVEL=$(kubectl -n knative-serving get cm config-logging -o jsonpath="{.data.loglevel\.autoscaler}" | grep "debug")
    if [[ -z "$LOG_LEVEL" ]]; then
        kubectl -n knative-serving patch cm config-logging --type='merge' -p '{"data":{"loglevel.autoscaler":"debug"}}'
    fi
    unset LOG_LEVEL
}

function v_kubelet_loglevel () {
    KUBELET_CONFIG_FILE="/etc/default/kubelet"
    sed -i 's/--v=[0-9]\+/--v=4/' "$KUBELET_CONFIG_FILE" 
    systemctl daemon-reload
    systemctl restart kubelet
}

i_set_activator_image
ii_scheduler_loglevel
iii_controller_manager_loglevel
iv_autoscaler_loglevel
v_kubelet_loglevel
