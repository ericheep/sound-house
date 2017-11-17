from math import sqrt

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

def find_distance_old(wall_num):
    #position vals will be in dictionary, function will receive key to perform calculation, and normalize 0-1
    point_1 = [(positions[wall_num][0] / max_distance),
               ((positions[wall_num][1] + 20) / max_distance)]
    mic_point = [(positions["mic"][0] / max_distance),
                 (positions["mic"][1] / max_distance)]
    distances[wall_num] = round(((((point_1[0] - mic_point[0]) ** 2) +
                                  ((point_1[1] - mic_point[1]) ** 2)) ** 0.5), 2)
    print("Distance for Wall #" + str(wall_num) + ": " + str(distances[wall_num]))
    client.send_message("/wall" + str(wall_num), distances[wall_num])

def find_distance(obj1, obj2, panel=None):
    # finds the distance in pixels between two objects, then normalizes (0-1)
    x1, y1 = obj1.rect.center
    x2, y2 = obj2.rect.center

    x_diff = x2 - x1
    y_diff = y2 - y1

    distance = sqrt(x_diff**2 + y_diff**2)

    if panel:
        height = panel.height - ((obj1.height / 2) + (obj2.height / 2))
        width = panel.width - ((obj1.width / 2) + (obj2.width / 2))
        max_distance = sqrt(height**2 + width**2)
        normalized = distance / max_distance
        return normalized

    else:
        return distance
