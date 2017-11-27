import pygame

class Settings():
    """A class to store all settings for Sound House pi controller."""

    def __init__(self):
        """Initialize settings"""
        self.screen_width = 1200 # change later when building interface window
        self.screen_height = 600
        self.bg_color = (0, 0, 0)
        self.panel_bg_color = (50, 50, 50)

        # Ports
        self.portFeedbackControl = 7400 # local to sender.ck
        self.portOscControl = 10001 # also for playback control, send to pi's directly
        self.portPingSensors = 5000  # ping pi's
        self.portGetSensorData = 12345 # receive from pi's
        self.portVideo = 10002 # to video

        #IPs
        self.localIP = '127.0.0.1' # local IP
        self.wallIPs = ['pione.local', 'pitwo.local', 'pithree.local',
                        'pifour.local', 'pifive.local', 'pisix.local',
                        'piseven.local', 'pieight.local']

        self.videoIP = 'John-Eagle-MBP.local' # enter video hostname here

        # Client lists
        self.senderCK_client = 0 # initialize variable
        self.wallOsc_clients = [] # initialize list
        self.video_client = 0 # initialize variable

        # Current wall panel to display
        self.wall_panel = 0 # Wall 1 by default
        # Current selected puppet
        self.puppet = 0 # P1 by default

        self.PB_EVENT = pygame.USEREVENT
        self.bpm_ms = 1000 # BPM converted to ms interval
        self.count = 0

        # Network status
        self.networkOn = False # when off, in 'dev' mode and sends things locally or not at all

        # Modes - all off to start
        self.ternaryWallMode = False
        self.feedbackMode = False
        self.playbackMode = False
        self.sensorTuningMode = False

        self.bandpass = False

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
        self.interval = 1.1667 # add fractions and selection availability, make control for this, a series of fractions? 7?
        self.u_interval = 1 / self.interval
        self.ternary_chain = [0, 0, 0, 0, 0, 0, 0] # initial vals

        # Wall Map settings
        self.mapping = False # Turn mapping on or off
        self.wall_speed_factor = 1