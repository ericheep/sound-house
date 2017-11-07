import pygame
from slider import Slider

class Panel(): # 0-7
    """A class to handle the back panel with label for slider controls."""

    def __init__(self, ctl_settings, screen, wall_index):
        """Initialize panel and starting position."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ctl_settings = ctl_settings
        self.wall_index = wall_index
        self.wall_num = "Wall " + str(wall_index + 1)

        # Set dimensions and color
        self.padding = 10
        self.color = (50, 50, 50)
        self.width, self.height = self.ctl_settings.screen_width - \
                                  (self.padding * 2), 150 # based on slider height
        self.slider_spacing = 50 # distance between sliders
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 22)

        # Build panel rect object and move to location
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.top = self.screen_rect.top + self.padding
        self.rect.left = self.screen_rect.left + self.padding

        # Prep panel label
        self.prep_label()

        # Add sliders. add self.?


        # fix the way wall number is added to message (move to slider.py?)
        # fix display (maybe don't display wall_num in panel???)
        micGainSL = Slider(self.ctl_settings, self.screen, 0, 1, 85, 40,
                           '/micGain', wall_index, 'log')
        hpCutoffSL = Slider(self.ctl_settings, self.screen, 0, 10000,
                            micGainSL.rect.right + self.slider_spacing, 40,
                            '/hpCutoff', wall_index, 'exp')
        lpCutoffSL = Slider(self.ctl_settings, self.screen, 0, 20000,
                            hpCutoffSL.rect.right + self.slider_spacing, 40,
                            '/lpCutoff', wall_index, 'exp')
        resSL = Slider(self.ctl_settings, self.screen, 0, 1,
                       lpCutoffSL.rect.right + self.slider_spacing, 40,
                       '/res', wall_index, 'log')
        thresholdSL = Slider(self.ctl_settings, self.screen, 0.1, 50,
                             resSL.rect.right + self.slider_spacing, 40,
                             '/threshold', wall_index, 'linear')
        packetLengthSL = Slider(self.ctl_settings, self.screen, 0, 1000,
                                thresholdSL.rect.right + self.slider_spacing,
                                40, '/packetLength', wall_index, 'linear')
        delayLengthSL = Slider(self.ctl_settings, self.screen, 0, 10000,
                               packetLengthSL.rect.right + self.slider_spacing,
                               40, '/delayLength', wall_index, 'linear')
        # Add all sliders to this list
        self.sliders = [micGainSL, hpCutoffSL, lpCutoffSL, resSL, thresholdSL,
                        packetLengthSL, delayLengthSL]

    def prep_label(self):
        """Turn wall num label into rendered image and center in top left"""
        self.label_image = self.font.render(self.wall_num, True,
                                            self.text_color, self.color)
        self.label_image_rect = self.label_image.get_rect()
        self.label_image_rect.top = self.rect.top + self.padding
        self.label_image_rect.left = self.rect.left + self.padding

    def update(self, mouse_y):
        self.draw_panel()
        for slider in self.sliders:
            slider.update(mouse_y)
            slider.draw_slider()

    def draw_panel(self):
        # Draw panel and label
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.label_image, self.label_image_rect)