import argparse
from pythonosc import udp_client, osc_message_builder, dispatcher, osc_server
import threading
from time import sleep

def make_client(IP, port):
    # set IP and port
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=IP, help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=port,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()
    # make client
    client = udp_client.SimpleUDPClient(args.ip, args.port)
    return client

def send(client, msg):
    msg1 = msg
    msg2 = 0
    client.send_message(msg1, msg2)
    print(msg1, msg2)


IP = "127.0.0.1"
port = 5000#12345

wall_IPs = ['pione.local', 'pitwo.local', 'pithree.local', 'pifour.local',
            'pifive.local', 'pisix.local', 'piseven.local', 'pieight.local']

#local_client = make_client(IP, port)

wall_clients = []
for wall_IP in wall_IPs:
    client = make_client(wall_IP, port)
    wall_clients.append(client)

while True:
    for client in wall_clients:
        send(client, "/w")
    sleep(1)