"""
    Basic and NON-general example of a track discovery policy: the car will collect all piece IDs from the track
    and store them in a text file.

    If you then run 'create_track_image.py' a png image of the map will be produced.
"""

import argparse, time
from py_overdrive_sdk.py_overdrive import Overdrive
from driving_policies import discovery

# parse input
parser = argparse.ArgumentParser()
parser.add_argument("--car", help="id of the bluetooth car", default="d7204d5e4bee")
parser.add_argument("--host", help="host of the node gateway for bluetooth communication", default='127.0.0.1')
parser.add_argument("--port", help="port of the node gateway for bluetooth communication", type=int, default=8005)
args = parser.parse_args()

# name of the output file
TRACK_FILE = 'track_piece_list.txt'


# define custom driving policy for track discovery


# let's drive!

try:
    discovery(args)
    # the car will change speed when traversing the starting straight segment
    input()  # hold the program so it won't end abruptly

except KeyboardInterrupt:
    car.change_speed(0, 2000)
