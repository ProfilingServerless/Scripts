#/usr/bin/bash

# The script is written in a way to keep idempotency

function i_install_go {
    cd /tmp && wget https://go.dev/dl/go1.23.2.linux-amd64.tar.gz
    sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.23.2.linux-amd64.tar.gz 
    if [[ ":$PATH:" != *":/usr/local/go/bin:"* ]]; then
        echo "export PATH=$PATH:/usr/local/go/bin" | tee -a $HOME/.bashrc
    fi
    source $HOME/.bashrc
}

i_install_go

echo "run 'source ~/.bashrc'"

