#!/usr/bin/bash

set -x

RES_DIR=$(date +"%dof%m-%H:%M")

mkdir -p $RES_DIR
cd $RES_DIR

scp -r vhive-loader:/users/mghgm/outs/* .

echo "Extracting logs ..."
cd $RES_DIR
tar xvf master.tar.gz 

touch e2es
workers=$(ls worker-*.tar.gz)
for w in $workers; do
    tar xvf $w && cat e2e >> e2es && rm e2e
done

# Remove all compressed files
rm *.tar.gz

cd ..
echo "All logs are extracted"

mkdir -p "$RES_DIR/clean"
RESULT_PATH=$RES_DIR python pods.py
