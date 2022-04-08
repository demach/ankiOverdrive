"""
    Basic and NON-general example of a track discovery policy: the car will collect all piece IDs from the track
    and store them in a text file.

    If you then run 'create_track_image.py' a png image of the map will be produced.
"""

import argparse, time
from py_overdrive_sdk.py_overdrive import Overdrive

# parse input
parser = argparse.ArgumentParser()
parser.add_argument("--car", help="id of the bluetooth car", default="daa87a9810c9")
parser.add_argument("--host", help="host of the node gateway for bluetooth communication", default='127.0.0.1')
parser.add_argument("--port", help="port of the node gateway for bluetooth communication", type=int, default=8005)
args = parser.parse_args()

# name of the output file
TRACK_FILE = 'track_piece_list.txt'


# define custom driving policy for track discovery
def discovery_driving_policy(self, **kwargs) -> None:
    def clockwise_format(bool_str) -> str:
        if bool_str.lower() == "true":
            return "cw_1"
        else:
            return "cw_0"
    
    def create_trackfile_insert(track_pieces_lst) -> str:
        write_lst = []
        for p in track_pieces_lst:
            write_lst.append('{},{}'.format(p[0], p[2]))
        return "\n".join(write_lst)

    if not hasattr(self, 'track_pieces'):
        self.track_pieces = []
    if not hasattr(self, 'progress'):
        self.progress = 0
    if not hasattr(self, 'last_abspos'):
        self.last_abspos = (34, 0, False)
    
    if self.last_abspos != (int(kwargs["piece"]), int(kwargs["location"]), kwargs["is_clockwise"]):
        #new absolute car position detected
        if self.track_pieces == [] and int(kwargs["piece"]) == 34 and kwargs["is_clockwise"] == "True":
            self.turn()
            self.change_lane(400, 2000, -68)
            self.track_pieces.append((34, 0, "cw_0"))
        elif self.track_pieces == [] and int(kwargs["piece"]) == 34 and kwargs["is_clockwise"] == "False":
            self.track_pieces.append((34, 0, "cw_0"))

        if (34, 0, "cw_0") in self.track_pieces:
            
            if int(kwargs["piece"]) == 34 and len(self.track_pieces) > 3 and open(TRACK_FILE, 'r').read() != create_trackfile_insert(self.track_pieces):
                #finished first part of scan process
                print("Finished first part of scan process: 1/2")
                with open(TRACK_FILE, 'w') as dok:
                    dok.write(create_trackfile_insert(self.track_pieces))
                self.track_pieces = []
                self.progress = 50
                self.change_speed(400, 1000)

            elif int(kwargs["piece"]) == 34 and len(self.track_pieces) > 3 and open(TRACK_FILE, 'r').read() == create_trackfile_insert(self.track_pieces):
                #track_discovery_finished when discovered data matches track_file_data
                print("Finished track discovery!")
                self.change_speed(0, 1000)
                del self.track_pieces, self.last_abspos
                exit()


            elif (int(kwargs["piece"]) != self.track_pieces[-1][0] or kwargs["is_clockwise"] != self.last_abspos[2]) and kwargs["piece"] != 34:
                #new piece number or
                #direction_change
                self.track_pieces.append((int(kwargs["piece"]), int(kwargs["location"]), clockwise_format(kwargs["is_clockwise"])))

            elif int(kwargs["piece"]) == self.track_pieces[-1][0] and kwargs["is_clockwise"] == self.last_abspos[2]:
                if clockwise_format(kwargs["is_clockwise"]) == "cw_0" and int(kwargs["location"]) < self.last_abspos[1]:
                    self.track_pieces.append((int(kwargs["piece"]), int(kwargs["location"]), clockwise_format(kwargs["is_clockwise"])))
                elif clockwise_format(kwargs["is_clockwise"]) == "cw_1" and int(kwargs["location"]) > self.last_abspos[1]:
                    self.track_pieces.append((int(kwargs["piece"]), int(kwargs["location"]), clockwise_format(kwargs["is_clockwise"])))
                   
        self.last_abspos = (int(kwargs["piece"]), int(kwargs["location"]), kwargs["is_clockwise"])
        
    return


# let's drive!

try:
    with open(TRACK_FILE, 'w') as dok:
        dok.write("")
    car = Overdrive(args.host, args.port, args.car, discovery_driving_policy)  # init overdrive object with custom policy
    car.change_speed(400, 2000)  # set car speed with speed = 400, acceleration = 2000
    car.change_lane(400, 2000, -68)
    # the car will change speed when traversing the starting straight segment
    input()  # hold the program so it won't end abruptly

except KeyboardInterrupt:
    car.change_speed(0, 2000)