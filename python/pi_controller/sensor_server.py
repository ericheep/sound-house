import argparse
from pythonosc import udp_client, osc_message_builder, dispatcher, osc_server
import threading
from time import sleep


# ping pis
wallIPs = ['pione.local', 'pitwo.local', 'pithree.local',
                        'pifour.local', 'pifive.local', 'pisix.local',
                        'piseven.local', 'pieight.local']
ping_port = 5000

#### make client list for pinging pi's
client_list = []
for wall in wallIPs:

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=wall, help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=ping_port,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)
    client_list.append(client)
#####

##### listening server
rec_port = 12345
localIP = '192.168.0.7'
parser2 = argparse.ArgumentParser()
parser2.add_argument("--ip", default=localIP, help="The ip of the OSC server")
parser2.add_argument("--port", type=int, default=rec_port,
                    help="The port the OSC server is listening on")
args2 = parser2.parse_args()

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/w", print)

print(args2.ip, args2.port)

print('starting server')
server = osc_server.ForkingOSCUDPServer((args2.ip, args2.port), dispatcher)
server_thread = threading.Thread(target=server.serve_forever())
server_thread.start()
print('next line')

"""
server = ForkingOSCUDPServer((ip, port), dispatcher)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()
...
server.shutdown()
"""
#server.serve_forever()
#####


while True:
    msg = "/w"
    #for index, client in enumerate(client_list):
    #    client.send_message(msg, '')
    print(msg)
    sleep(1)

    #server.shutdown()