import pygame
import sys
import random
import numpy as np

SCREEN_SIZE = WIDTH, HEIGHT = (640, 480)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
personRadius = 30
virusRadius = 3

# Initialization
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Circles')
fps = pygame.time.Clock()
paused = False
spread = False


xFactors = random.sample(range(1, 11), 10)
yFactors = random.sample(range(-10, 10), 10)

virusBalls = []
# Ball setup
personPos = [100, 240]
virusStartPos = [100 + personRadius, 240]


def update():
    #list of x and y factors 
    for i in range(0,9):
        print(virusBalls[i][0])
        print(xFactors[i])
        virusBalls[i][0] += xFactors[i]
        virusBalls[i][1] += yFactors[i]


def render():
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, personPos, personRadius, 0)

    if spread:
        for i in range(0,9):
            pygame.draw.circle(screen, RED, virusBalls[i], virusRadius, 0)

    pygame.display.update()
    fps.tick(6)

def Spread():
    for i in range(0,10):
        virusBalls.insert(0,virusStartPos)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                spread = True
                Spread()
    if not paused:
        if spread:
            update()
        render()
