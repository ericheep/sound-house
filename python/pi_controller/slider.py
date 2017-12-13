import pygame
from scale_function import scale
from network_functions import send_audioControl_data, sendVideoTrigger # update vidoe function later

class Slider():
    """
    A class to handle graphical sliders for sound control in Sound House
    """
    def __init__(self, ctl_settings, screen, min_val, max_val, x, y, param,
                 wall_index=None, scale='linear'):
        """Initialize slider and starting position."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ctl_settings = ctl_settings
        self.min_val = min_val
        self.max_val = max_val
        self.x = x # left
        self.y = y # bottom
        if type(wall_index) == int:
            self.wall_index = wall_index
        else:
            self.wall_index = ''
        #exponential or linear scale
        if scale == 'linear':
            self.scale = 'linear'
        elif scale == 'exp':
            self.scale = 'exp'
        elif scale == 'log':
            self.scale = 'log'

        # Set dimensions and properties of slider
        self.width, self.height = 20, 100
        self.k_width, self.k_height = self.width, 10
        self.color = (100, 100, 100)
        self.k_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 14)

        # Build the slider's rect object and move to specified location
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottom = self.y
        self.rect.left = self.x
        # Knob rect
        self.k_rect = pygame.Rect(0, 0, self.k_width, self.k_height)
        self.k_rect.bottom = self.rect.bottom
        self.k_rect.centerx = self.rect.centerx
        # Movement flag
        self.k_moving = False

        # Initialize control value to 0
        self.ctl_value = 0

        # Specify parameter for OSC message
        if type(wall_index) == int:
            self.param = param + str(self.wall_index)
        else:
            self.param = param

        # Make visual label, use 'param'
        self.prep_title()

        # Prep message
        self.prep_msg()

        # Draw rectangle image for slider and knob
        self.slider = pygame.draw.rect(screen, self.color, (0, 0, self.width,
                                                            self.height), 0)
        self.knob = pygame.draw.rect(screen, self.k_color,
                                     (0, 0, self.k_width, self.k_height), 0)

    def get_ctl_value(self):
        self.knob_pos = self.rect.bottom - self.k_rect.bottom
        x0, x1 = 0, self.height
        y0, y1 = self.min_val, self.max_val
        self.ctl_value = scale(self.knob_pos, x0, x1, y0, y1, self.scale)
        self.prep_msg()
        msg = self.param
        val = self.ctl_value
        send_audioControl_data(self.ctl_settings, msg, val) #
        #sendVideoTrigger(self.ctl_settings, self.wall_index, val) #get rid of this

    def update(self, mouse_y):
        """Update knob position based on mouse click and movement."""
        if self.k_moving and self.k_rect.bottom <= self.rect.bottom \
                and self.k_rect.bottom >= self.rect.top:
            self.k_rect.centery = mouse_y
            self.get_ctl_value()
        elif self.k_moving and self.k_rect.bottom > self.rect.bottom:
            self.k_rect.bottom = self.rect.bottom
            self.k_moving = False
            self.get_ctl_value()
        elif self.k_moving and self.k_rect.bottom < self.rect.top:
            self.k_rect.bottom = self.rect.top
            self.k_moving = False
            self.get_ctl_value()

    def automate(self, value, reverse=False):
        """Update knob position based on value."""
        if reverse:
            self.k_rect.bottom = self.rect.top + value
        else:
            self.k_rect.bottom = self.rect.bottom - value
        self.get_ctl_value()

    def prep_msg(self):
        """Turn msg into rendered image and center on knob."""
        self.msg_image = self.font.render(str(self.ctl_value), True,
                                          self.text_color, self.k_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.k_rect.center

    def prep_title(self):
        """Turn param title into rendered image and center atop slider."""
        self.title_image = self.font.render(self.param, True, self.text_color,
                                            self.ctl_settings.panel_bg_color)
        self.title_image_rect = self.title_image.get_rect()
        self.title_image_rect.centerx = self.rect.centerx
        self.title_image_rect.bottom = self.rect.top - 10

    def draw_slider(self):
        # Draw blank slider and knob and msg
        self.screen.fill(self.color, self.rect)
        self.screen.fill(self.k_color, self.k_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.screen.blit(self.title_image, self.title_image_rect)