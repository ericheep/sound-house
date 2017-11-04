"""
functions for MIDI input and processing for Sound House pi controller
"""
import pygame.midi

def check_midi_devices():
    for device in range(0, pygame.midi.get_count()):
        print(pygame.midi.get_device_info(device))


def midi_to_ternary(chain_list, index, integer):
    if integer < 10:
        chain_list[index] = 0
    elif integer < 117:
        chain_list[index] = 1
    else:
        chain_list[index] = 2

def get_ctl_and_value(device_name):
    # returns control number and value for midi events
    midi_event = device_name.read(1) # argument=number of events to read
    ctl = midi_event[0][0][1]
    val = midi_event[0][0][2]
    return ctl, val