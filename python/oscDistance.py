"""
oscDistance.py
Eric Heep

Waits for an OSC message from a host, then sends back a distance measurement to the host
"""
# standard imports
import argparse
import random
import time

# pi import
import RPi.GPIO as GPIO

# osc imports
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client

# osc vars
piIp = "192.168.1.11"
hostIp = "192.168.1.100"
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


def getReading():
    """Gets a reading from the attached Ultrasonic sensor.
    """

    # does a ping or something
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # finds the time measurements?
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    # some calculations to convert to centimeters
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

def send(self, wait):
    # we send the Pi's IP address as the OSC address
    # so the host computer knows which Pi sent a message
    packet = osc_message_builder.OscMessageBuilder(address='/' + piIp)
    # option to wait a bit before reading
    if wait > 0:
        time.sleep(wait)
    # adds distance reading to the OSC message
    packet.add_arg(getReading(), arg_type='f')
    # complets the OSC message
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
    dispatcher.map("/wait", send)

    # the server we're listening on
    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)

    print("Serving on {}".format(server.server_address))

    # here we go!
    server.serve_forever()