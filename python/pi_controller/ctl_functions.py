import sys, pygame, pygame.midi
import network_functions as nf
import midi_functions as mf
import other_functions as of
from fractions import Fraction

def check_events(ctl_settings, screen, panels, midi_input, mouse_x, mouse_y):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            shutdown(ctl_settings, midi_input)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ctl_settings, screen, panels,
                                 midi_input)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ctl_settings, screen, panels)

        # Mouse events --factor out!
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_wall_sliders(ctl_settings, panels, mouse_x, mouse_y) # check wall panel clicks
            for button in panels['Automation Panel'].buttons.values(): # check automation panel clicks
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
            check_slider(panels['Playback Panel'].BPM, ctl_settings, panels,
                         mouse_x, mouse_y) # check BPM slider
            if ctl_settings.mapping:
                check_map_clicks(ctl_settings, panels, mouse_x, mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            wall_sliders_stop(ctl_settings, panels)
            if panels['Playback Panel'].BPM.k_moving:
                if ctl_settings.playbackMode:
                    # Updates timer
                    if panels['Playback Panel'].timer:
                        pygame.time.set_timer(ctl_settings.PB_EVENT,
                                              ctl_settings.bpm_ms)
                panels['Playback Panel'].BPM.k_moving = False
            # Stop all walls and puppets
            for wall in panels['Wall Map'].walls:
                wall.mouse_move = False
            for puppet in panels['Wall Map'].puppets:
                puppet.mouse_move = False

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

        # PING Events
        elif event.type == ctl_settings.PING_EVENT:
            nf.ping_sensors(ctl_settings)

    # MIDI events
    if midi_input:
        check_MIDI(ctl_settings, screen, panels, midi_input)

def shutdown(ctl_settings, midi_input):
    # shutdown procedures
    print('Goodbye')
    nf.stopServer(ctl_settings)
    if midi_input:
        midi_input.close()
    sys.exit()

def check_keydown_events(event, ctl_settings, screen, panels, midi_input):
    if event.key == pygame.K_q:
        shutdown(ctl_settings, midi_input)
    if ctl_settings.key_entry == False:
        # select wall panel with num entry
        if event.key == pygame.K_1:
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

    elif ctl_settings.key_entry:
        keyname = pygame.key.name(event.key)
        if keyname == 'return':
            convert_to_fraction(ctl_settings)
            ctl_settings.entry = '' # reset
            panels['Ternary Panel'].display_interval.target = ctl_settings.interval
        else:
            ctl_settings.entry += keyname


    # turn off sine tones
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
            print(ctl_settings.wall_sensors) # delete this
            print(ctl_settings.wall_amps)

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

def convert_to_fraction(ctl_settings):
    # convert fraction string to fraction
    try:
        strings = ctl_settings.entry.split('/')
        num = int(strings[0])
        den = int(strings[1])
        ctl_settings.interval = Fraction(num, den)
    except:
        print('Invalid Entry')

def check_wall_sliders(ctl_settings, panels, mouse_x, mouse_y):
    for index, slider in \
            enumerate(panels['Wall Panels'][ctl_settings.wall_panel].sliders):
        check_slider(slider, ctl_settings, panels, mouse_x, mouse_y,
                     slider_index=index)

def check_slider(slider, ctl_settings, panels, mouse_x, mouse_y,
                 slider_index=None):
    knob_clicked = slider.rect.collidepoint(mouse_x, mouse_y)
    if knob_clicked:
        if slider_index == None:
            slider.k_moving = True
        elif slider_index >= 0 and ctl_settings.set_all:
            for panel in panels['Wall Panels']:
                panel.sliders[slider_index].k_moving = True

        else: # can this be cleared?
            slider.k_moving = True

def wall_sliders_stop(ctl_settings, panels):
    for panel in panels['Wall Panels']:  # check wall panel click releases
        for slider in panel.sliders:
            slider.k_moving = False

def check_map_clicks(ctl_settings, panels, mouse_x, mouse_y):
    for wall in panels['Wall Map'].walls:
        wall_clicked = wall.rect.collidepoint(mouse_x, mouse_y)
        if wall_clicked:
            wall_index = int(wall.label) - 1
            ctl_settings.wall_panel = wall_index
            panels['Wall Map'].switch_wall()
            panels['Wall Map'].walls[wall_index].mouse_move = True

    for index, puppet in enumerate(panels['Wall Map'].puppets):
        puppet_clicked = puppet.rect.collidepoint(mouse_x, mouse_y)
        if puppet_clicked:
            on_puppet = ctl_settings.puppet
            if on_puppet == 0:
                off_puppet = 1
            else:
                off_puppet = 0

            if puppet.on == False:
                puppet.onoff()
                panels['Wall Map'].puppets[on_puppet].onoff()
                ctl_settings.puppet = off_puppet

            puppet.mouse_move = True


def check_button(button, screen, ctl_settings, panels, mouse_x, mouse_y,
                 column=None, check_column=False):
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:

        # check modes first, right now activating one mode doesn't turn others off--add this behavior later
        if button.title == 'TC MODE':
            button.update()
            if button.on == True:
                ctl_settings.ternaryWallMode = True
                if ctl_settings.networkOn:
                    if panels['Automation Panel'].buttons['SENSORS'].on == False:
                        panels['Automation Panel'].buttons['SENSORS'].update()
                        for panel in panels['Wall Panels']:
                            panel.sensor_reading.update()
                        # start timer for pinging sensors
                        pygame.time.set_timer(ctl_settings.PING_EVENT,
                                              ctl_settings.ping_interval)
                else:
                    ctl_settings.wall_amps = [ctl_settings.amp_high for wall
                                              in range(8)]

            elif button.on == False:
                ctl_settings.ternaryWallMode = False
                ctl_settings.wall_amps = [0 for wall in range(8)]

        elif button.title == 'FB MODE':
            button.update()
            if button.on == True:
                ctl_settings.feedbackMode = True
                feedback_default_automation(ctl_settings, panels)
                if panels['Automation Panel'].buttons['MIC'].on == False:
                    panels['Automation Panel'].buttons['MIC'].update() # Turn 'Mic' on
            elif button.on == False:
                ctl_settings.feedbackMode = False
                all_off_automation(ctl_settings, panels)
                if panels['Automation Panel'].buttons['MIC'].on:
                    panels['Automation Panel'].buttons['MIC'].update() # Turn 'Mic' off

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
                ctl_settings.mapping = False

        elif button.title == 'Sensors':
            if ctl_settings.networkOn == True:
                button.update()
                for panel in panels['Wall Panels']:
                    panel.sensor_reading.update()
                if button.on == True:
                    ctl_settings.sensors = True
                    # start timer for pinging sensors
                    pygame.time.set_timer(ctl_settings.PING_EVENT,
                                          ctl_settings.ping_interval)
                elif button.on == False:
                    ctl_settings.sensors = False
                    # turn timer off
                    pygame.time.set_timer(ctl_settings.PING_EVENT, 0)
            else:
                print("Network must be running to ping sensors.")

        # Next check Network button
        elif button.title == 'NETWORK':
            button.update()
            if button.on == True:
                ctl_settings.networkOn = True
            elif button.on == False:
                ctl_settings.networkOn = False
                if ctl_settings.sensors:
                    # turn sensors off
                    panels['Automation Panel'].buttons['SENSORS'].update()
                    ctl_settings.sensors = False
                    for panel in panels['Wall Panels']:
                        panel.sensor_reading.update()

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

        elif button.title == 'Interval':
            button.update()
            if button.on:
                ctl_settings.key_entry = True
            elif button.on == False:
                ctl_settings.key_entry = False

        elif button.title == 'brick' and ctl_settings.playbackMode:
            button.update()

        elif button.title == 'Video':
            button.update()
            if button.on:
                ctl_settings.sendVideo = True
            else:
                ctl_settings.sendVideo = False

        elif button.title == 'Set All':
            button.update()
            if button.on:
                ctl_settings.set_all = True
            else:
                ctl_settings.set_all = False

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
        if panels['Automation Panel'].buttons['BANDPASS'].on == False: # Only set HP/LP if 'Bandpass' is off
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


def update_screen(ctl_settings, screen, panels, mouse_x, mouse_y):


    # Update Wall Panels
    for panel in panels['Wall Panels']:
        panel.update(mouse_y)
#    panels['Wall Panels'][ctl_settings.wall_panel].update(mouse_y)
    # Update Wall Map
    panels['Wall Map'].update(mouse_x, mouse_y)
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