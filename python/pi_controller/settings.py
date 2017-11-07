class Settings():
    """A class to store all settings for Sound House pi controller."""

    def __init__(self):
        """Initialize settings"""
        self.screen_width = 600 # change later when building interface window
        self.screen_height = 400
        self.bg_color = (0, 0, 0)

        # Ports
        self.portFeedbackControl = 7400
        self.portOscControl = 10001
        self.portPingSensors = 5000
        self.portGetSensorData = 12345

        #IPs
        self.wallIPs = ['127.00.0', '127.00.1', '127.00.2', '127.00.3', '127.00.4',
            '127.00.5', '127.00.6', '127.00.7'] #Example only, need to add real IPs

        # Current wall panel to display
        self.panel = 0 # Wall 1 by default

        # Modes
        self.ternaryWallMode = True # Initial setting
        self.feedbackMode = False # Initial setting

        # Feedback defaults
        self.mic = 100 #starting vals, need to tech and set exactly
        self.hp = 0
        self.lp = 100
        self.res = 100
        self.threshold = 5
        self.packetLength = 50
        self.delayLength = 5

        # Ternary Wall Mode settings
        self.centerFreq = 440
        self.interval = 1.1 # add fractions and selection availability
        self.u_interval = 1 / self.interval
