[General]
- python_wrapper for anki Overdrive
- edited the Overdrive-Class from the main-project for more actions
- github project we used as a base: https://github.com/jacopotagliabue/anki-drive-python-sdk

[Goal]
- Use anki-overdrive as a transport system

[Installation]
- Download Repo to Raspberry Pi
- use "bash install.sh" to install all necessary modules

[Usage]
- node server:
    - cd to node directory
    - command to connect node server to Anki-Overdrive car:
        -   "sudo node node_server.js [port] [car_uuid]"
        -   default port: 8005
    - car_uuid can be retrieved by setting port==1 and car_uuid==1
    - node_server scans all ble devices and returns them
    - use desired car_uuid when connecting to car

- python program:
    - either edit default parameter for car_uuid in python file or pass it in command_line as an argrument (--car [car_uuid])
    - default port: 8005
- anki.json file contains uuid for the cars we tested the project with
