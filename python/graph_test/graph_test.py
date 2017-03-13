#graph_test.py demo version of GUI for wall sound control
#John Eagle
#Python v. 3.6
#must install pygame and python-osc packages


import pygame
from random import randint
import subprocess as sp
import argparse
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

#from pygame.locals import *
#import math
#from time import sleep
#import sys

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

# initialize values then add method which initializes wall positions and calls distance method on each
distances = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0 }

#for wall selection via number keys
wall_keys = { 49: 1, 50: 2, 51: 3, 52: 4, 53: 5, 54: 6, 55: 7, 56: 8, 109: "mic" }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=7400,
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
    #position vals will be in dictionary, function will receive key to perform calculation
    point_1 = [positions[wall_num][0], (positions[wall_num][1] + 20)]
    mic_point = [positions["mic"][0], positions["mic"][1]]
    distances[wall_num] = round(((((point_1[0] - mic_point[0]) ** 2) + ((point_1[1] - mic_point[1]) ** 2)) ** 0.5), 2)
    print("Distance for Wall #" + str(wall_num) + ": " + str(distances[wall_num]) + " pixels")
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
            x = randint(0, 490)
            y = randint(0, 460)
            positions[wall_num][0] = x
            positions[wall_num][1] = y
            find_distance(wall_num)

initialize()

pygame.init()

#open a window and set display (width, height)
size = (500, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Walls")

#Loop until the user clicks the close button.
done = False

#Used to manage how fast the screen updates
clock = pygame.time.Clock()

x = "mic"
y = "mic"

#----- Main Program Loop -----
while not done:
    #--- Main event loop
    for event in pygame.event.get(): # user did something
        if event.type == pygame.QUIT: # if user clicked 'close'
            done = True # exit main program loop
            print("User asked to quit.")
        elif event.type == pygame.KEYDOWN:
            #1-8 selects wall number, 'm' selects mic, arrows move, holding L Shift reduces movement size
            if pygame.key.get_mods() == 1:
                move_size = 1
            else:
                move_size = 10
            if event.key in wall_keys:
                x = wall_keys[event.key]
                y = wall_keys[event.key]
            #use key mod "shift" to change movement interval
            if event.key == pygame.K_LEFT:
                positions[x][0] -= move_size
            if event.key == pygame.K_RIGHT:
                positions[x][0] += move_size
            if event.key == pygame.K_UP:
                positions[y][1] -= move_size
            if event.key == pygame.K_DOWN:
                positions[y][1] += move_size
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
    screen.fill(WHITE)

    # --- Drawing code should go here
    #circle = mic position
    pygame.draw.circle(screen, GREEN, (positions['mic'][0], positions['mic'][1]), 10, 1)

    #walls 1-8
    pygame.draw.rect(screen, CRIMSON, (positions[1][0], positions[1][1], 10, 40), 1)
    pygame.draw.rect(screen, DEEPPINK, (positions[2][0], positions[2][1], 10, 40), 1)
    pygame.draw.rect(screen, MAGENTA, (positions[3][0], positions[3][1], 10, 40), 1)
    pygame.draw.rect(screen, RED, (positions[4][0], positions[4][1], 10, 40), 1)
    pygame.draw.rect(screen, BLUE, (positions[5][0], positions[5][1], 10, 40), 1)
    pygame.draw.rect(screen, CYAN, (positions[6][0], positions[6][1], 10, 40), 1)
    pygame.draw.rect(screen, YELLOW, (positions[7][0], positions[7][1], 10, 40), 1)
    pygame.draw.rect(screen, BLACK, (positions[8][0], positions[8][1], 10, 40), 1)

    # --- Update the screen with what we've drawn
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

#Close the window and quit
pygame.quit()

#updates any changes
#    pygame.display.update()


"""
    move = int(input("1. Move wall 2. Reset 3. Exit: "))
    if move == 1:
        method = int(input("1. By coordinate 2. Using Arrows "))
        wall_num = int(input("Which wall? 1-8 "))
        if method == 1:
            update_pos(wall_num)
            find_distance(wall_num)
        if method == 2:
            while 1:

    elif move == 2:
        initialize()
    elif move == 3:
        break
"""
