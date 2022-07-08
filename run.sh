#! /bin/bash

# trap ctrl_c and call ctrl_c() --> exiting bash script with interrupt
trap ctrl_c INT


# kill all running scripts and exit this script
function ctrl_c() {
    echo "Exiting all scripts"
    kill $(ps -e | grep 'python3\|bash' | awk '{print $1}') &> /dev/null
    exit 0
} 

read -p "For first run enter \"first\", if you already have a car-uuid enter said car-uuid: " car_uuid

if [ "$car_uuid" = "first" ]; then
    sudo timeout 10 node node_app/node_socket_app/node_server.js 1 1 | stdbuf -o0 grep -I "SCAN" | grep -v -I "COMPLETED"
    
    exit 0

else
    # run all scripts after a sleep in the background
    sudo node node_app/node_socket_app/node_server 8005 $car_uuid &> /dev/null
    sleep 10
    cd python_app
    python3 opcua_api.py &
    sleep 5
    python3 opcua_client.py &
    sudo systemctl restart codesyscontrol.service &
    sleep 3
    echo "All Scripts are running"
    sleep 2
    while :
    do
        ((count++))
        sleep 1
    done

fi

