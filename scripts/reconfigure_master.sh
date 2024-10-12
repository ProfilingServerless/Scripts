#!/usr/bin/bash

# The script is written in a way to keep idempotency

kubectl -n knative-serving patch deployment activator -p '{"spec": {"template": {"spec": {"containers": [{"name": "activator", "image": "lkondras/activator-ecd51ca5034883acbe737fde417a3d86:rr-policy"}]}}}}'

if [ $? -eq 0 ]; then
    echo "Changed activator image to round-robin policy"
else
    echo "Failed to change activator image"
    exit 1
fi


