#!/usr/bin/env bash

sudo apt-get install -y python-setuptools python-dev build-essential

sudo easy_install pip

pip install grpcio
pip install grpcio-tools
pip install docker

market_proto=./

for entry in $market_proto/*;
do
    if [ ${entry: -6} == '.proto' ]
    then
        echo $entry;
        python -m grpc_tools.protoc \
            -I$market_proto \
            --python_out=$market_proto \
            --grpc_python_out=$market_proto $entry;
    fi
done
