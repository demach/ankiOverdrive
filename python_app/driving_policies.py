def discovery(args) -> None:
    
    from py_overdrive_sdk.py_overdrive import Overdrive
    from pathlib import Path
    import time
    
    def track_discovery_policy(self, **kwargs) -> None:
    
        TRACK_FILE = 'track_piece_list.txt'
        def clockwise_format(bool_str) -> str:
            if bool_str.lower() == "true":
                return "cw_1"
            else:
                return "cw_0"
        
        def create_trackfile_insert(track_pieces_lst) -> str:
            write_lst = []
            for i, p in enumerate(track_pieces_lst):
                write_lst.append('{}, {}, {}'.format(i, p[0], p[2]))
            return "\n".join(write_lst)

        if not hasattr(self, 'track_pieces'):
            self.track_pieces = []
        if not hasattr(self, 'progress'):
            self.progress = 0
        if not hasattr(self, 'last_abspos'):
            self.last_abspos = (34, 0, False)
        
        if self.last_abspos != (int(kwargs["piece"]), int(kwargs["location"]), kwargs["is_clockwise"]):
            #new absolute car position detected
            with open("position.txt", "a") as f:
                f.write(f"{kwargs['piece']},{kwargs['location']}\n")

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

                    pieces = len(self.track_pieces)

                    del self.track_pieces, self.last_abspos
                    
                    #generate file so the api knows when the car has finished
                    with open("finished.txt", "a") as finished_file:
                        finished_file.write(str(pieces))
                    
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
        
    #generate car object for the task and delete it afterwards again
    car = Overdrive(args.host, args.port, args.car, track_discovery_policy)
    car.change_speed(400, 2000)  # set car speed with speed = 400, acceleration = 2000
    car.change_lane(400, 2000, -68)
    del car

def positioning(args, selection: list, fine_positioning: int) -> None:


    from py_overdrive_sdk.py_overdrive import Overdrive
    from pathlib import Path
    import time
    SPEED = 200
    LEFT_OFFSET = -68
    LANE_OFFSET = 8.5

    def positioning_policy(self, **kwargs) -> None:


        # write current position in a file
        with open("position.txt", "a") as f:
            f.write(f"{kwargs['piece']},{kwargs['location']}\n")

        #if the desired piece follows in two pieces change lane and slow down
        if int(kwargs['piece']) == int(selection[0]):
            self.change_lane(300,500,(LEFT_OFFSET+(selection[2])*LANE_OFFSET))
            self.change_speed(SPEED, 1000)

        #if the desired piece and the location matches the current piece and location, stop the car
        if int(kwargs['piece']) == selection[1] and int(kwargs['location']) in selection[3]:
            if int(fine_positioning) > 0:
                time.sleep(int(fine_positioning)/200)
            self.change_speed(0,2000)
            self.battery_level()
            
            # create finished file
            filename = Path("finished.txt")
            filename.touch()
            return
           
    #generate car object for the task and delete it afterwards again
    car = Overdrive(args.host, args.port, args.car, positioning_policy)
    car.change_speed(400, 2000)  # set car speed with speed = 400, acceleration = 2000
    car.change_lane(1000,1000, -68)
    del car
