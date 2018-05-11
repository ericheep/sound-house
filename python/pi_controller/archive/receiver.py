import argparse
from pythonosc import udp_client, osc_message_builder, dispatcher, osc_server
import threading
from time import sleep

IP = "192.168.07"#"127.0.0.1"
port = 12345


def make_server(IP, port, address):
    # set IP and port to listen on
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=IP, help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=port,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    # the thread that listens for the OSC messages
    dispatcherX = dispatcher.Dispatcher()
    dispatcherX.map(address, print)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port),
                                              dispatcherX)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    print("Serving on {}".format(server.server_address))

    return server



local_server = make_server(IP, port, "/w")

while True:
    print("now something new")
    ui = input('enter: ')
    if ui == 'q':
        local_server.shutdown()
        break
