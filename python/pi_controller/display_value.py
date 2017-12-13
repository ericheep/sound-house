import pygame

class DisplayValue():
    """
    A class to handle displayed values in pi controller
    """
    def __init__(self, ctl_settings, screen, x, y, wall_index=None, title=None,
                 target=None):
        """Initialize button and starting position."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ctl_settings = ctl_settings
        self.x = x
        self.y = y

        # can't have wall_index and target
        self.wall_index = wall_index
        self.target = target

        # Set dimensions and properties of button
        self.width, self.height = 40, 20
        self.off_color = (100, 100, 100)
        self.on_color = (255, 255, 0) # yellow
        self.color = self.off_color # starts 'off'
        self.text_color = (255, 255, 255)
        self.display_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 14)

        # Build button's rect object and move to specified location
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.bottom = self.y # top left corner
        self.rect.left = self.x

        # Clicked 'on' or not
        self.on = False

        if title:
            # Make title
            self.title = title
            self.prep_title()
        else:
            self.title = None

        self.prep_value()

    def update(self):
        if self.on == False: # then turn 'on'
            self.color = self.on_color
            self.on = True
        else: # then turn 'off'
            self.color = self.off_color
            self.on = False

    def prep_title(self):
        """Turn title into rendered image and center above button."""
        self.title_image = self.font.render(self.title, True, self.text_color,
                                            self.ctl_settings.panel_bg_color)
        self.title_image_rect = self.title_image.get_rect()
        self.title_image_rect.centerx = self.rect.centerx
        self.title_image_rect.bottom = self.rect.top - 1

    def prep_value(self):
        """Turn value into rendered image and center below button."""
        if self.wall_index:
            self.value = self.ctl_settings.wall_sensors[self.wall_index]
        else:
            self.value = self.target
        self.value_image = self.font.render(str(self.value), True,
                                            self.display_color, self.color)
        self.value_image_rect = self.value_image.get_rect()
        self.value_image_rect.centerx = self.rect.centerx
        self.value_image_rect.centery = self.rect.centery

    def draw_display(self):
        # Draw button and title
        self.screen.fill(self.color, self.rect)
        if self.title:
            self.screen.blit(self.title_image, self.title_image_rect)
        elif self.target: #
            self.target = self.target #
        #if self.ctl_settings.sensors:
        self.prep_value()
        self.screen.blit(self.value_image, self.value_image_rect)