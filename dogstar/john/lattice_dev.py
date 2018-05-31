"""
John Eagle
"""

import argparse
from pythonosc import udp_client, osc_message_builder, dispatcher, osc_server
import threading
import pygame, sys
import network_functions as nf
import chains
from time import sleep


# TO DO: add ability to change to next chain by standing in front of 1 * 8 for x seconds
# is there another method that could work for changing interval? or just have x number of times for each prime?

###
def parse_sensors(address, hostname, val):
    #print("pi: ", hostname, "val: ", val)
    if hostname in wall_names:
        wall_index = wall_names.index(hostname)
        wall_vals[wall_index] = val
        #print(wall_vals)

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

def send_OscControl_data(freq_list, amp_list):
    # send sine freqs and amplitudes
    freq_message = "/sineFreq"
    amp_message = "/sineGain"

    for index, client in enumerate(wall_oscs):
        amp = amp_list[index]
        freq = freq_list[index]

        # amplitude envelope
        if freq < 200:
            amp *= 2.5
            #print('200', freq)
        elif freq < 300:
            amp *= 2.1
            #print('300', freq)
        elif freq < 400:
            amp *= 2
            #print('400', freq)
        elif freq < 700:
            amp *= 1.5
            #print('700', freq)
        elif freq < 1000:
            amp *= 1.25
            #print('1k', freq)
        elif freq < 2000:
            amp *= 0.5
            #print('2k', freq)
        elif freq < 3000:
            amp *= 0.5
            #print('3k', freq)
        elif freq < 4000:
            amp *= 0.6
            #print('4k', freq)
        else:
            pass
            #print('4k+', freq)

        # now send everything
        client.send_message(freq_message, freq)
        client.send_message(amp_message, amp)

        # uncomment these two lines to arpeggiate chord
        #sleep(1)
        #client.send_message(amp_message, 0)

def send_local_osc(client, freq, amp):
    freq_message = "/sineFreq"
    amp_message = "/sineGain"
    client.send_message(freq_message, freq)
    client.send_message(amp_message, amp)

def check_for_threshold(wall_vals, wall_amps):
    # checks sensor data to see if distance threshold has been passed
    threshold = 30 # cm
    min_amp = 0.05
    max_amp = 0.7

    for index, val in enumerate(wall_vals):
        if val < threshold:
            wall_amps[index] = max_amp
            send_OscControl_data(wall_freqs, wall_amps)
            print(index + 1, ' on')
        else:
            wall_amps[index] = min_amp
    return wall_amps

def send_test_values():
    client = int(input("wall num: ")) - 1
    freq = float(input("frequency: "))
    amp = float(input("amp: "))
    wall_oscs[client].send_message("/sineFreq", freq)
    wall_oscs[client].send_message("/sineGain", amp)

def get_pair(user_list, index_1):
    first_pair = user_list[index_1:index_1 + 2]
    return first_pair

def check_events(local_freq, wall_freqs, prime_pair, prime_progression):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutdown()
        elif event.type == pygame.KEYDOWN:
            local_freq, wall_freqs, prime_pair, prime_progression = check_keydown_events(event, local_freq, wall_freqs, prime_pair, prime_progression)

    return local_freq, wall_freqs, prime_pair, prime_progression

def check_keydown_events(event, local_freq, wall_freqs, prime_pair, prime_progression):
    if event.key == pygame.K_q:
        shutdown()
    # key triggers
    if event.key == pygame.K_RETURN:
        # get new chain
        print('return')
        local_freq, wall_freqs = make_chain()
    if event.key == pygame.K_LEFT:
        prime_progression -= 1
        if prime_progression < 0:
            prime_progression = 0
        prime_pair = get_pair(primes, prime_progression)
        print(prime_pair)
    elif event.key == pygame.K_RIGHT:
        prime_progression += 1
        if prime_progression > (len(primes) - 2):
            prime_progression = len(primes) - 2
        prime_pair = get_pair(primes, prime_progression)
        print(prime_pair)

    # add events for changing primes

    return local_freq, wall_freqs, prime_pair, prime_progression

def shutdown():
    # shutdown procedures
    print('Goodbye')
    local_server.shutdown()
    sys.exit()


def update_screen(screen):
    # draw screen
    screen.fill((0, 0, 0))
    pygame.display.flip()

###

local_IP = "127.0.0.1"
john_MBP = "192.168.0.7"

# select runtime mode or dev mode
ui = input("1. Run Program (networked) 2. Dev. Mode (local): ")

if ui == "1":
    IP = john_MBP
    sending = "pis"
elif ui == "2":
    IP = local_IP
    sending = "local"

#prime_1 = float(input('prime 1: '))
#prime_2 = float(input('prime 2: '))
#primes = [prime_1, prime_2]
primes = [2, 1.5, 1.25, 1.75, 1.375, 1.625] # len = 6, 2nd to last index = 4
prime_progression = 0
prime_pair = get_pair(primes, prime_progression)


# pi hostnames
wall_IPs = ['pione.local', 'pitwo.local', 'pithree.local', 'pifour.local',
            'pifive.local', 'pisix.local', 'piseven.local', 'pieight.local']

# ports for sending and receiving
ping_port = 5000
rec_port = 12345
osc_port = 10001
local_sine = 10002
local_osc = nf.make_client(local_IP, local_sine)


# create one local client or 8 pi clients
wall_clients = []
wall_oscs = []
if sending == "pis":
    # for pinging sensors
    for wall_IP in wall_IPs:
        client = nf.make_client(wall_IP, ping_port)
        wall_clients.append(client)
    # for sending sine tone data
    for wall_IP in wall_IPs:
        client = nf.make_client(wall_IP, osc_port)
        wall_oscs.append(client)

elif sending == "local":
    client = nf.make_client(IP, rec_port)
    wall_clients.append(client)

local_server = make_server(IP, rec_port, "/w")

wall_names = ["pione", "pitwo", "pithree", "pifour", "pifive", "pisix",
              "piseven", "pieight"]
wall_vals = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
wall_amps = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]

#chain = chains.make_quaternary_chain(8)
#freqs = chains.convert_to_freqs(chain, primes)
#local_freq = freqs[0]
#wall_freqs = freqs[1:]

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Lattice Chain Pi Controller")

def make_chain():
    searching = True
    while searching:
        chain = chains.make_quaternary_chain(8)
        freqs = chains.convert_to_freqs(chain, prime_pair)
        if min(freqs) < 100.0:
            # too low start again
            continue
        elif min(freqs) > 400:
            # too high start again
            continue
        else:
            searching = False
            local_freq = freqs[0]
            # print(local_freq)
            wall_freqs = freqs[1:]
            print("primes:", prime_pair, "sines: ", wall_freqs)

    return local_freq, wall_freqs

local_freq, wall_freqs = make_chain()


#searching = True

# main program loop
while True:
    # ping
    for client in wall_clients:
        if sending == "pis":
            nf.send(client, "/w")
        elif sending == "local":
            # generate random reading
            nf.send_reading(client, "/w", sending) #simulation use nf.send for real
    # check for trigger
    wall_amps = check_for_threshold(wall_vals, wall_amps)

    # send local freq and amp
    send_local_osc(local_osc, local_freq, 0.9)
    # send frequency and amp to walls
    print(wall_freqs)
    send_OscControl_data(wall_freqs, wall_amps)

    local_freq, wall_freqs, prime_pair, prime_progression = \
        check_events(local_freq, wall_freqs, prime_pair, prime_progression)
    update_screen(screen)


    # testing
    #send_test_values()

    # how many chains for each prime set?

    sleep(0.1)


# make max patch or chuck script to accept first freq value and plug into speaker