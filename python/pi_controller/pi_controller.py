"""
John Eagle
pi_controller.py

Main program for pi_controller system

uses pygame 1.9.4.dev0 and custom modules:

button.py
ctl_functions.py
drawing_functions.py
lattice_chains.py # ????
map_objects.py
midi_functions.py
network_functions.py
other_functions.py
panel.py
scale_function.py
settings.py
slider.py
ternary_control.py
wall_panel.py ?????
"""

import sys, pygame, pygame.midi
import midi_functions as mf
import other_functions as of
import network_functions as nf
import ctl_functions as control
from settings import Settings
import panel

ctl_settings = Settings()


### Initialize program
# select runtime mode or dev mode
ui = input("1. Run Program (networked) 2. Dev. Mode (local): ")

if ui == "1":
    IP = ctl_settings.myIP #"192.168.0.7"
    ctl_settings.sending = "pis"
elif ui == "2":
    IP = ctl_settings.localIP #"127.0.0.1"
    ctl_settings.sending = "local"

# initialize port connections
nf.initialize_sensorPing_ports(ctl_settings)
nf.initialize_OscControl_ports(ctl_settings)

server = nf.make_server(ctl_settings, IP, ctl_settings.portGetSensorData, "/w")

#nf.initialize_audioControl_port(ctl_settings)
#nf.initialize_video_port(ctl_settings)

pygame.init()
pygame.midi.init()
screen = pygame.display.set_mode(
    (ctl_settings.screen_width, ctl_settings.screen_height))
pygame.display.set_caption("Sound House Pi Controller")

# Make clock
clock = pygame.time.Clock()

# Make wall panel (1-8)
panel1 = panel.WallPanel(ctl_settings, screen, 'Wall Controls', 0, 0)
panel2 = panel.WallPanel(ctl_settings, screen, 'Wall Controls', 0, 1)
panel3 = panel.WallPanel(ctl_settings, screen, 'Wall Controls', 0, 2)
panel4 = panel.WallPanel(ctl_settings, screen, 'Wall Controls', 0, 3)
panel5 = panel.WallPanel(ctl_settings, screen, 'Wall Controls', 0, 4)
panel6 = panel.WallPanel(ctl_settings, screen, 'Wall Controls', 0, 5)
panel7 = panel.WallPanel(ctl_settings, screen, 'Wall Controls', 0, 6)
panel8 = panel.WallPanel(ctl_settings, screen, 'Wall Controls', 0, 7)

wall_panels = [panel1, panel2, panel3, panel4, panel5, panel6, panel7, panel8]

automation_panel = panel.AutomationPanel(ctl_settings, screen, 'Automation', # Label?
                                         panel1.rect.bottom, height=90)

ternary_panel = panel.TernaryPanel(ctl_settings, screen, 'Sound Code',
                                   automation_panel.rect.bottom, height=120)

wall_map_panel = panel.WallMapPanel(wall_panels, ctl_settings, screen,
                                    'Wall Map', 0, height=400) # make responsive? or customizable?

playback_panel = panel.PlaybackPanel(ctl_settings, screen, 'Playback',
                                     ternary_panel.rect.bottom, height=170,
                                     fullsize=True)

panels = {
             'Wall Panels': wall_panels, 'Automation Panel': automation_panel,
             'Ternary Panel': ternary_panel, 'Wall Map': wall_map_panel,
             'Playback Panel': playback_panel
}

try:
    midi_input = pygame.midi.Input(0)
except:
    midi_input = 0
    print("No midi devices found.")

# Check midi devices
mf.check_midi_devices()

while True:
    clock.tick(60)
    # get cursor position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # check events
    control.check_events(ctl_settings, screen, panels, midi_input, mouse_x,
                         mouse_y)
    # update screen
    control.update_screen(ctl_settings, screen, panels, mouse_x, mouse_y)
