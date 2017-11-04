"""
1 --> 2 --> 3 --> 4 --> 5 --> 6 --> 7 --> 8
"""
from fractions import Fraction
import argparse
from pythonosc import udp_client, osc_message_builder
from random import randint

PORT = 7400

STARTING_FREQ = 200 # Figure out how to scale correctly 0 - 1???

def get_user_chain():
    user_entry = input("Enter 7 digit ternary sequence (no spaces), 'return' "
                       "for random sequence: ")
    if user_entry:
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
    else:
        chain = random_chain()
    print(chain)
    return chain

def random_chain():
    chain = [randint(0, 2) for num in range(7)]
    return chain

def get_freqs(chain, interval1, u_interval1, interval2, u_interval2,
              starting_freq):
    # Returns freqs for walls 1 - 8 (0 = L from direction, 1 = straight, 2 = R
    wall_freqs = [starting_freq]
    current_freq = starting_freq
    orientation = 'up'
    for direction in chain:

        # Determine variables
        if orientation == 'up':
            straight = interval1
            left = u_interval2
            right = interval2
        elif orientation == 'down':
            straight = u_interval1
            left = interval2
            right = u_interval2
        elif orientation == 'left':
            straight = u_interval2
            left = u_interval1
            right = interval1
        elif orientation == 'right':
            straight = interval2
            left = interval1
            right = u_interval1

        # Compute frequencies
        if direction == 0:
            current_freq *= float(left)
            if orientation == 'up':
                orientation = 'left'
            elif orientation == 'down':
                orientation = 'right'
            elif orientation == 'left':
                orientation = 'down'
            elif orientation == 'right':
                orientation = 'up'
        elif direction == 1:
            current_freq *= float(straight)
        elif direction == 2:
            current_freq *= float(right)
            if orientation == 'up':
                orientation = 'right'
            elif orientation == 'down':
                orientation = 'left'
            elif orientation == 'left':
                orientation = 'up'
            elif orientation == 'right':
                orientation = 'down'
        wall_freqs.append(current_freq)

    return wall_freqs

def get_interval(num):
    user_interval = input("Axis {0} ratio (x/y): ".format(num))
    if user_interval:
        try:
            interval = Fraction(user_interval)
            u_interval = 1 / interval
        except ValueError:
            print("Invalid entry.")
            get_interval(num)
        return interval, u_interval
    else:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=PORT,
        help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)

first_pass = True
while True:
    if first_pass:
        try:
            interval1, u_interval1 = get_interval(1)
        except TypeError:
            print("Please make an entry.")
            continue
        try:
            interval2, u_interval2 = get_interval(2)
        except TypeError:
            print("Please make an entry.")
            continue
    chain = get_user_chain()
    wall_freqs = get_freqs(chain, interval1, u_interval1, interval2,
                               u_interval2, STARTING_FREQ)
    print(wall_freqs)
    client.send_message("/chain", wall_freqs)
    first_pass = False
    loop = input("'q' to quit. 'return' to enter another chain. 'c' to change "
                 "intervals: ")
    if loop == 'q':
        break
    elif loop == 'c':
        first_pass = True