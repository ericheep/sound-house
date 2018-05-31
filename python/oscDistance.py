"""
oscDistance.py
Eric Heep

Waits for an OSC message from a host, then sends back a distance measurement to the host.
"""

# standard imports
import socket, argparse, random, time
from datetime import datetime, timedelta

# pi import
import RPi.GPIO as GPIO

# osc imports
from pythonosc import dispatcher, osc_server, osc_message_builder, udp_client

TRIG = 23
ECHO = 24


def ultrasonic_init():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(2)


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


def get_reading():
    # does a ping or something
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    break_loop = False
    timeout = datetime.now() + timedelta(seconds=1)

    pulse_end = 0
    pulse_start = 0

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


def send(self, junk):
    packet = osc_message_builder.OscMessageBuilder(address=piWall)

    # adds whichPi to the OSC message
    hostname = socket.gethostname()

    # we send the Pi's IP address as the OSC address
    # so the host computer knows which Pi sent a message
    packet.add_arg(hostname, arg_type='s')

    # adds distance reading to the OSC message
    packet.add_arg(get_reading(), arg_type='f')

    # completes the OSC message
    packet = packet.build()

    # sends distance back to the host
    client.send(packet)


if __name__ == "__main__":
    # osc vars
    piWall = "/w"
    hostIp = "192.168.0.7"
    piPort = 5000
    hostPort = 12345

    piIp = get_ip()
    ultrasonic_init()

    # sets up arguments for the dispatcher
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostIp",
                        type=str, default=hostIp, help="The IP address to send back to")
    parser.add_argument("--hostPort",
                        type=int, default=hostPort, help="The port to send back to")
    args = parser.parse_args()

    # this IP is set to send out
    client = udp_client.UDPClient(args.hostIp, args.hostPort)

    # the thread that listens for the OSC messages
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map(piWall, send)

    # the server we're listening on
    server = osc_server.ThreadingOSCUDPServer(
        (piIp, piPort), dispatcher)

    print("Serving on " + piIp + " (" + socket.gethostname() + ")" +  " on port " + str(piPort))
    print("Sending back to " + args.hostIp + " to port " + str(args.hostPort))

    # here we go!
    server.serve_forever()
