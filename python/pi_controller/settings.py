class Settings():
    """A class to store all settings for Sound House pi controller."""

    def __init__(self):
        """Initialize settings"""
        self.screen_width = 600 # change later when building interface window
        self.screen_height = 500
        self.bg_color = (0, 0, 0)
        self.panel_bg_color = (50, 50, 50)

        # Ports
        self.portFeedbackControl = 7400
        self.portOscControl = 10001
        self.portPingSensors = 5000
        self.portGetSensorData = 12345

        #IPs

        self.wallIPs = ['pione.local', 'pitwo.local', 'pithree.local',
                        'pifour.local', 'pifive.local', 'pisix.local',
                        'piseven.local', 'pieight.local']

        #self.wallIPs = ["192.168.1.11",
        #                "192.168.1.12",
        #                "192.168.1.13",
        #                "192.168.1.14",
        #                "192.168.1.15",
        #                "192.168.1.16",
        #                "192.168.1.17",
        #                "192.168.1.18"] # possible to use hostnames?

        # Client lists
        self.wallOSC_clients = []

        # Current wall panel to display
        self.wall_panel = 0 # Wall 1 by default

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
        self.centerFreq = 440.01 # why does 440.01 work and not 440????
        self.interval = 1.1667 # add fractions and selection availability
        self.u_interval = 1 / self.interval
