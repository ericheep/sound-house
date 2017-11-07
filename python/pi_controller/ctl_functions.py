import sys, pygame, pygame.midi

def check_slider(slider, mouse_x, mouse_y):
    knob_clicked = slider.rect.collidepoint(mouse_x, mouse_y)
    if knob_clicked:
        slider.k_moving = True

def check_button(button, ctl_settings, buttons, panels, mouse_x, mouse_y):
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        button.update()
        if button.title == 'Bandpass':
            if button.on == True: # is this best way to do this?
                bandpass_automation(panels)
            elif button.on == False:
                allpass_automation(panels)
        elif button.title == 'Mic':
            if button.on == True:
                mic_on_off_automation(panels, 100) # turn mic on
            elif button.on == False:
                mic_on_off_automation(panels, 0) # turn off
        elif button.title == 'Feedback':
            if button.on == True:
                feedback_default_automation(ctl_settings, panels)
                if buttons[1].on == False:
                    buttons[1].update() # Turn 'Mic' on
            elif button.on == False:
                all_off_automation(ctl_settings, panels)
                if buttons[1].on == True:
                    buttons[1].update() # Turn 'Mic' off


def check_events(ctl_settings, screen, panels, buttons, midi_input,
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
            # select wall panel with num entry
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
            for button in buttons:
                check_button(button, ctl_settings, buttons, panels, mouse_x,
                             mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            for panel in panels:
                for slider in panel.sliders:
                    slider.k_moving = False

def bandpass_automation(panels):
    print("bandpass automation") # not sure about the scaling here
    hp = 6.3
    lp = 9.7
    for panel in panels:
        panel.sliders[1].automate(hp)
        panel.sliders[2].automate(lp)
        hp += 12
        lp += 11

def allpass_automation(panels):
    print("bandpass automation")
    for panel in panels:
        panel.sliders[1].automate(0)
        panel.sliders[2].automate(100)

def mic_on_off_automation(panels, gain_val):
    print("Mic on/off")
    for panel in panels:
        panel.sliders[0].automate(gain_val)

def feedback_default_automation(ctl_settings, panels):
    print("Feedback Mode Default")
    for panel in panels:
        panel.sliders[0].automate(ctl_settings.mic)
        panel.sliders[1].automate(ctl_settings.hp)
        panel.sliders[2].automate(ctl_settings.lp)
        panel.sliders[3].automate(ctl_settings.res)
        panel.sliders[4].automate(ctl_settings.threshold)
        panel.sliders[5].automate(ctl_settings.packetLength)
        panel.sliders[6].automate(ctl_settings.delayLength)

def all_off_automation(ctl_settings, panels):
    print("All Off")
    for panel in panels:
        panel.sliders[0].automate(0)
        panel.sliders[1].automate(0)
        panel.sliders[2].automate(0)
        panel.sliders[3].automate(0)
        panel.sliders[4].automate(0)
        panel.sliders[5].automate(0)
        panel.sliders[6].automate(0)

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

def update_screen(ctl_settings, screen, panels, buttons, mouse_y):

    screen.fill(ctl_settings.bg_color)

    panels[ctl_settings.panel].update(mouse_y)

    for button in buttons:
        button.draw_button()

    pygame.display.flip()