"""
1 <-- 2 <-- 3 <-- 4 --> 5 --> 6 --> 7 --> 8
"""
from fractions import Fraction
import argparse
from pythonosc import udp_client, osc_message_builder

PORT = 7400

CENTER_FREQ = 440

interval = Fraction(7/4)    # 3/2 5/4 7/4
u_interval = 1 / interval

def get_user_chain():
    user_entry = input('Enter 7 digit ternary sequence (no spaces): ')
    chain = []
    for i in user_entry:
        try:
            i = int(i)
        except ValueError:
            print("Please enter only 0's, 1's, or 2's.")
            break
            get_user_chain()
        if i < 0 or i > 2:
            print("Please enter only 0's, 1's, or 2's.")
            break
            get_user_chain()
        else:
            chain.append(i)
    return chain

def freqs_going_down(chain, interval, u_interval, center_freq):
    # Walls 3, 2, 1 (from Wall 4) returns freqs [wall1, wall2, wall3, wall4]
    walls_1234 = []
    current_freq = center_freq
    walls_1234.insert(0, current_freq)
    for direction in chain[2::-1]:
        if direction == 2:
            current_freq = float(current_freq * u_interval)
        elif direction == 1:
            pass
        elif direction == 0:
            current_freq = float(current_freq * interval)
        walls_1234.insert(0, current_freq)
    return walls_1234

def freqs_going_up(chain, interval, u_interval, center_freq):
    # Walls 5, 6, 7, 8 (from Wall 4) returns freqs [wall5, wall6, wall7, wall8]
    walls_5678 = []
    current_freq = center_freq
    for direction in chain[3:]:
        if direction == 2:
            current_freq = float(current_freq * interval)
        elif direction == 1:
            pass
        elif direction == 0:
            current_freq = float(current_freq * u_interval)
        walls_5678.append(current_freq)
    return walls_5678

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=PORT,
        help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)

while True:
    get_interval = input("Interval ratio (x/y, 'q' to quit): ")
    if get_interval == 'q':
        break
    elif not get_interval:
        pass
    else:
        try:
            interval = Fraction(get_interval)
            u_interval = 1 / interval
        except ValueError:
            print("Invalid entry.")
            continue
    chain = get_user_chain()
    walls_1234 = freqs_going_down(chain, interval, u_interval, CENTER_FREQ)
    walls_5678 = freqs_going_up(chain, interval, u_interval, CENTER_FREQ)
    walls_12345678 = walls_1234 + walls_5678
    print(walls_12345678)
    client.send_message("/chain", walls_12345678)