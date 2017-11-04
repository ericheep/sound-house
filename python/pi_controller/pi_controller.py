import sys, pygame, pygame.midi
import midi_functions as mf
import other_functions as of
import network_functions as nf
import ctl_functions as control
from settings import Settings
from slider import Slider
from wall_panel import Panel

ctl_settings = Settings()

sinOscWalls = nf.initialize_OscControl_ports(ctl_settings)

pygame.init()
pygame.midi.init()
screen = pygame.display.set_mode(
    (ctl_settings.screen_width, ctl_settings.screen_height))
pygame.display.set_caption("Sound House Pi Controller")

ternary_chain = [0, 0, 0, 0, 0, 0, 0]

# Make wall panel (1-8)
panel1 = Panel(ctl_settings, screen, 0)
panel2 = Panel(ctl_settings, screen, 1)
panel3 = Panel(ctl_settings, screen, 2)
panel4 = Panel(ctl_settings, screen, 3)
panel5 = Panel(ctl_settings, screen, 4)
panel6 = Panel(ctl_settings, screen, 5)
panel7 = Panel(ctl_settings, screen, 6)
panel8 = Panel(ctl_settings, screen, 7)

panels = [panel1, panel2, panel3, panel4, panel5, panel6, panel7, panel8]

midi_input = 0#pygame.midi.Input(0)


# Check midi devices
mf.check_midi_devices()

while True:

    mouse_x, mouse_y = pygame.mouse.get_pos()

    control.check_events(ctl_settings, screen, panels, midi_input,
                         ternary_chain, mouse_x, mouse_y)



        # add logic here for mode selection (flag for ternary wall mode, etc.)
        # and then logic for changes

    # update screen
    control.update_screen(ctl_settings, screen, panels, mouse_y)