# Basic Experiment
In this experiment we aim to only observe the behaviour of control plane and data plane under simple load of function invocations.

## Cluster Setup
1. Create a 6 node cluster on cloudlab (Create a Applicable nodes: `c220g5` , `xl170`, and `rs440`
2. On loader: `git clone https://github.com/vhive-serverless/invitro.git /tmp/invitro`
3. Change `/tmp/invitro/scripts/setup/setup.cfg` to following:
```
VHIVE_BRANCH='v1.7.1'
LOADER_BRANCH='main'
CLUSTER_MODE='container' # choose from {container, firecracker, firecracker_snapshots}
PODS_PER_NODE=240
DEPLOY_PROMETHEUS=true
```
4. On loader: `cd /tmp/invitro && ./scripts/setups/create_multinode.sh <master-ip> <loader-ip> <worker01-ip> <worker02-ip> <worker03-ip> <worker04-ip>`
5. (optional) Zipkin???
6. On loader: `git clone https://github.com/ProfilingServerless/experiment-toolset.git ~/experiment-toolset && ~/experiment-toolset/setup/reconfigure_loader.sh`
7. On master: `git clone https://github.com/ProfilingServerless/experiment-toolset.git ~/experiment-toolset && ~/experiment-toolset/setup/reconfigure_master.sh`
8. On workers: `git clone https://github.com/ProfilingServerless/experiment-toolset.git ~/experiment-toolset && ~/experiment-toolset/setup/reconfigure_worker.sh`
9. Trace Generator??
