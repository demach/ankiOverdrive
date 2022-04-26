import argparse
from py_overdrive_sdk.py_overdrive import Overdrive
from time import sleep
import json

# parse input
parser = argparse.ArgumentParser()
parser.add_argument("--car", help="id of the bluetooth car", default="d7204d5e4bee")
parser.add_argument("--host", help="host of the node gateway for bluetooth communication", default='127.0.0.1')
parser.add_argument("--port", help="port of the node gateway for bluetooth communication", type=int, default=8005)
args = parser.parse_args()

SPEED = 400

TRACK_FILE = 'track_piece_list.txt'
TRACK_DATA = 'track_images/track_data.json'

lane = -70


positions = [[40, 20], [34, 0], [20, 30], [17, 8]]

with open(TRACK_FILE, "r") as file:
    track_data = file.read().split("\n")

with open(TRACK_DATA, "r") as file:
    track_info = json.loads(file.read())

# print(track_info['straight_locations_start'])

change_offset_piece = 0
desired_lane = 0
desired_piece = 0
desired_location = 0
locations = []

pos = 1
if pos == 1:
    desired_piece, desired_location = positions[0][0], positions[0][1]
    if desired_piece in [40]:
        piece_list = track_info['straight_locations_start']
        for i in range(len(piece_list)):
            if desired_location >= piece_list[i] and desired_location <= piece_list[i+1]:
                desired_lane = i
                #print(kwargs['offset'], kwargs['location'], i, -68+(i+1)*8.5)
                # print(i, piece_list[i])
                location_list = track_info['straight_scheme']
                loc_index = location_list[i].index(desired_location)
                locations = [location_list[i-1][loc_index], location_list[i][loc_index], location_list[i+1][loc_index]]



for i in track_data:
    x = i.split(',')
    #print(x[0])
    if int(x[0]) == desired_piece:
        change_offset_piece = track_data[track_data.index(i)-1].split(',')[0]

print(change_offset_piece)
LEFT = -68
RIGHT = +68

LANES = 16

OFFSET_PRO_LANE = 8.5

# define custom driving policy
def my_driving_policy(self, **kwargs):
    global track_data, lane

    #self.change_lane(1000,1000,-68)
    if kwargs['piece'] in [33, 34]:
        self.battery_level()
        print(kwargs['offset'])

    # if kwargs['offset'] < (-68+(6+1)*8.5 -8.5) or kwargs['offset'] > (-68+(6+1)*8.5 +8.5):
    #     self.change_lane(1000,1000,(-68+(6+1)*8.5))
        # self.change_lane(1000,1000,(-68+(i+1)*8.5))
    if kwargs['piece'] == int(change_offset_piece):
        self.change_lane(1000,1000,(-68+(desired_lane+1)*8.5))

    # if kwargs['piece'] == 40 and kwargs['location'] in [17, 20 ,23]:
    #     print(True)
    #     self.change_speed(0, 2000)
    #     sleep(2)
    #     self.change_speed(SPEED, 2000)
    #     self.change_lane(1000,1000, -68)
    

    if int(kwargs['piece']) == desired_piece and int(kwargs['location']) in locations:
        print(True)
        self.change_speed(0, 2000)
        sleep(2)
        self.change_speed(SPEED, 2000)
        self.change_lane(1000,1000, -68)



try:
    # let's drive!
    car = Overdrive(args.host, args.port, args.car, my_driving_policy)  # init overdrive object with custom policy
    car.change_speed(SPEED, 2000)  # set car speed with speed = 400, acceleration = 2000
    car.change_lane(1000,1000, -68)

    input()  # hold the program so it won't end abruptly
except (KeyboardInterrupt):
    # car.change_speed(200,2000)

    car.change_speed(0,2000)