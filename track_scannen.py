import argparse
from py_overdrive_sdk.py_overdrive import Overdrive

# parse input
parser = argparse.ArgumentParser()
parser.add_argument("--car", help="id of the bluetooth car", default="daa87a9810c9")
parser.add_argument("--host", help="host of the node gateway for bluetooth communication", default='127.0.0.1')
parser.add_argument("--port", help="port of the node gateway for bluetooth communication", type=int, default=8005)
args = parser.parse_args()

TRACK_FILE = 'track_data.txt'   #   --> Output-File

lane = -70
# define custom driving policy
def track_discovery_policy(self, **kwargs) --> None:
    global lane
    """
    A policy to discover every piece of the track and write it to a file
    Change lanes to also get every trackposition

    :param kwargs will be a location event as dict produced by the 'build_location_event' function
    :return:
    """
    if kwargs['piece'] in [33]:
        print(lane)
        self.change_lane(1000,1000,lane)
        if int(kwargs['offset']) <= 70:
            lane += 10
        if lane == 70:
            self.change_speed(0,2000)

    with open(TRACK_FILE, 'a') as track_f:
        track_f.write('{}\n'.format(kwargs))


try:
    # let's drive!
    car = Overdrive(args.host, args.port, args.car, track_discovery_policy)  # init overdrive object with custom policy
    car.change_speed(500, 2000)  # set car speed with speed = 400, acceleration = 2000
    car.change_lane(1000,1000,-1000)    # set initial lane to the furthest left
    input()  # hold the program so it won't end abruptly
except (KeyboardInterrupt):
    car.change_speed(0,2000)    # stop car after interrupting program