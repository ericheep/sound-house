#graph_test.py demo version of GUI for wall sound control
#John Eagle
#Python v. 3.6
#must install pygame and python-osc packages


import pygame, argparse, time
from random import randint, randrange
from math import sqrt
import subprocess as sp

from pythonosc import osc_message_builder
from pythonosc import udp_client

#constants
CRIMSON =   (176, 23, 31)
DEEPPINK =  (255, 20, 147)
MAGENTA =   (255, 0, 255)
RED =       (255, 0, 0)
GREEN =     (0, 255, 0)
BLUE =      (0, 0, 255)
CYAN =      (0, 255, 255)
YELLOW =    (255, 255, 0)
WHITE =     (255, 255, 255)
BLACK =     (0, 0, 0)

#store these vals in a dictionary so they can be accessed by key val
positions = { 1: [0, 0], 2: [0, 0], 3: [0, 0], 4: [0, 0], 5: [0, 0], 6: [0, 0], 7: [0, 0], 8: [0, 0], "mic": [250, 250] }

#rectangle dimensions:
long = 40
short = 10
dimensions = { 1: [short, long], 2: [short, long], 3: [short, long], 4: [short, long], 5: [short, long], 6: [short, long], 7: [short, long], 8: [short, long] }

# initialize values then add method which initializes wall positions and calls distance method on each
distances = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0 }

#for wall selection via number keys
wall_keys = { 49: 1, 50: 2, 51: 3, 52: 4, 53: 5, 54: 6, 55: 7, 56: 8, 109: "mic" }

try:
    screen_size = int(input("Input screen length, in pixels, for square screen (500 default): "))
except ValueError:
    screen_size = 500

max_distance = sqrt(((screen_size ** 2) * 2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=7401,
        help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)

def update_pos(wall_num):
    print("Wall " + str(wall_num) + ": ")
    x = int(input("x: "))
    y = int(input("y: "))
    positions[wall_num] = [x, y]
    print("Updated position for Wall #" + str(wall_num) + ": " + str(positions[wall_num]))

def find_distance(wall_num):
    #position vals will be in dictionary, function will receive key to perform calculation, and normalize 0-1
    point_1 = [(positions[wall_num][0] / max_distance),
               ((positions[wall_num][1] + 20) / max_distance)]
    mic_point = [(positions["mic"][0] / max_distance),
                 (positions["mic"][1] / max_distance)]
    distances[wall_num] = round(((((point_1[0] - mic_point[0]) ** 2) +
                                  ((point_1[1] - mic_point[1]) ** 2)) ** 0.5), 2)
    print("Distance for Wall #" + str(wall_num) + ": " + str(distances[wall_num]))
    client.send_message("/wall" + str(wall_num), distances[wall_num])

def initialize():
    choice = int(input("1. Specify wall positions 2. Random distribution "))
    if choice == 1:
        for i in range(8):
            wall_num = i + 1
            update_pos(wall_num)
            find_distance(wall_num)
    elif choice == 2:
        for i in range(8):
            wall_num = i + 1
            x = randint(0, screen_size - 10)
            y = randint(0, screen_size - 40)
            positions[wall_num][0] = x
            positions[wall_num][1] = y
            find_distance(wall_num)

initialize()

pygame.init()

#open a window and set display (width, height)
size = (screen_size, screen_size)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Walls")

#Loop until the user clicks the close button.
done = False

#Used to manage how fast the screen updates
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 15, True, False)
x = "mic"
y = "mic"

line_on = False
wall_index = "mic"

#----- Main Program Loop -----
while not done:
    #--- Main event loop
    for event in pygame.event.get(): # user did something
        if event.type == pygame.QUIT: # if user clicked 'close'
            done = True # exit main program loop
            print("User asked to quit.")
        elif event.type == pygame.KEYDOWN:
            #1-8 selects wall number, 'm' selects mic, arrows move, holding L Shift reduces movement size
            if pygame.key.get_mods() == 1:  #use key mod "shift" to change movement interval
                move_size = 1
            else:
                move_size = 10
            if event.key in wall_keys:
                wall_index = wall_keys[event.key]
                if wall_index != "mic":
                    line_on = True
                elif wall_index == "mic":
                    line_on = False
            if event.key == pygame.K_r:     # 'r' rotates wall
                temp_0 = dimensions[wall_index][0]
                temp_1 = dimensions[wall_index][1]
                dimensions[wall_index][0] = temp_1
                dimensions[wall_index][1] = temp_0
            #'w, a, s, d' to control walls
            if event.key == pygame.K_a:
                positions[wall_index][0] -= move_size
            if event.key == pygame.K_d:
                positions[wall_index][0] += move_size
            if event.key == pygame.K_w:
                positions[wall_index][1] -= move_size
            if event.key == pygame.K_s:
                positions[wall_index][1] += move_size
            #Arrow keys to control mic
            if event.key == pygame.K_LEFT:
                positions['mic'][0] -= move_size
            if event.key == pygame.K_RIGHT:
                positions['mic'][0] += move_size
            if event.key == pygame.K_UP:
                positions['mic'][1] -= move_size
            if event.key == pygame.K_DOWN:
                positions['mic'][1] += move_size
        elif event.type == pygame.KEYUP:
            sp.call('clear', shell=True)
            for wall in range(8):
                wall = wall + 1
                find_distance(wall)
            #print(distances)
                #pygame.display.update()
        #elif event.type == pygame.MOUSEBUTTONDOWN:
            #print("User pressed a mouse button")


    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)

    # --- Drawing code should go here
    #circle = mic position
    pygame.draw.circle(screen, GREEN, (positions['mic'][0], positions['mic'][1]), 10, 0)

    #walls 1-8
    pygame.draw.rect(screen, RED, (positions[1][0], positions[1][1], dimensions[1][0], dimensions[1][1]), 0)
    pygame.draw.rect(screen, RED, (positions[2][0], positions[2][1], dimensions[2][0], dimensions[2][1]), 0)
    pygame.draw.rect(screen, RED, (positions[3][0], positions[3][1], dimensions[3][0], dimensions[3][1]), 0)
    pygame.draw.rect(screen, RED, (positions[4][0], positions[4][1], dimensions[4][0], dimensions[4][1]), 0)
    pygame.draw.rect(screen, RED, (positions[5][0], positions[5][1], dimensions[5][0], dimensions[5][1]), 0)
    pygame.draw.rect(screen, RED, (positions[6][0], positions[6][1], dimensions[6][0], dimensions[6][1]), 0)
    pygame.draw.rect(screen, RED, (positions[7][0], positions[7][1], dimensions[7][0], dimensions[7][1]), 0)
    pygame.draw.rect(screen, RED, (positions[8][0], positions[8][1], dimensions[8][0], dimensions[8][1]), 0)



    if line_on == True:
        pygame.draw.line(screen, WHITE, (positions['mic'][0], positions['mic'][1]), (positions[wall_index][0] + 5, positions[wall_index][1] + 20), 2)

    #labels:

    mic_label = font.render("m", True, BLACK)
    screen.blit(mic_label, [positions["mic"][0] - 7, positions["mic"][1] - 9])
    for wall in range(len(positions) - 1):
        wall = wall + 1
        wall_label = str(wall)
        #text = "text" + str(wall)
        text = font.render(wall_label, True, WHITE)
        screen.blit(text, [positions[wall][0] + 1, positions[wall][1] + 10])

    # --- Update the screen with what we've drawn
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

#Close the window and quit
pygame.quit()
