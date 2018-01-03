import pygame
from slider import Slider
from button import Button
from display_value import DisplayValue
from ternary_control import TernaryControl
import map_objects
from other_functions import find_distance

class Panel():
    """A parent panel class."""

    def __init__(self, ctl_settings, screen, label, top_y, height=170,
                 full_length=False): # can specify y-axis location but not x-axis
        """Initialize panel and starting position."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ctl_settings = ctl_settings
        self.label = label

        # Set dimensions and color
        self.padding = 10
        self.color = self.ctl_settings.panel_bg_color
        if full_length:
            self.width = self.ctl_settings.screen_width - self.padding * 2
        else:
            self.width = (self.ctl_settings.screen_width / 2) - \
                                  (self.padding * 2)
        self.height = height
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

        # sensor reading

        self.sensor_reading = DisplayValue(ctl_settings, self.screen, 40,
                                           self.rect.bottom - self.padding,
                                           wall_index=wall_index,
                                           title='Sensor')

        self.slider_spacing = 50  # distance between sliders

        # fix the way wall number is added to message (move to slider.py?)
        self.slider_bottom = self.rect.bottom - self.padding

        micGainSL = Slider(self.ctl_settings, self.screen, 0, 1,
                           self.sensor_reading.rect.right + 10,
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
        for slider in self.sliders:
            slider.update(mouse_y)

    def draw_panel_and_sliders(self):
        # Draw panel and label and wall label
        self.draw_panel()
        self.sensor_reading.draw_display()
        for slider in self.sliders:
            slider.draw_slider()
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

        map_button = Button(ctl_settings, screen,
                            st_button.rect.right + self.button_x_spacing,
                            self.rect.top + self.padding, 'MAP')

        sensor_button = Button(ctl_settings, screen,
                               map_button.rect.right + self.button_x_spacing,
                               self.rect.top + self.padding, 'Sensors')

        bp_button = Button(ctl_settings, screen,
                           sensor_button.rect.right + self.button_x_spacing,
                           self.rect.top + self.padding, 'Bandpass')

        mic_button = Button(ctl_settings, screen,
                            bp_button.rect.right + self.button_x_spacing,
                            self.rect.top + self.padding, 'Mic')

        video_button = Button(ctl_settings, screen,  # where to put this??
                              mic_button.rect.right + self.button_x_spacing,
                              self.rect.top + self.padding, 'Video')

        set_all_button = Button(ctl_settings, screen,
                                video_button.rect.right +
                                self.button_x_spacing,
                                self.rect.top + self.padding, 'Set All')

        network_button = Button(ctl_settings, screen,
                                set_all_button.rect.right +
                                self.button_x_spacing,
                                self.rect.top + self.padding,
                                'NETWORK')

        self.buttons = {
            'FEEDBACK': fb_button, 'TERNARY': tc_button, 'PLAYBACK': pb_button,
            'TUNING': st_button, 'MAP': map_button, 'SENSORS': sensor_button,
            'BANDPASS': bp_button, 'MIC': mic_button,
            'NETWORK': network_button, 'VIDEO': video_button,
            'SET ALL': set_all_button
        } # add all buttons here

    def draw_panel_and_buttons(self):
        self.draw_panel()
        for button in self.buttons.values():
            button.draw_button()


class TernaryPanel(Panel):
    """A Panel subclass for the ternary code control."""
    def __init__(self, ctl_settings, screen, label, top_y, height):
        super().__init__(ctl_settings, screen, label, top_y, height)

        self.padding = 50 # custom padding here

        send_code_button = Button(ctl_settings, screen,
                                  40, self.rect.top + self.padding,
                                  'Send Code')


        self.display_interval = DisplayValue(ctl_settings, screen,
                                             send_code_button.rect.right + 30,
                                             send_code_button.rect.bottom,
                                             title='Interval',
                                             target=ctl_settings.interval)

        self.buttons = [send_code_button, self.display_interval]


        # Make a ternary button controller
        self.controller = TernaryControl(ctl_settings, screen,
                                         self.display_interval.rect.right + 30,
                                         self.rect.top + 30)

    def draw_panel_and_controller(self):
        self.draw_panel()
        #self.display_interval.draw_display()
        self.controller.draw_controller()
        for button in self.buttons:
            try:
                button.draw_button()
            except:
                button.draw_display()


class WallMapPanel(Panel):
    """A Panel subclass for the wall mapping control."""
    def __init__(self, wall_panels, ctl_settings, screen, label, top_y, height):
        super().__init__(ctl_settings, screen, label, top_y, height)
        # make all panels available
        self.wall_panels = wall_panels
        # set panel properties
        self.rect.right = self.screen_rect.right - self.padding
        self.prep_label()

        self.zero_x = self.rect.left
        self.zero_y = self.rect.top

        self.walls = []
        # make 8 walls
        x, y = self.zero_x + 5, self.zero_y + 60
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

        # stores distances between walls and puppets
        self.p1_distances = [0, 0, 0, 0, 0, 0, 0, 0] # initialize with 8 values
        self.p2_distances = [0, 0, 0, 0, 0, 0, 0, 0]

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

    def update(self, mouse_x, mouse_y):
        self.walls[self.ctl_settings.wall_panel].update(mouse_x, mouse_y)
        for puppet in self.puppets:
            puppet.update(mouse_x, mouse_y)

    def draw_panel_and_contents(self):
        self.draw_panel()
        for wall in self.walls:
            wall.draw_wall()
        for puppet in self.puppets:
            puppet.draw_puppet()

    def get_distances(self):
        for index, wall in enumerate(self.walls):
            self.p1_distances[index] = find_distance(wall, self.puppet1, self)
            self.p2_distances[index] = find_distance(wall, self.puppet2, self)
        if self.ctl_settings.bandpass:
            self.scale_factor = 80 # val should be less than 100 so there's always a window
            self.scale_offset = 20 # how wide a band
            for index, wall in enumerate(self.wall_panels):
                if self.ctl_settings.puppet == 0:
                    val = (self.p1_distances[index] * self.scale_factor)
                    wall.sliders[1].automate(val + self.scale_offset, reverse=True)
                    wall.sliders[2].automate(val, reverse=True)
                if self.ctl_settings.puppet == 1:
                    val = self.p2_distances[index] * self.scale_factor
                    wall.sliders[1].automate(val + self.scale_offset, reverse=True)
                    wall.sliders[2].automate(val, reverse=True)


class PlaybackPanel(Panel):
    """A Panel subclass for the ternary code control."""

    def __init__(self, ctl_settings, screen, label, top_y, height,
                 fullsize):
        super().__init__(ctl_settings, screen, label, top_y, height,
                         fullsize)

        self.timer = False

        self.padding = 50  # custom padding here

        self.button_x_spacing = 30

        # add slider to control playback speed: ctl_settings.bpm
        self.slider_bottom = self.rect.bottom - 10

        self.BPM = Slider(self.ctl_settings, self.screen, 0, 200,
                          self.rect.left + self.button_x_spacing,
                          self.slider_bottom, 'BPM', 'linear')
        self.BPM.automate(30) # set initial value

        # Display buttons in sequencer - to show sequence
        row1_y = self.rect.top + self.padding
        pb1 = Button(ctl_settings, screen,
                     self.BPM.rect.right + self.button_x_spacing, row1_y, '1')
        pb2 = Button(ctl_settings, screen,
                     pb1.rect.right + self.button_x_spacing, row1_y, '2')
        pb3 = Button(ctl_settings, screen,
                     pb2.rect.right + self.button_x_spacing, row1_y, '3')
        pb4 = Button(ctl_settings, screen,
                     pb3.rect.right + self.button_x_spacing, row1_y, '4')
        pb5 = Button(ctl_settings, screen,
                     pb4.rect.right + self.button_x_spacing, row1_y, '5')
        pb6 = Button(ctl_settings, screen,
                     pb5.rect.right + self.button_x_spacing, row1_y, '6')
        pb7 = Button(ctl_settings, screen,
                     pb6.rect.right + self.button_x_spacing, row1_y, '7')
        pb8 = Button(ctl_settings, screen,
                     pb7.rect.right + self.button_x_spacing, row1_y, '8')

        self.buttons = [pb1, pb2, pb3, pb4, pb5, pb6, pb7, pb8]  # add all buttons here

        # Control buttons in sequencer - to show sequence
        row2_y = pb1.rect.bottom + 13
        brick1 = Button(ctl_settings, screen,
                        self.BPM.rect.right + self.button_x_spacing, row2_y, 'brick')
        brick2 = Button(ctl_settings, screen,
                        brick1.rect.right + self.button_x_spacing, row2_y, 'brick')
        brick3 = Button(ctl_settings, screen,
                        brick2.rect.right + self.button_x_spacing, row2_y, 'brick')
        brick4 = Button(ctl_settings, screen,
                        brick3.rect.right + self.button_x_spacing, row2_y, 'brick')
        brick5 = Button(ctl_settings, screen,
                        brick4.rect.right + self.button_x_spacing, row2_y, 'brick')
        brick6 = Button(ctl_settings, screen,
                        brick5.rect.right + self.button_x_spacing, row2_y, 'brick')
        brick7 = Button(ctl_settings, screen,
                        brick6.rect.right + self.button_x_spacing, row2_y, 'brick')
        brick8 = Button(ctl_settings, screen,
                        brick7.rect.right + self.button_x_spacing, row2_y, 'brick')
        self.brick_buttons = [brick1, brick2, brick3, brick4, brick5, brick6,
                              brick7, brick8]


    def update(self, mouse_y): # updates every screen for mouse values
        self.BPM.update(mouse_y)
        # convert BPM to ms
        try:
            self.ctl_settings.bpm_ms = int(60000 / self.BPM.ctl_value)
        except ZeroDivisionError:
            self.ctl_settings.bpm_ms = 0


    def draw_panel_and_buttons(self):
        self.draw_panel()
        for button in self.buttons:
            button.draw_button()
        for button in self.brick_buttons:
            button.draw_button()
        self.BPM.draw_slider()