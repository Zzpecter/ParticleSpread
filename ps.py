import pygame
import sys
import random
import numpy as np


# Initialization
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Circles')
fps = pygame.time.Clock()


def update(renderList):
    persons = []
    viruses = []
    for objct in renderList:
        if(objct.isVirus()):
            objct.move()
            viruses.append(objct)
        elif(objct.isPerson()):
            persons.append(objct)

    #check for collisions, aka new infections
    #for each person, check all viruses
    for p in persons:
        for v in viruses:
            d = np.sqrt(np.power((p.pos[0] - v.pos[0]), 2) + np.power((p.pos[1] - v.pos[1]), 2)) - 1
            if d <= p.radius:
                p.contractInfection()  


def render(renderList):
    screen.fill((0,0,0))

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
    def __init__(self, pos, color = (255, 255, 255), radius = 30, speed = [0, 0], immunity=0, infected = False):
        self.color = color
        self.radius = radius
        self.pos = pos
        self.speed = speed
        self.immunity = immunity
        self.infected = infected
        if (self.infected):
            self.color = (255,255,0)

    def isPerson(self):
        return True

    def isInfected(self):
        return self.infected

    def contractInfection(self):
        self.infected = True
        self.color = (255,255,0)

class Virus(Ball):
    def __init__(self, lifeTime, pos, color = (255, 50, 50), radius = 2, speed = [0, 0]):
        self.color = color
        self.radius = radius
        self.pos = pos
        self.speed = speed
        self.lifeTime = lifeTime
        self.speed = [random.randint(1,10), random.randint(-10,10)]

    def isVirus(self):
        return True



if __name__ == '__main__':

    testSubject = Person(pos =  [100, 240])
    testSubject2 = Person(pos =  [500, 240])
    renderList = []
    renderList.append(testSubject)
    renderList.append(testSubject2)

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