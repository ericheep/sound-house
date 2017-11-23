import argparse
from pythonosc import udp_client, osc_message_builder
import other_functions as of
from time import sleep
from random import randrange

def initialize_OscControl_ports(ctl_settings): # need to test this
    wallIPs = ctl_settings.wallIPs
    port = ctl_settings.portOscControl
    client_list = []
    for IP in wallIPs:
        #wallIP = '--' + IP # if this doesn't work, use 'default=wallIP' # will host names work?
        wallIP = IP
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default=wallIP, help="The ip of the OSC"
                                                          "server")
        parser.add_argument("--port", type=int, default=port,
                            help="The port the OSC server is listening on")
        args = parser.parse_args()
        client = udp_client.SimpleUDPClient(args.ip, args.port)
        client_list.append(client)
    ctl_settings.wallOsc_clients = client_list

def send_OscControl_data(ctl_settings, switch, freq_list=None): # need to test this
    # add amplitude scaling?
    freq_message = "/sineFreq"
    amp_message = "/sineGain"
    print(switch)
    #if switch == 'on':
    #    amp = 0.2 # add coefficient or function here to generate EQ'd amp
    #else:
    #    amp = 0
    for index, client in enumerate(ctl_settings.wallOsc_clients):
        if switch == 'on':
            freq = freq_list[index]
            client.send_message(freq_message, freq)
            client.send_message(amp_message, 0.2)
        else:
            client.send_message(amp_message, 0)

        #client.send_message(amp_message, amp)

def send_ternary_chain(ctl_settings, ternary_chain):
    """
    Sends freqs out to walls from ternary chain
    """
    freqs = of.convert_chain_to_freqs(ternary_chain, ctl_settings)
    send_OscControl_data(ctl_settings, 'on', freqs)
    print(freqs)

def send_OscControl_off(ctl_settings):
    freqs = [0, 0, 0, 0, 0, 0, 0, 0]        # debug this!
    send_OscControl_data(ctl_settings, 'off')

def send_brickplay(ctl_settings):
    wall_index = ctl_settings.count
    sample = str(randrange(1, 17))
    msg = '/brickPlay'
    if ctl_settings.networkOn:
        ctl_settings.wallOscClients[wall_index].send_message(msg, sample) # need to test this
    else:
        print(wall_index, msg, sample)