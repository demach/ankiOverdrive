import json

def selector(desired_piece, desired_location, track_piece_list = 'track_piece_list.txt') -> list:
    global piece, desired_lane
    
    doable = True

    TRACK_DATA = 'track_data.json'

    with open(track_piece_list, "r") as file:
        track_data = file.read().split("\n")

    with open(TRACK_DATA, "r") as file:
        track_info = json.loads(file.read())

    start_piece_long = track_info['start_piece_long']
    start_piece_short = track_info['start_piece_short']
    straight_pieces = track_info['straight_pieces']
    curve_pieces = track_info['curve_pieces']

    reverse_list = False

    for info in track_data:
        info = info.split(',')
        if int(info[0]) == desired_piece:
            piece = int(info[1])
            #print(piece, info[2])
            if info[2].strip() == 'cw_1':
                reverse_list = True
            break

    if piece in start_piece_short:
        piece_list = track_info['start_33_locations_start']
        location_list = track_info['start_scheme_33']
    if piece in start_piece_long:
        piece_list = track_info['start_34_locations_start']
        location_list = track_info['start_scheme_34']
    if piece in straight_pieces:
        piece_list = track_info['straight_locations_start']
        location_list = track_info['straight_scheme']
    if piece in curve_pieces:
        piece_list = track_info['curve_locations_start']
        location_list = track_info['curve_scheme']
        
    if reverse_list:
        piece_list.reverse()
        location_list.reverse()
    for i in range(len(piece_list)):
        try:
            if not reverse_list:
                #print(reverse_list)
                if piece_list[i] == piece_list[-1]:
                    desired_lane = i
                    #print(piece_list,location_list, desired_location)
                    loc_index = location_list[i].index(desired_location)
                    if len(location_list[i-2]) == 2:
                        locations =  [location_list[i-2][loc_index-1], location_list[i-1][loc_index], location_list[i][loc_index]]
                    locations = [location_list[i-2][loc_index], location_list[i-1][loc_index], location_list[i][loc_index]]
                    break
                
                if int(desired_location) >= int(piece_list[i]) and int(desired_location) < int(piece_list[i+1]):
                    desired_lane = i
                    loc_index = location_list[i].index(int(desired_location))
                    if len(location_list[i-1]) == 2:
                        locations =  [location_list[i-1][loc_index-1], location_list[i][loc_index], location_list[i+1][loc_index]]
                    locations = [location_list[i-1][loc_index], location_list[i][loc_index], location_list[i+1][loc_index]]
                    break
            else:
                if piece_list[i] == piece_list[-1]:
                    desired_lane = i
                    loc_index = location_list[i].index(desired_location)
                    if len(location_list[i-2]) == 2:
                        locations =  [location_list[i-2][loc_index-1], location_list[i-1][loc_index], location_list[i][loc_index]]
                    locations = [location_list[i-2][loc_index], location_list[i-1][loc_index], location_list[i][loc_index]]
                    break
                
                if int(desired_location) >= int(piece_list[i]) and int(desired_location) < int(piece_list[i-1]):
                    desired_lane = i
                    #print(desired_lane)
                    loc_index = location_list[i].index(int(desired_location))
                    #print(loc_index)
                    if len(location_list[i-1]) == 2:
                        locations =  [location_list[i-1][loc_index-1], location_list[i][loc_index], location_list[i+1][loc_index]]
                    locations = [location_list[i-1][loc_index], location_list[i][loc_index], location_list[i+1][loc_index]]
                    break

        except ValueError as err:
            print(err)
            print("Location could not be found in piece")
            locations = []
            doable = False

    for data in track_data:
        x = data.split(',')
        if int(x[1]) == int(piece):
            
            piece_index = int(track_data.index(data)-2)
            if piece_index == -1:
                piece_index = -2
            change_offset_piece = int(track_data[piece_index].split(',')[1])
            break


    return [change_offset_piece, piece, desired_lane, locations, doable]
