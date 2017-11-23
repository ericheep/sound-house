import sys, pygame, pygame.midi
import network_functions as nf
import midi_functions as mf
import other_functions as of

def check_events(ctl_settings, screen, panels, midi_input, mouse_x, mouse_y):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Goodbye')
            if midi_input:
                midi_input.close()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ctl_settings, screen, panels,
                                 midi_input)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ctl_settings, screen, panels)

        # Mouse events --factor out!
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for panel in panels['Wall Panels']: # check wall panel clicks
                for slider in panel.sliders:
                    check_slider(slider, mouse_x, mouse_y)
            for button in panels['Automation Panel'].buttons: # check automation panel clicks
                check_button(button, screen, ctl_settings, panels, mouse_x,
                             mouse_y)
            for button in panels['Ternary Panel'].buttons: # check ternary code panel clicks
                check_button(button, screen, ctl_settings, panels, mouse_x,
                             mouse_y)
            for column in panels['Ternary Panel'].controller.column_list: # check ternary controller clicks
                for button in column.column:
                    check_button(button, screen, ctl_settings, panels, mouse_x,
                                 mouse_y, column, check_column=True)
            for button in panels['Playback Panel'].brick_buttons: # check sequencer buttons
                check_button(button, screen, ctl_settings, panels, mouse_x,
                             mouse_y)
            check_slider(panels['Playback Panel'].BPM, mouse_x, mouse_y) # check BPM slider

        elif event.type == pygame.MOUSEBUTTONUP:
            for panel in panels['Wall Panels']: # check wall panel click releases
                for slider in panel.sliders:
                    slider.k_moving = False
            if panels['Playback Panel'].BPM.k_moving:
                if ctl_settings.playbackMode:
                    # Updates timer
                    if panels['Playback Panel'].timer:
                        pygame.time.set_timer(ctl_settings.PB_EVENT,
                                              ctl_settings.bpm_ms)
                panels['Playback Panel'].BPM.k_moving = False

        # PB Events --factor out
        elif event.type == ctl_settings.PB_EVENT:
            if panels['Playback Panel'].buttons[ctl_settings.count - 1].on:
                panels['Playback Panel'].buttons[ctl_settings.count - 1].update() # turn off last button
            panels['Playback Panel'].buttons[ctl_settings.count].update() # turn on new button
            if panels['Playback Panel'].brick_buttons[ctl_settings.count].on: # trigger brick sound
                nf.send_brickplay(ctl_settings)
                #print(ctl_settings.count) # replace with function to randomly select brick sample and send osc message
            ctl_settings.count += 1
            if ctl_settings.count == 8:
                ctl_settings.count = 0

    # MIDI events
    if midi_input:
        check_MIDI(ctl_settings, screen, panels, midi_input)

def check_keydown_events(event, ctl_settings, screen, panels, midi_input):
    if event.key == pygame.K_q:
        print('Goodbye')
        if midi_input:
            midi_input.close()
        sys.exit()
    # select wall panel with num entry
    elif event.key == pygame.K_1:
        ctl_settings.wall_panel = 0
        panels['Wall Map'].switch_wall()
    elif event.key == pygame.K_2:
        ctl_settings.wall_panel = 1
        panels['Wall Map'].switch_wall()
    elif event.key == pygame.K_3:
        ctl_settings.wall_panel = 2
        panels['Wall Map'].switch_wall()
    elif event.key == pygame.K_4:
        ctl_settings.wall_panel = 3
        panels['Wall Map'].switch_wall()
    elif event.key == pygame.K_5:
        ctl_settings.wall_panel = 4
        panels['Wall Map'].switch_wall()
    elif event.key == pygame.K_6:
        ctl_settings.wall_panel = 5
        panels['Wall Map'].switch_wall()
    elif event.key == pygame.K_7:
        ctl_settings.wall_panel = 6
        panels['Wall Map'].switch_wall()
    elif event.key == pygame.K_8:
        ctl_settings.wall_panel = 7
        panels['Wall Map'].switch_wall()

    elif event.key == pygame.K_o and ctl_settings.networkOn:
        nf.send_OscControl_off(ctl_settings)  # add button for this

    if ctl_settings.mapping:
        # Arrow keys to control wall position
        if event.key == pygame.K_LEFT:
            panels['Wall Map'].walls[ctl_settings.wall_panel].moving_left = True
        if event.key == pygame.K_RIGHT:
            panels['Wall Map'].walls[ctl_settings.wall_panel].moving_right = True
        if event.key == pygame.K_UP:
            panels['Wall Map'].walls[ctl_settings.wall_panel].moving_up = True
        if event.key == pygame.K_DOWN:
            panels['Wall Map'].walls[ctl_settings.wall_panel].moving_down = True

        # Left shift slows down wall movement
        if event.key == pygame.K_LSHIFT:
            ctl_settings.wall_speed_factor = 0.25

        # 'r' rotates wall
        if event.key == pygame.K_r:
            panels['Wall Map'].walls[ctl_settings.wall_panel].rotate()

        # 'p' selects puppet --cycles 1 and 2
        if event.key == pygame.K_p:
            # get current active puppet
            on_puppet = ctl_settings.puppet
            if on_puppet == 0:
                off_puppet = 1
            else:
                off_puppet = 0
            # trigger both to switch
            panels['Wall Map'].puppets[on_puppet].onoff()
            panels['Wall Map'].puppets[off_puppet].onoff()
            # now update
            ctl_settings.puppet = off_puppet

        # w,a,s,d control puppet position
        # maybe make a mode selector for this?
        if event.key == pygame.K_a:
            panels['Wall Map'].puppets[ctl_settings.puppet].moving_left = True
        if event.key == pygame.K_d:
            panels['Wall Map'].puppets[ctl_settings.puppet].moving_right = True
        if event.key == pygame.K_w:
            panels['Wall Map'].puppets[ctl_settings.puppet].moving_up = True
        if event.key == pygame.K_s:
            panels['Wall Map'].puppets[ctl_settings.puppet].moving_down = True

    # start timer
    if ctl_settings.playbackMode:
        if event.key == pygame.K_SPACE:
            # Turns off timer if on
            if panels['Playback Panel'].timer:
                panels['Playback Panel'].timer = False
                pygame.time.set_timer(ctl_settings.PB_EVENT, 0)
            # Else turns timer on
            else:
                panels['Playback Panel'].timer = True
                pygame.time.set_timer(ctl_settings.PB_EVENT,
                                      ctl_settings.bpm_ms)

def check_keyup_events(event, ctl_settings, screen, panels):

    if ctl_settings.mapping:
        # Arrow keys to control wall position
        if event.key == pygame.K_LEFT:
            panels['Wall Map'].walls[ctl_settings.wall_panel].moving_left = False
        if event.key == pygame.K_RIGHT:
            panels['Wall Map'].walls[ctl_settings.wall_panel].moving_right = False
        if event.key == pygame.K_UP:
            panels['Wall Map'].walls[ctl_settings.wall_panel].moving_up = False
        if event.key == pygame.K_DOWN:
            panels['Wall Map'].walls[ctl_settings.wall_panel].moving_down = False

        # Returns wall speed to normal
        if event.key == pygame.K_LSHIFT:
            ctl_settings.wall_speed_factor = 1

        # w,a,s,d control puppet position
        if event.key == pygame.K_a:
            panels['Wall Map'].puppets[ctl_settings.puppet].moving_left = False
        if event.key == pygame.K_d:
            panels['Wall Map'].puppets[ctl_settings.puppet].moving_right = False
        if event.key == pygame.K_w:
            panels['Wall Map'].puppets[ctl_settings.puppet].moving_up = False
        if event.key == pygame.K_s:
            panels['Wall Map'].puppets[ctl_settings.puppet].moving_down = False

def check_MIDI(ctl_settings, screen, panels, midi_input):
    # event processing for MIDI controls
    if midi_input.poll():
        ctl, val = mf.get_ctl_and_value(midi_input)

        if ctl_settings.ternaryWallMode:
            if ctl < 7:
                mf.midi_to_ternary(ctl_settings, ctl, val)
                mf.update_ternary_controller(ctl_settings,
                                             panels['Ternary Panel'])  # how to streamline this so it doesn't lag. update only when?
            if ctl == 41 and val == 127:  # midi 'play' button
                button = panel['Ternary Panel'].buttons[0]
                button.update()
                send_code_automation(button, ctl_settings, screen,
                                     panels, mouse_y)


def check_slider(slider, mouse_x, mouse_y):
    knob_clicked = slider.rect.collidepoint(mouse_x, mouse_y)
    if knob_clicked:
        slider.k_moving = True

def check_button(button, screen, ctl_settings, panels, mouse_x, mouse_y,
                 column=None, check_column=False):
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:

        # check modes first, right now activating one mode doesn't turn others off--add this behavior later
        if button.title == 'TC MODE':
            button.update()
            if button.on == True:
                ctl_settings.ternaryWallMode = True
            elif button.on == False:
                ctl_settings.ternaryWallMode = False

        elif button.title == 'FB MODE':
            button.update()
            if button.on == True:
                ctl_settings.feedbackMode = True
                feedback_default_automation(ctl_settings, panels)
                if panels['Automation Panel'].buttons[5].on == False:
                    panels['Automation Panel'].buttons[5].update() # Turn 'Mic' on
            elif button.on == False:
                ctl_settings.feedbackMode = False
                all_off_automation(ctl_settings, panels)
                if panels['Automation Panel'].buttons[5].on == True:
                    panels['Automation Panel'].buttons[5].update() # Turn 'Mic' off

        elif button.title == 'PB MODE':
            button.update()
            if button.on == True:
                ctl_settings.playbackMode = True
            elif button.on == False:
                ctl_settings.playbackMode = False

        elif button.title == 'ST MODE':
            button.update()
            if button.on == True:
                ctl_settings.sensorTuningMode = True
            elif button.on == False:
                ctl_settings.sensorTuningMode = False

        elif button.title == 'MAP':
            button.update()
            if button.on == True:
                ctl_settings.mapping = True
            elif button.on == False:
                ctl_settings.mappin = False

        # Next check Network button
        elif button.title == 'NETWORK':
            button.update()
            if button.on == True:
                ctl_settings.networkOn = True
            elif button.on == False:
                ctl_settings.networkOn = False

        # Next check Feedback Mode automation buttons
        elif button.title == 'Bandpass': # can be set with FB MODE off for presetting
            button.update()
            if button.on == True: # is this best way to do this?
                bandpass_automation(panels['Wall Panels']) # send wall panels only
                ctl_settings.bandpass = True
            elif button.on == False:
                allpass_automation(panels['Wall Panels'])
                ctl_settings.bandpass = False

        elif button.title == 'Mic' and ctl_settings.feedbackMode: # can't be set without FB MODE on
            button.update()
            if button.on == True:
                mic_on_off_automation(panels['Wall Panels'], 100) # turn mic on
            elif button.on == False:
                mic_on_off_automation(panels['Wall Panels'], 0) # turn off

        # Next check Ternary Controller and button
        elif check_column and ctl_settings.ternaryWallMode: # Turn other buttons off in ternary control array
            button.update()
            none_on = True
            for other_button in column.column:
                if other_button != button and other_button.on == True:
                    none_on = False
                    other_button.update()
            if none_on:
                button.update()
            column.update()

        elif button.title == 'Send Code' and ctl_settings.ternaryWallMode:
            button.update()
            send_code_automation(button, ctl_settings, screen, panels, mouse_y)

        elif button.title == 'brick' and ctl_settings.playbackMode:
            button.update()

def bandpass_automation(wall_panels):
    print("bandpass automation") # not sure about the scaling here
    hp = 6.3
    lp = 9.7
    for panel in wall_panels:
        panel.sliders[1].automate(hp)
        panel.sliders[2].automate(lp)
        hp += 12
        lp += 11

def allpass_automation(wall_panels):
    print("bandpass automation")
    for panel in wall_panels:
        panel.sliders[1].automate(0)
        panel.sliders[2].automate(100)

def mic_on_off_automation(wall_panels, gain_val):
    print("Mic on/off")
    for panel in wall_panels:
        panel.sliders[0].automate(gain_val)

def feedback_default_automation(ctl_settings, panels):
    print("Feedback Mode Default")
    for panel in panels['Wall Panels']:
        panel.sliders[0].automate(ctl_settings.mic)
        panel.sliders[3].automate(ctl_settings.res)
        panel.sliders[4].automate(ctl_settings.threshold)
        panel.sliders[5].automate(ctl_settings.packetLength)
        panel.sliders[6].automate(ctl_settings.delayLength)
        if panels['Automation Panel'].buttons[0].on == False: # Only set HP/LP if 'Bandpass' is off
            panel.sliders[1].automate(ctl_settings.hp)
            panel.sliders[2].automate(ctl_settings.lp)


def all_off_automation(ctl_settings, panels):
    print("All Off")
    for panel in panels['Wall Panels']:
        panel.sliders[0].automate(0)
        panel.sliders[3].automate(0)
        panel.sliders[4].automate(0)
        panel.sliders[5].automate(0)
        panel.sliders[6].automate(0)
        if panels['Automation Panel'].buttons[4].on == False: # Only turn off HP/LP if 'Bandpass' is off
            panel.sliders[1].automate(0)
            panel.sliders[2].automate(0)

def send_code_automation(button, ctl_settings, screen, panels, mouse_y):
    if button.on == True:
        panels['Ternary Panel'].controller.get_ternary_chain()
        print(panels['Ternary Panel'].controller.ternary_chain)
        if ctl_settings.networkOn:
            try:
                nf.send_ternary_chain(ctl_settings,
                            panels['Ternary Panel'].controller.ternary_chain)
            except:
                print("Network error")
        else:
            print('Network Off')

        # update screen then turn off button - 'bang'
        update_screen(ctl_settings, screen, panels, mouse_y)
        pygame.time.wait(500)
        button.update()


def update_screen(ctl_settings, screen, panels, mouse_y):


    # Update Wall Panel
    panels['Wall Panels'][ctl_settings.wall_panel].update(mouse_y)
    # Update Wall Map
    panels['Wall Map'].update()
    # Update Playback Panel
    panels['Playback Panel'].update(mouse_y)

    # draw screen
    screen.fill(ctl_settings.bg_color)
    # draw wall panel
    panels['Wall Panels'][ctl_settings.wall_panel].draw_panel_and_sliders()
    # draw automation panel
    panels['Automation Panel'].draw_panel_and_buttons()
    # draw sound code panel
    panels['Ternary Panel'].draw_panel_and_controller()
    # draw wall map panel
    panels['Wall Map'].draw_panel_and_contents()
    # draw playback panel
    panels['Playback Panel'].draw_panel_and_buttons()

    pygame.display.flip()