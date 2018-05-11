import network_functions as nf
from settings import Settings
import argparse
from pythonosc import udp_client, osc_message_builder, dispatcher, osc_server
import threading

ctl_settings = Settings()

# initialize port connections
nf.initialize_sensorPing_ports(ctl_settings)
#nf.initialize_sensorReceiver_port(ctl_settings)

if __name__ == "__main__":
    wallIPs = ctl_settings.wallIPs
    port = ctl_settings.portGetSensorData
    client_list = []
    for IP in wallIPs:
        # sets up arguments for the dispatcher
        wallIP = IP
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip",
                            default=wallIP, help="The ip to listen to")
        parser.add_argument("--port",
                            type=int, default=port, help="The port to listen on")
        args = parser.parse_args()
        client = udp_client.SimpleUDPClient(args.ip, args.port)
        client_list.append(client)
    ctl_settings.wallSensor_clients = client_list

    # the thread that listens for the OSC messages
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/w", print)

    # the server we're listening on
    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)

    print("Serving on {}".format(server.server_address))

    # here we go!
    server.serve_forever()

while True:

    msg = "/w"
    for index, client in enumerate(ctl_settings.wallSensor_clients):
        client.send_message(msg, 0) # is a val needed here?
        #print(msg)

    #ui = input('input: ')
    #if ui == 'q':
    #    ctl_settings.server.shutdown()
    #    break