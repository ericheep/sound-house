import network_functions as nf
from time import sleep

# select runtime mode or dev mode
ui = input("1. Run Program (networked) 2. Dev. Mode (local): ")

if ui == "1":
    IP = "192.168.07"
    sending = "pis"
elif ui == "2":
    IP = "127.0.0.1"
    sending = "local"

# pi hostnames
wall_IPs = ['pione.local', 'pitwo.local', 'pithree.local', 'pifour.local',
            'pifive.local', 'pisix.local', 'piseven.local', 'pieight.local']

# ports for sending and receiving
ping_port = 5000
rec_port = 12345


# create one local client or 8 pi clients
wall_clients = []
if sending == "pis":
    for wall_IP in wall_IPs:
        client = nf.make_client(wall_IP, ping_port)
        wall_clients.append(client)
elif sending == "local":
    client = nf.make_client(IP, ping_port)
    wall_clients.append(client)

# create listening server
local_server = nf.make_server(IP, rec_port, "/w")

wall_names = ["pione", "pitwo", "pithree", "pifour", "pifive", "pisix",
              "piseven", "pieight"]
wall_vals = [0, 0, 0, 0, 0, 0, 0]


# main program loop
while True:
    # ping
    for client in wall_clients:
        nf.send(client, "/w", sending)
    # exit loop option
    ui = input("'q' to quit: ")
    if ui == 'q':
        local_server.shutdown()
        break