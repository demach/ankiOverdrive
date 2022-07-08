import datetime
import argparse, time

from opcua import Server, ua
from random import randint
from pathlib import Path

from py_overdrive_sdk.py_overdrive import Overdrive
from driving_policies import discovery, positioning
import position_selector

# parse input
parser = argparse.ArgumentParser()
parser.add_argument("--car", help="id of the bluetooth car", default="d7204d5e4bee")
parser.add_argument("--host", help="host of the node gateway for bluetooth communication", default='127.0.0.1')
parser.add_argument("--port", help="port of the node gateway for bluetooth communication", type=int, default=8005)
args = parser.parse_args()

# name of the output file
TRACK_FILE = 'track_piece_list.txt'
POSITION_FILE = 'position.txt'

# variables for positioning
SPEED = 300
LEFT_OFFSET = -68
RIGHT = +68
LANES = 16
OFFSET_PRO_LANE = 8.5

# track_file clearing and generation
filename = Path(TRACK_FILE)
filename.unlink()
filename.touch()

#delete position.txt file so it doesnt fill up the internal storage
positionfile = Path(POSITION_FILE)
positionfile.unlink()

#create position file with init value
with open(POSITION_FILE, 'a') as f:
    f.write("0,0\n")

#create opcua server
server = Server()

url = "opc.tcp://0.0.0.0:4841"
server.set_endpoint(url)

name = "OPC_SIMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

#define and set variables to use with opcua server
Start = Param.add_variable(addspace, "Start", False, ua.VariantType.Boolean)
SetupModus = Param.add_variable(addspace, "Setupmodus", False, ua.VariantType.Boolean)
PosAnwahl = Param.add_variable(addspace, "Positionsanwahl", 0, ua.VariantType.UInt32)
NachPos = Param.add_variable(addspace, "Nachpositionierung", 0, ua.VariantType.Int32)

SystemBereit = Param.add_variable(addspace, "System_Bereit", False, ua.VariantType.Boolean)
FahrzeugFaehrt = Param.add_variable(addspace, "Fahrzeug_faehrt", False, ua.VariantType.Boolean)
FahrzeugSteht = Param.add_variable(addspace, "Fahrzeug_steht", False, ua.VariantType.Boolean)
TrackdiscoveryErfolgreich = Param.add_variable(addspace, "Trackdiscovery_Erfolgreich", False, ua.VariantType.Boolean)
SystemFehler = Param.add_variable(addspace, "System_Fehler", False, ua.VariantType.Boolean)
Heartbeat = Param.add_variable(addspace, "Heartbeat", False, ua.VariantType.Boolean)
AktuellePos = Param.add_variable(addspace, "Aktuelle_Position", 0, ua.VariantType.UInt32)
AnzahlStreckenstueck = Param.add_variable(addspace, "Anzahl_Streckenstueck", 0, ua.VariantType.UInt32)

Start.set_writable()
SetupModus.set_writable()
PosAnwahl.set_writable()
NachPos.set_writable()

SystemBereit.set_writable()
FahrzeugFaehrt.set_writable()
FahrzeugSteht.set_writable()
TrackdiscoveryErfolgreich.set_writable()
SystemFehler.set_writable()
Heartbeat.set_writable()
AktuellePos.set_writable()
AnzahlStreckenstueck.set_writable()

server.start()
print("Server started at {}".format(url))

trackdiscovery = False

while True:
    #always reset these values
    SystemBereit.set_value(True)
    FahrzeugSteht.set_value(True)
    FahrzeugFaehrt.set_value(False)
    
    reset = False
    
    #if one of these values changes, store them for usage
    start_bit = server.get_node("ns=2; i=2").get_value()
    setupmode = server.get_node("ns=2; i=3").get_value()
    desired_position = server.get_node("ns=2; i=4").get_value()
    fine_positioning = server.get_node("ns=2; i=5").get_value()
    
    
    if start_bit:

        # update values to current state
        FahrzeugFaehrt.set_value(True)
        FahrzeugSteht.set_value(False)
        SystemBereit.set_value(False)
        SystemFehler.set_value(False)
        if not setupmode and trackdiscovery:
            if desired_position > 100: 
                piece = int(str(desired_position)[:-3])
                position = int(str(desired_position)[-3:])
            else:
                piece = 0
                position = int(desired_position)
            selection = position_selector.selector(piece, position, TRACK_FILE)
            
            #if position is not available on the track publish an error bit 
            if selection[4]:
                positioning(args, selection, int(fine_positioning))
            
                #wait till the car has finished
                while not Path("finished.txt").exists():
                    time.sleep(0.1)
                Path("finished.txt").unlink()
            else:
                SystemFehler.set_value(True)
            #reset start value
            Start.set_value(reset)
            
        
        #start trackdiscovery
        if setupmode:
            pieces = discovery(args)
            AnzahlStreckenstueck.set_value(0)
            while not Path("finished.txt").exists():
                time.sleep(0.1)
            
            #wait till the car has finished
            with open("finished.txt", "r") as finished_file:
                pieces = finished_file.readlines()[0]
            AnzahlStreckenstueck.set_value(int(pieces))
            
            Path("finished.txt").unlink()
            
            SetupModus.set_value(reset)
            Start.set_value(reset)
            TrackdiscoveryErfolgreich.set_value(True)
            trackdiscovery = True
        
        else:
            Start.set_value(reset)
            
    time.sleep(0.1)