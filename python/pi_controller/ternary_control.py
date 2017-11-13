import pygame
from button import Button

class TernaryColumn():
    """Consists of a single column of 3 stacked buttons and a digit display."""

    def __init__(self, ctl_settings, screen, x, y):
        self.ctl_settings = ctl_settings
        self.screen = screen
        self.x = x
        self.y = y
        self.rows = 3

        # Get button properties
        a_button = Button(self.ctl_settings, self.screen, 0, 0)
        self.width = a_button.width
        self.button_height = a_button.height
        self.height = (self.button_height * 3) + 2

        self.make_column()

        self.ternary_digit = 0 # starting value
        # text properties
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 16)
        # prep message
        self.prep_msg()

    def make_column(self):
        y = self.y + ((self.button_height + 1) * 2)
        self.column = []
        for row in range(self.rows):
            button = Button(self.ctl_settings, self.screen, self.x, y)
            self.column.append(button)
            y -= button.height + 1
        # initalize to 0
        self.column[0].update()

    def prep_msg(self):
        """Turn ternary digit into rendered image and display below column."""
        self.msg_image = self.font.render(str(self.ternary_digit), True,
                                          self.text_color,
                                          self.ctl_settings.panel_bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = self.column[0].rect.centerx
        self.msg_image_rect.top = self.column[0].rect.bottom + 5

    def update(self):
        for i, button in enumerate(self.column):
            if button.on == True:
                self.ternary_digit = i
                self.prep_msg()

    def draw_column(self):
        # draw the 3 buttons in column and digit display
        for button in self.column:
            button.draw_button()
        self.screen.blit(self.msg_image, self.msg_image_rect)

class TernaryControl():
    """A button-based controller for ternary sound code."""

    def __init__(self, ctl_settings, screen, x, y):
        """Initialize controller and starting position"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ctl_settings = ctl_settings
        self.x = x
        self.y = y

        self.make_controller()

    def make_controller(self):
        # 7 columns
        x = self.x
        y = self.y
        columns = 7
        self.column_list = []
        for column in range(columns):
            new_column = TernaryColumn(self.ctl_settings, self.screen, x, y)
            self.column_list.append(new_column)
            x += new_column.width + 7

    def draw_controller(self):
        # draw each column
        for column in self.column_list:
            column.draw_column()

    def get_ternary_chain(self):
        # Gets ternary digit from each column and stores in list
        self.ternary_chain = []
        for column in self.column_list:
            self.ternary_chain.append(column.ternary_digit)
        #print(self.ternary_chain)