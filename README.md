[General]
- python_wrapper for anki Overdrive
- edited the Overdrive-Class from the main-project for more actions
- github project we used as a base: https://github.com/jacopotagliabue/anki-drive-python-sdk
- Information: https://transparent-scorpio-4cb.notion.site/Projekt-6-Semester-8e1bfe87eefb4661ac9e9da6f463b216

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
    - program to discover the track: fts_track_discovery.py
    - program to drive to specific position: positionierung.py
- anki.json file contains uuid for the cars we tested the project with

- to start all programms with on script: 
    - run from main directory "bash run.sh"
    - on the first run enter: first
    - on the second run, you can enter the found uuid
        --> this will execute all scripts for that uuid
        
    [Attention]
    - if you dont have a codesys-runtime installed, this script will throw an error:
        - to disable reastarting a codesys-runtime, you have manually comment it in the run.sh script
