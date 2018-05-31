import pygame
from fractions import Fraction

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
        self.portVideo = 1234 # to video

        #IPs
        self.myIP = '192.168.0.7' # John MBP
        self.localIP = '127.0.0.1'
        self.wallIPs = ['pione.local', 'pitwo.local', 'pithree.local',
                        'pifour.local', 'pifive.local', 'pisix.local',
                        'piseven.local', 'pieight.local']

        self.videoIP = 'isyetteki-MBP' # enter video hostname here

        # Client lists
        self.senderCK_client = 0 # initialize variable
        self.wallOsc_clients = [] # initialize list
        self.wallSensor_clients = []
        #self.video_client = '192.168.1.79' # initialize variable
        self.video_client = 0

        self.server = 0 # for receiving OSC

        # Ping interval
        self.ping_interval = 100 # interval in ms for pinging sensors
        self.PING_EVENT = pygame.USEREVENT

        # Sets all wall settings at same time
        self.set_all = False

        # Current wall panel to display
        self.wall_panel = 0 # Wall 1 by default
        self.wall_sensors = [0, 0, 0, 0, 0, 0, 0, 0] # stores most recent sensor readings
        self.wall_amps = [0, 0, 0, 0, 0, 0, 0, 0] # stores amplitude for each wall
        self.amp_high = 0.5 # need to test and set these vals
        self.amp_low = 0.2 # test this

        # Current selected puppet
        self.puppet = 0 # P1 by default

        self.PB_EVENT = pygame.USEREVENT + 1
        self.bpm_ms = 1000 # BPM converted to ms interval
        self.count = 0

        # Network status
        self.networkOn = False # when off, in 'dev' mode and sends things locally or not at all

        # keyboard entry of interval
        self.key_entry = False
        self.entry = ''

        # Modes - all off to start
        self.ternaryWallMode = False
        self.feedbackMode = False
        self.playbackMode = False
        self.sensors = False
        self.sensorTuningMode = False
        self.sendVideo = False

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
        self.centerFreq = 440.01 # why does 440.01 work and not 440???? #speaker range = 100 -18k Hz
        self.interval = Fraction(7, 6) # 1.1667 # add fractions and selection availability, make control for this, a series of fractions? 7?
        self.u_interval = Fraction(1 / self.interval)
        self.ternary_chain = [0, 0, 0, 0, 0, 0, 0] # initial vals

        self.distance_threshold = 30 # set later--for turning up sine amp.

        # Wall Map settings
        self.mapping = False # Turn mapping on or off
        self.wall_speed_factor = 1

        # testing server
        self.sending = ''
        self.save_this = 0
        self.server_thread = 0


    def parse_sensors(self, address, hostname, val): # do i need to remove self?
        wall_names = ["pione", "pitwo", "pithree", "pifour", "pifive", "pisix",
                      "piseven", "pieight"]
        print("pi: ", hostname, "val: ", val)
        if hostname in wall_names:
            wall_index = wall_names.index(hostname)
            self.wall_sensors[wall_index] = val
            print(self.wall_sensors)
"""
    def update_wall_sensors(self, address, wall_string, val):
        # gets OSC messages and converts to wall/amp info
        walls = ['pione', 'pitwo', 'pithree', 'pifour', 'pifive', 'pisix',
                 'piseven', 'pieight']
        wall_index = walls.index(wall_string)
        val = round(val, 2)
        self.wall_sensors[wall_index] = val

        if self.ternaryWallMode:
            self.set_wall_amps(self, wall_index, val)

    def set_wall_amps(self, wall_index, val):
        # takes sensor vals and determines amp
        if val > self.distance_threshold:
            self.wall_amps[wall_index] = self.amp_high
        elif val <= self.distance_threshold:
            self.wall_amps[wall_index] = self.amp_low
        print(self.wall_amps) # network function call goes here
"""