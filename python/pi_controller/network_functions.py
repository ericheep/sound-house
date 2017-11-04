import argparse
from pythonosc import udp_client, osc_message_builder

def initialize_OscControl_ports(ctl_settings): # need to test this
    wallIPs = ctl_settings.wallIPs
    port = ctl_settings.portOscControl
    client_list = []
    for IP in wallIPs:
        wallIP = '--' + IP # if this doesn't work, use 'default=wallIP' # will host names work?
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", wallIP, help="The ip of the OSC"
                                                          "server")
        parser.add_argument("--port", type=int, default=port,
                            help="The port the OSC server is listening on")
        args = parser.parse_args()
        client = udp_client.SimpleUDPClient(args.ip, args.port)
        client_list.append(client)
    return client_list

def send_OscControl_data(client_list, freq_list): # need to test this
    # add amplitude scaling?
    for index, client in enumerate(client_list):
        freq = freq_list[index]
        amp = 0.8 # add coefficient or function here to generate EQ'd amp
        freq_message = '/sineFreq'
        amp_message = '/sineGain'
        client.send_message(freq_message, freq)
        client.send_message(amp_message, amp)