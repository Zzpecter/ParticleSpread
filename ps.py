import pygame
import sys
import random
import numpy as np

SCREEN_SIZE = WIDTH, HEIGHT = (640, 480)

# Initialization
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Circles')
fps = pygame.time.Clock()


def update(renderList):
    for objct in renderList:
        if(objct.isVirus()):
            objct.move()


def render(renderList):
    screen.fill(BLACK)

    for objct in renderList:
        print(objct.pos)
        print(objct.speed)
        pygame.draw.circle(screen, objct.color, objct.pos, objct.radius, 0)

    pygame.display.update()
    fps.tick(10)


class Ball():
    def __init__(self, color, radius, pos,  speed):
        self.color = color
        self.radius = radius
        self.pos = pos
        self.speed = speed

    def isPerson(self):
        return False

    def isVirus(self):
        return False

    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

class Person(Ball):
    def __init__(self, pos, color = (255, 255, 255), radius = 30, speed = [0, 0], immunity=0):
        self.color = color
        self.radius = radius
        self.pos = pos
        self.speed = speed
        self.immunity = immunity

    def isPerson(self):
        return True

class Virus(Ball):
    def __init__(self, lifeTime, pos, color = (255, 50, 50), radius = 2, speed = [0, 0]):
        self.color = color
        self.radius = radius
        self.pos = pos
        self.speed = speed
        self.lifeTime = lifeTime
        self.speed = [random.randint(1,10), random.randint(-10,10)]
        self.lifeTime = lifeTime

    def isVirus(self):
        return True

if __name__ == '__main__':

    testSubject = Person(pos =  [100, 240])
    renderList = []
    renderList.append(testSubject)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    numP = random.randint(3,20)
                    for i in range(numP):
                        renderList.append(Virus(lifeTime = 10, pos = [130, 240]))
        
        update(renderList)
        render(renderList)