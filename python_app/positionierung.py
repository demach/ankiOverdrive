import argparse
import json
from time import sleep

from py_overdrive_sdk.py_overdrive import Overdrive
import position_selector

# parse input
parser = argparse.ArgumentParser()
parser.add_argument("--car", help="id of the bluetooth car", default="d7204d5e4bee")
parser.add_argument("--host", help="host of the node gateway for bluetooth communication", default='127.0.0.1')
parser.add_argument("--port", help="port of the node gateway for bluetooth communication", type=int, default=8005)
args = parser.parse_args()

# variables for positioning
SPEED = 300
LEFT_OFFSET = -68
RIGHT = +68
LANES = 16
OFFSET_PRO_LANE = 8.5

# file position
TRACK_FILE = 'track_piece_list.txt'

selection = position_selector.selector(2, 4, TRACK_FILE)

print(selection)


# define custom driving policy
def my_driving_policy(self, **kwargs):
    
    if int(kwargs['piece']) == int(selection[0]):
        self.change_lane(300,500,(LEFT_OFFSET+(selection[2])*OFFSET_PRO_LANE))
        self.change_speed(SPEED, 1000)

    if int(kwargs['piece']) == selection[1] and int(kwargs['location']) in selection[3]:
        self.change_speed(0, 2000)
        self.battery_level()
        sleep(1)
        self.change_speed(600, 2000)
        self.change_lane(500,1000, -68)
        
    print(kwargs)

try:
    # let's drive!
    car = Overdrive(args.host, args.port, args.car, my_driving_policy)  # init overdrive object with custom policy
    car.change_speed(SPEED, 2000)  # set car speed with speed = 400, acceleration = 2000
    car.change_lane(1000,1000, -68)

    input()  # hold the program so it won't end abruptly
except (KeyboardInterrupt):

    car.change_speed(0,2000)
