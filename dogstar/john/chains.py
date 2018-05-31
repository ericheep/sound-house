from random import randint, choice
from fractions import Fraction

# 0=left, 1=straight, 2=right
#   2       3       5       7       11      13
#   2       1.5     1.25    1.75    1.375   1.625
primes = [2, 1.5, 1.25, 1.75, 1.375, 1.625]


# initialize
freqs = [0, 0, 0, 0, 0, 0, 0, 0]
fundamental = 100

# quaternary chain functions
def is_even(integer):
    if integer % 2 == 0:
        is_even = True
    else:
        is_even = False
    return is_even

def make_quaternary_chain(chain_length): # input 8
    # need a chain of 8 for 9 pitches
    chain = [randint(0, 3)] # start with intial number 0 - 3
    for index, number in enumerate(range(chain_length - 1)):
        last_num = chain[index]
        options = [last_num]
        # if last_num is even, next_num must be odd or the same
        # if last_num is odd, next_num must be even or the same
        if is_even(last_num):
            options.append(1)
            options.append(3)
        else:
            options.append(0)
            options.append(2)
        next_num = choice(options)
        chain.append(next_num)
    return chain


# converting to freqency functions

def convert_to_freqs(chain, two_primes): # two primes is a list with 2 values
    # chain is 8 integers, converting to 9 frequencies
    initial = 100
    freqs = [initial]
    up_y = two_primes[0] # 1
    down_y = 1 / two_primes[0] # 3
    up_x = two_primes[1] # 0
    down_x = 1 / two_primes[1] # 2

    # get values in Hz
    for index, number in enumerate(chain):
        if number == 0:
            # up_x
            new_freq = freqs[index] * up_x
            freqs.append(new_freq)

        if number == 1:
            # up_y
            new_freq = freqs[index] * up_y
            freqs.append(new_freq)

        if number == 2:
            # down_x
            new_freq = freqs[index] * down_x
            freqs.append(new_freq)

        if number == 3:
            # down_y
            new_freq = freqs[index] * down_y
            freqs.append(new_freq)

    #print(freqs)
    # now normalize
    normalized = normalize_data(freqs)
    #print(normalized)
    # now put in right range
    scaled = scale_freqs(normalized)
    #print(scaled)
    return scaled

def normalize_data(data_list):
    #minimum = min(data_list)
    maximum = max(data_list)
    #print(minimum, maximum)
    new_list = []
    for i in data_list:
        scaled_datum = i / maximum
        new_list.append(scaled_datum)
    return new_list

def scale_freqs(normalized_data):
    # data all between 0 and 1
    # returns freqs in Hz between 100 and ___
    scale_factor = 4096 # power of 2
    new_list = []
    for i in normalized_data:
        scaled_datum = i * scale_factor
        new_list.append(scaled_datum)
    return new_list

#######
"""
1 <-- 2 <-- 3 <-- 4 --> 5 --> 6 --> 7 --> 8
"""

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
    for direction in chain[2::-1]: # get first three values
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

"""

def make_ternary_chain(chain_length):
    chain = []
    for number in range(chain_length):
        chain.append(randint(0, 2))
    return chain


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
"""