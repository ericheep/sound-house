import pygame
from slider import Slider
from button import Button
from ternary_control import TernaryControl
import map_objects

class Panel():
    """A parent panel class."""

    def __init__(self, ctl_settings, screen, label, top_y, height=170): # can specify y-axis location but not x-axis
        """Initialize panel and starting position."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ctl_settings = ctl_settings
        self.label = label

        # Set dimensions and color
        self.padding = 10
        self.color = self.ctl_settings.panel_bg_color
        self.width, self.height = (self.ctl_settings.screen_width / 2) - \
                                  (self.padding * 2), height
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 22)

        # Build panel rect object and move to location
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.top = top_y + self.padding
        self.rect.left = self.screen_rect.left + self.padding

        # Prep panel label
        self.prep_label()

    def prep_label(self):
        """Turn wall num label into rendered image and center in top left"""
        self.label_image = self.font.render(self.label, True,
                                            self.text_color, self.color)
        self.label_image_rect = self.label_image.get_rect()
        self.label_image_rect.top = self.rect.top + self.padding
        self.label_image_rect.left = self.rect.left + self.padding

    def draw_panel(self):
        # Draw panel and label
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.label_image, self.label_image_rect)

class WallPanel(Panel): # 0-7
    """A Panel subclass which handles the individual controls for each wall."""
    def __init__(self, ctl_settings, screen, label, top_y, wall_index):
        super().__init__(ctl_settings, screen, label, top_y)
        self.wall_index = wall_index
        self.wall_label = "Wall " + str(wall_index + 1)

        self.slider_spacing = 50  # distance between sliders

        # fix the way wall number is added to message (move to slider.py?)
        self.slider_bottom = self.rect.bottom - self.padding

        micGainSL = Slider(self.ctl_settings, self.screen, 0, 1, 85,
                           self.slider_bottom, '/micGain', wall_index, 'log')
        hpCutoffSL = Slider(self.ctl_settings, self.screen, 0, 10000,
                            micGainSL.rect.right + self.slider_spacing,
                            self.slider_bottom, '/hpCutoff', wall_index, 'exp')
        lpCutoffSL = Slider(self.ctl_settings, self.screen, 0, 20000,
                            hpCutoffSL.rect.right + self.slider_spacing,
                            self.slider_bottom, '/lpCutoff', wall_index, 'exp')
        resSL = Slider(self.ctl_settings, self.screen, 0, 1,
                       lpCutoffSL.rect.right + self.slider_spacing,
                       self.slider_bottom, '/res', wall_index, 'log')
        thresholdSL = Slider(self.ctl_settings, self.screen, 0.1, 50,
                             resSL.rect.right + self.slider_spacing,
                             self.slider_bottom, '/threshold', wall_index,
                             'linear')
        packetLengthSL = Slider(self.ctl_settings, self.screen, 0, 1000,
                                thresholdSL.rect.right + self.slider_spacing,
                                self.slider_bottom, '/packetLength',
                                wall_index, 'linear')
        delayLengthSL = Slider(self.ctl_settings, self.screen, 0, 10000,
                               packetLengthSL.rect.right + self.slider_spacing,
                               self.slider_bottom, '/delayLength', wall_index,
                               'linear')

        # Add all sliders to this list
        self.sliders = [micGainSL, hpCutoffSL, lpCutoffSL, resSL, thresholdSL,
                        packetLengthSL, delayLengthSL]

        # prep wall label
        self.prep_wall_label()

    def prep_wall_label(self):
        """Turn wall num label into rendered image and center in top left"""
        self.wall_label_image = self.font.render(self.wall_label, True,
                                            self.text_color, self.color)
        self.wall_label_image_rect = self.label_image.get_rect()
        self.wall_label_image_rect.top = self.rect.top + self.padding
        self.wall_label_image_rect.centerx = self.rect.centerx # center in screen

    def update(self, mouse_y): # updates every screen for mouse values
        self.draw_panel_and_sliders()
        for slider in self.sliders:
            slider.update(mouse_y)
            slider.draw_slider()

    def draw_panel_and_sliders(self):
        # Draw panel and label and wall label
        self.draw_panel()
        self.screen.blit(self.wall_label_image, self.wall_label_image_rect)


class AutomationPanel(Panel):
    """A Panel subclass containing buttons for sound automation."""
    def __init__(self, ctl_settings, screen, label, top_y, height=130):
        super().__init__(ctl_settings, screen, label, top_y, height)

        self.padding = 50 # custom padding here

        self.button_x_spacing = 30

        # Mode buttons first
        fb_button = Button(ctl_settings, screen, 40,
                           self.rect.top + self.padding, 'FB MODE') # Feedback

        tc_button = Button(ctl_settings, screen,
                           fb_button.rect.right + self.button_x_spacing,
                           self.rect.top + self.padding, 'TC MODE') # Ternary Sound Code

        pb_button = Button(ctl_settings, screen,
                           tc_button.rect.right + self.button_x_spacing,
                           self.rect.top + self.padding, 'PB MODE') # Sound Playback

        st_button = Button(ctl_settings, screen,
                           pb_button.rect.right + self.button_x_spacing,
                           self.rect.top + self.padding, 'ST MODE') # Sensor Tuning - shapes built on sensor data. better name?

        bp_button = Button(ctl_settings, screen,
                           st_button.rect.right + (self.button_x_spacing * 2),
                           self.rect.top + self.padding, 'Bandpass')
        mic_button = Button(ctl_settings, screen,
                            bp_button.rect.right + self.button_x_spacing,
                            self.rect.top + self.padding, 'Mic')
        network_button = Button(ctl_settings, screen,
                                self.rect.right - self.button_x_spacing -
                                self.padding, self.rect.top + self.padding,
                                'NETWORK')


        self.buttons = [fb_button, tc_button, pb_button, st_button, bp_button,
                        mic_button, network_button]  # add all buttons here

    def update(self):
        # update each button
        for button in self.buttons:
            button.update()

    def draw_panel_and_buttons(self):
        self.draw_panel()
        for button in self.buttons:
            button.draw_button()


class TernaryPanel(Panel):
    """A Panel subclass for the ternary code control."""
    def __init__(self, ctl_settings, screen, label, top_y, height):
        super().__init__(ctl_settings, screen, label, top_y, height)

        self.padding = 50 # custom padding here

        send_code_button = Button(ctl_settings, screen,
                                  40, self.rect.top + self.padding, 'Send Code')

        self.buttons = [send_code_button]

        # Make a ternary button controller
        self.controller = TernaryControl(ctl_settings, screen,
                                         send_code_button.rect.right + 30,
                                         self.rect.top + 30)

    def update(self):
        # update each button
        for button in self.buttons:
            button.update()

    def draw_panel_and_controller(self):
        self.draw_panel()
        self.controller.draw_controller()
        for button in self.buttons:
            button.draw_button()


class WallMapPanel(Panel):
    """A Panel subclass for the wall mapping control."""
    def __init__(self, ctl_settings, screen, label, top_y, height):
        super().__init__(ctl_settings, screen, label, top_y, height)
        # set panel properties
        self.rect.right = self.screen_rect.right - self.padding
        self.prep_label()

        zero_x = self.rect.left
        zero_y = self.rect.top

        self.walls = []
        # make 8 walls
        x, y = zero_x + 5, zero_y + 60
        for i in range(8):
            label = str(i + 1)
            wall = map_objects.Wall(ctl_settings, screen, self, x, y, label)
            y += 40
            self.walls.append(wall)
        self.walls[ctl_settings.wall_panel].on = True

        # make 2 puppets
        x, y = self.rect.centerx, self.rect.centery
        self.puppet1 = map_objects.Puppet(ctl_settings, screen, self, x, y,
                                         'P1')
        self.puppet2 = map_objects.Puppet(ctl_settings, screen, self, x,
                                          y + 20, 'P2')
        self.puppets = [self.puppet1, self.puppet2] # add all puppets to list
        self.puppets[ctl_settings.puppet].onoff() # Turn default puppet on

    def switch_wall(self):
        for wall in self.walls:
            if wall == self.walls[self.ctl_settings.wall_panel]:
                wall.on = True
            else:
                wall.on = False
                wall.moving_right = False
                wall.moving_left = False
                wall.moving_up = False
                wall.moving_down = False
                wall.update()

    def update(self):
        self.walls[self.ctl_settings.wall_panel].update()
        for puppet in self.puppets:
            puppet.update()

    def draw_panel_and_contents(self):
        self.draw_panel()
        for wall in self.walls:
            wall.draw_wall()
        for puppet in self.puppets:
            puppet.draw_puppet()