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

def convert_chain_to_freqs(chain, settings): # check this!
    center_freq = settings.centerFreq
    interval = settings.interval
    u_interval = settings.u_interval
    walls1234 = freqs_going_down(chain, interval, u_interval, center_freq)
    walls5678 = freqs_going_up(chain, interval, u_interval, center_freq)
    walls = walls1234 + walls5678
    return walls
