# john eagle

import argparse
from pythonosc import udp_client, osc_message_builder, dispatcher, osc_server
import threading
#import other_functions as of
from time import sleep
from random import randrange, choice

import pygame

import math


#### new functions from may 2018

def make_client(IP, port):
    # creates osc client
    # set IP and port
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=IP, help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=port,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()
    # make client
    client = udp_client.SimpleUDPClient(args.ip, args.port)
    return client

def send(client, msg1, msg2=0):
    # sends message to osc client
    # msg2 is a nul value just to make send work
    client.send_message(msg1, msg2)
    #print("sending...")

def send_reading(client, adr, mode):#self, junk):
    # we send the Pi's IP address as the OSC address
    # so the host computer knows which Pi sent a message
    packet = osc_message_builder.OscMessageBuilder(address=adr)

    # adds whichPi to the OSC message
    #hostname = socket.gethostname()

    # print(hostname)
    # for dev mode only
    if mode == 'local':
        pi = choice(["pione", "pitwo", "pithree", "pifour", "pifive", "pisix",
                     "piseven", "pieight"])
        val = randrange(0, 100)
        hostname = pi

    packet.add_arg(hostname, arg_type='s')

    # adds distance reading to the OSC message
    packet.add_arg(val, arg_type='f')

    # completes the OSC message
    packet = packet.build()

    # sends distance back to the host
    client.send(packet)

    #print("sending:", adr, hostname, val)

def parse_sensors(address, hostname, val):
    print("pi: ", hostname, "val: ", val)

def make_server(IP, port, address):
    # creates server on thread for receiving osc messages
    # set IP and port to listen on
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=IP, help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=port,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    # the thread that listens for the OSC messages
    dispatcherX = dispatcher.Dispatcher()
    dispatcherX.map(address, parse_sensors)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port),
                                              dispatcherX)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    print("Serving on {}".format(server.server_address))

    return server



#### old functions




 # need to test this with walls running

def initialize_sensorReceiver_port(ctl_settings):

    wallIPs = ctl_settings.wallIPs
    port = ctl_settings.portGetSensorData
    client_list = []
    for IP in wallIPs:
        wallIP = IP
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default=wallIP, help="The ip of the OSC"
                                                         "server")
        parser.add_argument("--port", type=int, default=port,
                            help="The port the OSC server is listening on")
        args = parser.parse_args()
        client = udp_client.SimpleUDPClient(args.ip, args.port)
        client_list.append(client)
    ctl_settings.wallSensor_clients = client_list

    #ip = ctl_settings.localIP
    #port = ctl_settings.portGetSensorData
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--ip", default=ip, help="The ip to listen on")
    #parser.add_argument("--port", type=int, default=port,
    #                    help="The port to listen on")
    #args = parser.parse_args()
    
    #receives two messages and a value (/w pione 216.3)
    address = "/w"

    # the thread that listens for the OSC messages
    dispatcherX = dispatcher.Dispatcher()
    dispatcherX.map(address, print)#ctl_settings.update_wall_sensors)

    ctl_settings.server = osc_server.ThreadingOSCUDPServer((args.ip, args.port),
                                                         dispatcherX)
    ctl_settings.server_thread = threading.Thread(
        target=ctl_settings.server.serve_forever)
    ctl_settings.server_thread.start()

    print("Serving on {}".format(ctl_settings.server.server_address))

def stopServer(ctl_settings):
    if ctl_settings.server:
        ctl_settings.server.shutdown()

def initialize_audioControl_port(ctl_settings): # sends to sender.ck
    IP = ctl_settings.localIP
    port = ctl_settings.portFeedbackControl # 7400
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=IP, help="The ip of the OSC"
                                                 "server")
    parser.add_argument("--port", type=int, default=port,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()
    ctl_settings.senderCK_client = udp_client.SimpleUDPClient(args.ip, args.port)

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

def initialize_sensorPing_ports(ctl_settings):
    wallIPs = ctl_settings.wallIPs
    port = ctl_settings.portPingSensors
    client_list = []
    for IP in wallIPs:
        wallIP = IP
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default=wallIP, help="The ip of the OSC"
                                                         "server")
        parser.add_argument("--port", type=int, default=port,
                            help="The port the OSC server is listening on")
        args = parser.parse_args()
        client = udp_client.SimpleUDPClient(args.ip, args.port)
        client_list.append(client)
    ctl_settings.wallSensor_clients = client_list

def initialize_video_port(ctl_settings):
    IP = ctl_settings.videoIP
    port = ctl_settings.portVideo
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=IP, help="The ip of the OSC"
                                                     "server")
    parser.add_argument("--port", type=int, default=port,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()
    ctl_settings.video_client = udp_client.SimpleUDPClient(args.ip, args.port)

def send_audioControl_data(ctl_settings, msg, val):
    # sends to sender.ck
    if ctl_settings.networkOn:
        ctl_settings.senderCK_client.send_message(msg, val)
    else:
        print(msg, val)

def send_OscControl_data(ctl_settings, freq_list=None): # need to test this
    # add amplitude scaling?
    freq_message = "/sineFreq"
    amp_message = "/sineGain"

    for index, client in enumerate(ctl_settings.wallOsc_clients):
        amp = ctl_settings.wall_amps[index]
        # add coeffecient or function here to EQ amp val
        if switch == 'on':
            freq = freq_list[index]
            amp = ctl_settings.wall_amps[index]
            client.send_message(freq_message, freq)
            client.send_message(amp_message, amp)
        else:
            client.send_message(amp_message, 0)

def send_ternary_chain(ctl_settings, ternary_chain):
    """
    Sends freqs out to walls from ternary chain
    """
    freqs = of.convert_chain_to_freqs(ternary_chain, ctl_settings)
    send_OscControl_data(ctl_settings, freqs)
    print(freqs)

def send_OscControl_off(ctl_settings):
    freqs = [0, 0, 0, 0, 0, 0, 0, 0]        # debug this!
    send_OscControl_data(ctl_settings, 'off')

def ping_sensors(ctl_settings):
    msg = "/w"
    if ctl_settings.networkOn:
        for index, client in enumerate(ctl_settings.wallSensor_clients):
            client.send_message(msg, '') # is a val needed here?
    else:
        print(msg)

def send_brickplay(ctl_settings):
    wall_index = ctl_settings.count
    sample = str(randrange(1, 17))
    msg = '/brickPlay'
    if ctl_settings.networkOn:
        ctl_settings.wallOscClients[wall_index].send_message(msg, sample) # need to test this
    else:
        print(wall_index, msg, sample)

def sendVideoTrigger(ctl_settings, channel, val): # placeholder function for testing video OSC messages
    msg = '/video/' + str(channel) # placeholders
    if ctl_settings.networkOn:
        ctl_settings.video_client.send_message(msg, val)
    else:
        print(msg, val)
