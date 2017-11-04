import sys, pygame, pygame.midi

def check_slider(slider, mouse_x, mouse_y):
    knob_clicked = slider.rect.collidepoint(mouse_x, mouse_y)
    if knob_clicked:
        slider.k_moving = True

def check_events(ctl_settings, screen, panels, midi_input,
                 ternary_chain, mouse_x, mouse_y):
    # factor all this shit out
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Goodbye')
            #midi_input.close()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                print('Goodbye')
                #midi_input.close()
                sys.exit()
            elif event.key == pygame.K_1:
                ctl_settings.panel = 0
            elif event.key == pygame.K_2:
                ctl_settings.panel = 1
            elif event.key == pygame.K_3:
                ctl_settings.panel = 2
            elif event.key == pygame.K_4:
                ctl_settings.panel = 3
            elif event.key == pygame.K_5:
                ctl_settings.panel = 4
            elif event.key == pygame.K_6:
                ctl_settings.panel = 5
            elif event.key == pygame.K_7:
                ctl_settings.panel = 6
            elif event.key == pygame.K_8:
                ctl_settings.panel = 7


        # Mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for panel in panels:
                for slider in panel.sliders:
                    check_slider(slider, mouse_x, mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            for panel in panels:
                for slider in panel.sliders:
                    slider.k_moving = False

"""
    if midi_input.poll():
        ctl, val = mf.get_ctl_and_value(midi_input)
        #print(ctl)

        if ctl_settings.ternaryWallMode:
            if ctl < 7:
                mf.midi_to_ternary(ternary_chain, ctl, val)
            if ctl == 41 and val == 127:
                print(ternary_chain)
                freqs = of.convert_chain_to_freqs(ternary_chain, ctl_settings)
                print(freqs)
                # add call to function to convert to freq and send to walls
"""

def update_screen(ctl_settings, screen, panels, mouse_y):

    screen.fill(ctl_settings.bg_color)

    panels[ctl_settings.panel].update(mouse_y)
#    for panel in panels:
#        panel.update(mouse_y)

    pygame.display.flip()