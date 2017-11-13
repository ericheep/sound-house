import sys, pygame, pygame.midi
from time import sleep
import network_functions as nf
import other_functions as of

def check_slider(slider, mouse_x, mouse_y):
    knob_clicked = slider.rect.collidepoint(mouse_x, mouse_y)
    if knob_clicked:
        slider.k_moving = True

def check_button(button, screen, ctl_settings, wall_panels, automation_panel,
                 ternary_panel, mouse_x, mouse_y, column=None,
                 check_column=False):
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        button.update()

        if check_column: # Turn other buttons off in ternary control array
            none_on = True
            for other_button in column.column:
                if other_button != button and other_button.on == True:
                    none_on = False
                    other_button.update()
            if none_on:
                button.update()
            column.update()

        if button.title == 'Bandpass':
            if button.on == True: # is this best way to do this?
                bandpass_automation(wall_panels)
            elif button.on == False:
                allpass_automation(wall_panels)
        elif button.title == 'Mic':
            if button.on == True:
                mic_on_off_automation(wall_panels, 100) # turn mic on
            elif button.on == False:
                mic_on_off_automation(wall_panels, 0) # turn off
        elif button.title == 'Feedback':
            if button.on == True:
                feedback_default_automation(ctl_settings, wall_panels,
                                            automation_panel)
                if automation_panel.buttons[1].on == False:
                    automation_panel.buttons[1].update() # Turn 'Mic' on
            elif button.on == False:
                all_off_automation(ctl_settings, wall_panels, automation_panel)
                if automation_panel.buttons[1].on == True:
                    automation_panel.buttons[1].update() # Turn 'Mic' off
        elif button.title == 'Send Code':
            if button.on == True:
                ternary_panel.controller.get_ternary_chain()
                print(ternary_panel.controller.ternary_chain)

                nf.send_ternary_chain(ctl_settings,
                        ternary_panel.controller.ternary_chain)
                #except:
                #    print("Network error")

                # update screen then turn off button - 'bang'
                update_screen(ctl_settings, screen, wall_panels,
                              automation_panel, ternary_panel, mouse_y)
                sleep(0.5)
                button.update()

def check_events(ctl_settings, screen, wall_panels, automation_panel,
                 ternary_panel, midi_input, ternary_chain, mouse_x, mouse_y):
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
                ctl_settings.wall_panel = 0
            elif event.key == pygame.K_2:
                ctl_settings.wall_panel = 1
            elif event.key == pygame.K_3:
                ctl_settings.wall_panel = 2
            elif event.key == pygame.K_4:
                ctl_settings.wall_panel = 3
            elif event.key == pygame.K_5:
                ctl_settings.wall_panel = 4
            elif event.key == pygame.K_6:
                ctl_settings.wall_panel = 5
            elif event.key == pygame.K_7:
                ctl_settings.wall_panel = 6
            elif event.key == pygame.K_8:
                ctl_settings.wall_panel = 7

            elif event.key == pygame.K_o:
                nf.send_OscControl_off(ctl_settings)

        # Mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for panel in wall_panels:
                for slider in panel.sliders:
                    check_slider(slider, mouse_x, mouse_y)
            for button in automation_panel.buttons:
                check_button(button, screen, ctl_settings, wall_panels,
                             automation_panel, ternary_panel, mouse_x, mouse_y)
            for button in ternary_panel.buttons:
                check_button(button, screen, ctl_settings, wall_panels,
                             automation_panel, ternary_panel, mouse_x, mouse_y)
            for column in ternary_panel.controller.column_list:
                for button in column.column:
                    check_button(button, screen, ctl_settings, wall_panels,
                                 automation_panel, ternary_panel, mouse_x,
                                 mouse_y, column, check_column=True)
        elif event.type == pygame.MOUSEBUTTONUP:
            for panel in wall_panels:
                for slider in panel.sliders:
                    slider.k_moving = False

    # MIDI events
    if midi_input:  # factor and double-check this
        if midi_input.poll():
            ctl, val = mf.get_ctl_and_value(midi_input)
            # print(ctl)

            if ctl_settings.ternaryWallMode:
                if ctl < 7:
                    mf.midi_to_ternary(ternary_chain, ctl, val)
                if ctl == 41 and val == 127:
                    print(ternary_chain)
                    freqs = of.convert_chain_to_freqs(ternary_chain,
                                                      ctl_settings)
                    print(freqs)
                    # add call to function to convert to freq and send to walls


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

def feedback_default_automation(ctl_settings, wall_panels, automation_panel):
    print("Feedback Mode Default")
    for panel in wall_panels:
        panel.sliders[0].automate(ctl_settings.mic)
        panel.sliders[3].automate(ctl_settings.res)
        panel.sliders[4].automate(ctl_settings.threshold)
        panel.sliders[5].automate(ctl_settings.packetLength)
        panel.sliders[6].automate(ctl_settings.delayLength)
        if automation_panel.buttons[0].on == False: # Only set HP/LP if 'Bandpass' is off
            panel.sliders[1].automate(ctl_settings.hp)
            panel.sliders[2].automate(ctl_settings.lp)


def all_off_automation(ctl_settings, wall_panels, automation_panel):
    print("All Off")
    for panel in wall_panels:
        panel.sliders[0].automate(0)
        panel.sliders[3].automate(0)
        panel.sliders[4].automate(0)
        panel.sliders[5].automate(0)
        panel.sliders[6].automate(0)
        if automation_panel.buttons[0].on == False: # Only turn off HP/LP if 'Bandpass' is off
            panel.sliders[1].automate(0)
            panel.sliders[2].automate(0)


def update_screen(ctl_settings, screen, wall_panels, automation_panel,
                  ternary_panel, mouse_y):

    # draw screen
    screen.fill(ctl_settings.bg_color)
    # draw wall panel
    wall_panels[ctl_settings.wall_panel].update(mouse_y)
    # draw automation panel
    automation_panel.draw_panel_and_buttons()
    # draw sound code panel
    ternary_panel.draw_panel_and_controller()

    pygame.display.flip()