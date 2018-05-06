"""
oscDistance.py
Eric Heep

Waits for an OSC message from a host, then sends back a distance measurement to the host
"""
# standard imports
import socket
import argparse
import random
import time
from datetime import datetime, timedelta

# pi import
import RPi.GPIO as GPIO

# osc imports
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client

# osc vars
piWall = "/w"
hostIp = "192.168.0.7"
piPort = 5000
hostPort = 12345

# ultrasonic stuff
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
time.sleep(2)

# initial readout, probably not necessary
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

# this IP is set to send out
client = udp_client.UDPClient(hostIp, hostPort)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
        return IP

piIp = get_ip()

def getReading():
    """Gets a reading from the attached Ultrasonic sensor.
    """

    # does a ping or something
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    break_loop = False
    timeout = datetime.now() + timedelta(seconds=1)

    pulse_end = 0

    # finds the time measurements?
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
        # if timeout > datetime.now():
        #    break;

    timeout = datetime.now() + timedelta(seconds=1)
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
        # if timeout > datetime.now():
        #     break;

    # some calculations to convert to centimeters
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

def send(self):
    # we send the Pi's IP address as the OSC address
    # so the host computer knows which Pi sent a message
    packet = osc_message_builder.OscMessageBuilder(address=piWall)

    # adds whichPi to the OSC message
    hostname = socket.gethostname()

    # print(hostname)

    packet.add_arg(hostname, arg_type='s')

    # adds distance reading to the OSC message
    packet.add_arg(getReading(), arg_type='f')

    # completes the OSC message
    packet = packet.build()

    # sends distance back to the host
    client.send(packet)


if __name__ == "__main__":
    # sets up arguments for the dispatcher
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default=piIp, help="The ip to listen to")
    parser.add_argument("--port",
                        type=int, default=piPort, help="The port to listen on")
    args = parser.parse_args()

    # the thread that listens for the OSC messages
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/w", send)

    # the server we're listening on
    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)

    print("Serving on {}".format(server.server_address))

    # here we go!
    server.serve_forever()
