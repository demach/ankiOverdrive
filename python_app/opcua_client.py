from opcua import Client
import time

#opcua client
url = "opc.tcp://127.0.0.1:4841"
client = Client(url)
client.connect()
print("Client Connected")

#get nodes from opcua client and assing them to variables
heartbeat = client.get_node("ns=2;i=11")
pos = client.get_node("ns=2;i=12")

#predifine variables to store values
trackdiscovery = False
first_time = True
track_dict = {0:0}
position_value = 0

while True:
    #while no trackdiscovery was done, check for it
    if not trackdiscovery:
        trackdiscovery = client.get_node("ns=2;i=9").get_value()

    #if trackdiscovery was executed and this if hasnt run before, read values from track_piece_list and store them in a dict
    if trackdiscovery and first_time:
        first_time = False
        with open("track_piece_list.txt", "r") as track_list:
            track = track_list.readlines()
        for values in track:
            values = values.split(',')
            track_dict[int(values[1])] = values[0]

    #publish current position and heartbeat to opcua

    with open("position.txt", "r") as f:
        last_line = f.readlines()[-1]
    if trackdiscovery:
        position_value = int(track_dict[int(last_line.split(",")[0])])*1000 + int(last_line.split(",")[1])

    pos.set_value(position_value)
    heartbeat.set_value(True)
    time.sleep(0.1)
    heartbeat.set_value(False)
    time.sleep(0.1)