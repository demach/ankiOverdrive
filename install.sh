#!/bin/bash

curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs

cd node_app/node_socket_app

npm install
cd ..
cd ..
cd python_app

pip3 install -r requirements.txt
