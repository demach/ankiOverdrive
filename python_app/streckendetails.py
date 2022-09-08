import argparse, time
from py_overdrive_sdk import Overdrive
from pathlib import Path

# parse input
parser = argparse.ArgumentParser()
parser.add_argument("--car", help="id of the bluetooth car", default="d7204d5e4bee")
parser.add_argument("--host", help="host of the node gateway for bluetooth communication", default='127.0.0.1')
parser.add_argument("--port", help="port of the node gateway for bluetooth communication", type=int, default=8005)
args = parser.parse_args()

# name of the output file
TRACK_FILE = 'trackinformation.txt'


# define custom driving policy for track discovery

def trackinformation(self, **kwargs) -> None:
    
    """
    
    Während der Fahrt mit dem Auto wichtige Parameter, die das Auto überträgt auslesen und in der Konsole ausgeben
    
    """

    print(kwargs['location'], kwargs['piece'], kwargs['offset'])
    with open(TRACK_FILE, "a") as f:
        f.write(str(kwargs['location']) + ", " + str(kwargs['piece']) + ", " + str(kwargs['offset']) + "\n")


# let's drive!

try:
    
    car = Overdrive(args.host, args.port, args.car, trackinformation)
    car.change_speed(400, 2000)


    input()  # hold the program so it won't end abruptly

except KeyboardInterrupt:
    car.change_speed(0, 2000)