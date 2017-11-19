"""
functions for MIDI input and processing for Sound House pi controller
"""
import pygame.midi

def check_midi_devices():
    for device in range(0, pygame.midi.get_count()):
        print(pygame.midi.get_device_info(device))


def midi_to_ternary(ctl_settings, index, integer):
    chain_list = ctl_settings.ternary_chain
    if integer < 10:
        chain_list[index] = 0
    elif integer > 116:
        chain_list[index] = 2
    else:
        chain_list[index] = 1
    if ctl_settings.ternary_chain != chain_list:
        ctl_settings.ternary_chain = chain_list


def update_ternary_controller(ctl_settings, ternary_panel):
    # take ternary chain and update digital controller---how to streamline this so it doesn't lag. update only when?
    for index, column in enumerate(ternary_panel.controller.column_list):
        button_index = ctl_settings.ternary_chain[index] # get the index for the right button
        button = column.column[button_index]
        if button.on == False:
            button.update()

            none_on = True
            for other_button in column.column:
                if other_button != button and other_button.on == True:
                    none_on = False
                    other_button.update()
            if none_on:
                button.update()
            column.update()



def get_ctl_and_value(device_name):
    # returns control number and value for midi events
    midi_event = device_name.read(10) # argument=number of events to read
    ctl = midi_event[0][0][1]
    val = midi_event[0][0][2]
    return ctl, val