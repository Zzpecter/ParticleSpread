import pygame
import sys
import random
import numpy as np

# Initialization
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Corona Run')
fps = pygame.time.Clock()
pygame.font.init()

def update(renderList):
    persons = []
    viruses = []
    killIdxs = []
    idx = 0
    
    #Main update loop
    print('Objects being traced: {}'.format(len(renderList)))
    for objct in renderList:

        #Check and skip objects out of screen
        if(objct.pos[0]>800 or objct.pos[0]<0 or objct.pos[1]>600 or objct.pos[1]<0):
            killIdxs.append(idx)

        #Update Viruses
        elif(objct.isVirus()):
            objct.move()
            viruses.append(objct)
            if objct.lifeTime == 0:
                killIdxs.append(idx)

        #Update Persons
        elif(objct.isPerson()):
            newViruses = objct.update()
            for v in newViruses:
                renderList.append(v)
            persons.append(objct)
        idx += 1

    #check for collisions, aka new infections
    #for each person, check all viruses
    for p in persons:
        for v in viruses:
            d = np.sqrt(np.power((p.pos[0] - v.pos[0]), 2) + np.power((p.pos[1] - v.pos[1]), 2)) - 1
            if d <= p.radius:
                p.contractInfection()
                v.pos = [1000, 1000]  

    #no longer update objects outside of the screen
    k = np.asarray(killIdxs)
    k = -np.sort(-k)
    for i in k:
        del renderList[i]

    return renderList


def render(renderList, metricsSrfc):
    screen.fill((0,255,0))

    for objct in renderList:
        pygame.draw.circle(screen, objct.color, objct.pos, objct.radius, 0)

    screen.blit(metricsSrfc,(0,0))

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

        #each time the balll moves, a deceleration must happen

class Person(Ball):
    def __init__(self, pos, facing = 'RIGHT', color = (255, 255, 255), radius = 30, speed = [0, 0], immunity=0, infected = False):
        self.color = color
        self.radius = radius
        self.pos = pos
        self.speed = speed
        self.immunity = immunity
        self.infected = infected
        self.infectionState = 0.0 #0 to 1 multiplier
        self.timeInfected = 0 
        if (self.infected):
            self.color = (255,255,0)
        self.facing = facing

    def update(self):
        viruses = []
        if self.isInfected():
            if random.randint(1, 100) < int(self.infectionState * 100) + 1:
                viruses =self.cough()
            elif random.randint(1, 100) < int(self.infectionState * 100) + 3:
                viruses =self.sneeze()
            self.timeInfected += 1
            self.infectionState += 0.00001 #TODO: change to an exponential like function based on timeInfected

        return viruses

    def isPerson(self):
        return True

    def isInfected(self):
        return self.infected

    def contractInfection(self):
        self.infected = True
        self.color = (255,255,0)

    def cough(self):
        #wide angle, low speed, more particles
        viruses = []
        numP = random.randint(8,15)
        xSpeedM = 1
        ySpeedM = 1

        for i in range(numP):

            #check for facing
            if self.facing == 'RIGHT':
                posX = self.pos[0] + self.radius
                posY = self.pos[1]
            elif self.facing == 'LEFT':
                posX = self.pos[0] - self.radius
                posY = self.pos[1]
                xSpeedM = -1
            elif self.facing == 'UP':
                posX = self.pos[0] 
                posY = self.pos[1] - self.radius
                ySpeedM = -1
            elif self.facing == 'DOWN':
                posX = self.pos[0]
                posY = self.pos[1] + self.radius

            viruses.append(Virus(pos = [posX, posY], speed = [random.randint(1,5) * xSpeedM, random.randint(-6,6)* ySpeedM]))
        return viruses

    def sneeze(self):
        #low angle, high speed, less particles
        viruses = []
        numP = random.randint(2,9)
        xSpeedM = 1
        ySpeedM = 1

        for i in range(numP):

            #check for facing
            if self.facing == 'RIGHT':
                posX = self.pos[0] + self.radius
                posY = self.pos[1]
            elif self.facing == 'LEFT':
                posX = self.pos[0] - self.radius
                posY = self.pos[1]
                xSpeedM = -1
            elif self.facing == 'UP':
                posX = self.pos[0] 
                posY = self.pos[1] - self.radius
                ySpeedM = -1
            elif self.facing == 'DOWN':
                posX = self.pos[0]
                posY = self.pos[1] + self.radius

            viruses.append(Virus(pos = [posX, posY], speed = [random.randint(1,7) * xSpeedM, random.randint(-3,3)* ySpeedM]))
        return viruses

class Virus(Ball):
    def __init__(self, pos, color = (255, 50, 50), radius = 2, speed = [0, 0]):
        self.color = color
        self.radius = radius
        self.pos = pos
        self.lifeTime = random.randint(40, 120) #TODO: replace with more accurate data

        if speed[0] == 0 and speed[1] == 0:
            self.speed = [random.randint(1,10), random.randint(-10,10)]
        else:
            self.speed = speed

        self.trueXSpeed = speed[0] 
        self.trueYSpeed = speed[1]

    def isVirus(self):
        return True

    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

        #each time the balll moves, a deceleration must happen
        decelX = 0.8 * self.trueXSpeed  #TODO: Logarithmic or some other kind of smoother deceleration funtion.
        decelY = 0.8 * self.trueYSpeed

        self.trueXSpeed -= decelX
        self.trueYSpeed -= decelY
        self.speed[0] -= int(self.trueXSpeed)
        self.speed[1] -= int(self.trueYSpeed)

        if self.lifeTime > 0:
            self.lifeTime -= 1

if __name__ == '__main__':

    testSubject = Person(pos =  [100, 240])
    testSubject2 = Person(pos =  [500, 240], facing = 'LEFT')
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

                    newViruses = testSubject.cough()
                    for v in newViruses:
                        renderList.append(v)
                    #numP = random.randint(3,20)
                    #for i in range(numP):
                    #    renderList.append(Virus( pos = [130, 240]))
        
        renderList = update(renderList)

        #metrics
        numPersons = 0
        numInfected = 0

        for objct in renderList:
            if objct.isPerson():
                numPersons += 1
                if objct.isInfected():
                    numInfected += 1

        #Setting up to display metrics on gui
        leFont = pygame.font.SysFont('Comic Sans MS', 30)
        metricsSrfc = leFont.render('Total: {}   Infected: {}'.format(numPersons, numInfected), False, (0, 0, 0))

        render(renderList, metricsSrfc)