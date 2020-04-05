import pygame
import sys
import random
import numpy as np

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
    def __init__(self, pos, id, facing = 'RIGHT', color = (237, 217, 210), texture = None, radius = 15, speed = [0, 0], immunity=0, infected = False, route = None):
        self.color = color
        self.radius = radius
        self.pos = pos
        self.id = id
        self.speed = speed
        self.immunity = immunity
        self.infected = infected
        self.infectionState = 0.0 #0 to 1 multiplier
        self.timeInfected = 0 
        self.route = route
        if (self.infected):
            self.color = (255,255,0)
        self.facing = facing
        self.speed = 1
        self.waitTime = 0
        self.waiting = False
        self.served = False
        self.texture = texture

    def update(self):
        viruses = []

        #Cough or sneeze if infected
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
                ySpeedM = random.randint(-1, 1)
            elif self.facing == 'LEFT':
                posX = self.pos[0] - self.radius
                posY = self.pos[1]
                xSpeedM = -1
                ySpeedM = random.randint(-1, 1)
            elif self.facing == 'UP':
                posX = self.pos[0] 
                posY = self.pos[1] - self.radius
                ySpeedM = -1
                xSpeedM = random.randint(-1, 1)
            elif self.facing == 'DOWN':
                posX = self.pos[0]
                posY = self.pos[1] + self.radius
                xSpeedM = random.randint(-1, 1)

            viruses.append(Virus(pos = [posX, posY], speed = [random.randint(4,10) * xSpeedM, random.randint(-6,6)* ySpeedM]))
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
                ySpeedM = random.randint(-1, 1)
            elif self.facing == 'LEFT':
                posX = self.pos[0] - self.radius
                posY = self.pos[1]
                ySpeedM = random.randint(-1, 1)
                xSpeedM = -1
            elif self.facing == 'UP':
                posX = self.pos[0] 
                posY = self.pos[1] - self.radius
                ySpeedM = -1
                xSpeedM = random.randint(-1, 1)
            elif self.facing == 'DOWN':
                posX = self.pos[0]
                posY = self.pos[1] + self.radius
                xSpeedM = random.randint(-1, 1)

            viruses.append(Virus(pos = [posX, posY], speed = [random.randint(8,15) * xSpeedM, random.randint(-4,4)* ySpeedM]))
        return viruses

    def move(self, direction):
        if self.route is not None:
            if not self.waiting:
                startPoint = self.pos
                nextPoint = self.route.getNextPoint()

                if direction == 'RIGHT':
                    d = np.abs(startPoint[0] - nextPoint[0])
                    if self.speed < d:
                        self.pos = [self.pos[0] + self.speed, self.pos[1]]
                    else:
                        self.pos = [self.pos[0] + d, self.pos[1]]
                        if np.abs(startPoint[1] - nextPoint[1]) == 0:
                            self.route.currentIdx += 1
                    self.facing = 'RIGHT'

                elif direction == 'LEFT':
                    d = np.abs(startPoint[0] - nextPoint[0])
                    if np.abs(self.speed) < d:
                        self.pos = [self.pos[0] - self.speed, self.pos[1]]
                    else:
                        self.pos = [self.pos[0] - d, self.pos[1]]
                        if np.abs(startPoint[1] - nextPoint[1]) == 0:
                            self.route.currentIdx += 1
                    self.facing = 'LEFT'

                elif direction == 'DOWN':
                    d = np.abs(startPoint[1] - nextPoint[1])
                    if self.speed < d:
                        self.pos = [self.pos[0], self.pos[1] + self.speed]
                    else:
                        self.pos = [self.pos[0], self.pos[1] + d]
                        if np.abs(startPoint[0] - nextPoint[0]) == 0:
                            self.route.currentIdx += 1
                    self.facing = 'DOWN'

                elif direction == 'UP':
                    d = np.abs(startPoint[1] - nextPoint[1])
                    if np.abs(self.speed) < d:
                        self.pos = [self.pos[0], self.pos[1] - self.speed]
                    else:
                        self.pos = [self.pos[0], self.pos[1] - d]
                        if np.abs(startPoint[0] - nextPoint[0]) == 0:
                            self.route.currentIdx += 1
                    self.facing = 'UP'
            else:
                self.waitTime -= 1
                print('waiting {}...'.format(self.waitTime))
                if self.waitTime == 0:
                    self.waiting = False
                    self.served = True
                    print('Served!')

    def getMoveHeading(self):
        startPoint = self.pos
        nextPoint = self.route.getNextPoint()
        direction = None

        #walk right
        if startPoint[0] < nextPoint[0]:
            direction = 'RIGHT'
        #walk left
        elif startPoint[0] > nextPoint[0]:
            direction = 'LEFT'
        #walk down
        elif startPoint[1] < nextPoint[1]:
            direction = 'DOWN'
        #walk up
        elif startPoint[1] > nextPoint[1]:
            direction = 'UP'

        return direction

    def checkCollision(self, newPos, r, safeDist):
        if np.sqrt(np.square(self.pos[0] - newPos[0]) + np.square(self.pos[1] - newPos[1])) <= (self.radius + r + safeDist):
            return True
        else:
            return False

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
        if self.trueXSpeed > 1 and self.trueYSpeed > 1: # needed for log
            decelX = np.log(self.trueXSpeed)   
            decelY = np.log(self.trueYSpeed)

            self.trueXSpeed -= decelX
            self.trueYSpeed -= decelY
            self.speed[0] = int(self.trueXSpeed)
            self.speed[1] = int(self.trueYSpeed)

        if self.lifeTime > 0:
            self.lifeTime -= 1

class Route():
    def __init__(self, wayPoints, currentIdx = 0):
        self.wayPoints = wayPoints
        self.currentIdx = currentIdx

    def getCurrentPoint(self):
        return self.wayPoints[self.currentIdx]

    def getNextPoint(self):
        return self.wayPoints[self.currentIdx + 1]

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
            #check new viruses
            newViruses = objct.update()
            for v in newViruses:
                renderList.append(v)
            persons.append(objct)

            
            
        idx += 1

    #Move all moveable persons, check collision before moving
    newPos = [0, 0]
    for p in persons:
        if p.route is not None:


            direction = p.getMoveHeading()
            if direction == 'RIGHT':
                newPos = [p.pos[0] + p.speed, p.pos[1]]
            elif direction == 'LEFT':
                newPos = [p.pos[0] - p.speed, p.pos[1]]
            elif direction == 'DOWN':
                newPos = [p.pos[0], p.pos[1] + p.speed]
            elif direction == 'UP':
                newPos = [p.pos[0], p.pos[1] - p.speed]

            #check all persons
            coll = False
            for pCheck in persons:
                if pCheck.id != p.id and pCheck.checkCollision(newPos, p.radius, safeDist = 10):
                    coll = True
                    break

            if not coll:
                p.move(direction)

            #check if the person is at the counter, if so give waitTime
            if p.pos == [770, 260] and not p.waiting and not p.served:
                p.waitTime = 100
                p.waiting = True

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

def render(renderList, metricsSrfc, backgrnd, persImg):
    screen.fill((0,255,0))
    screen.blit(backgrnd, [0, 0])

    for objct in renderList:
        if objct.isVirus():
            pygame.draw.circle(screen, objct.color, objct.pos, objct.radius, 0)
        elif objct.isPerson():
            if objct.texture is not None:


                if objct.facing == 'RIGHT':
                    angle = 270
                elif objct.facing == 'LEFT':
                    angle = 90
                elif objct.facing == 'UP':
                    angle = 0
                elif objct.facing == 'DOWN':
                    angle = 180

                auxImg = pygame.transform.rotate(persImg, angle)
                screen.blit(auxImg, objct.pos)
            else:
                pygame.draw.circle(screen, objct.color, objct.pos, objct.radius, 0)

    screen.blit(metricsSrfc,(0,0))

    pygame.display.update()
    fps.tick(10)

if __name__ == '__main__':

    bgr = pygame.image.load("./screens/backgr_Queue.bmp").convert()
    persImg = pygame.image.load('./screens/pers_young_1.png')

    queueRoute = Route(wayPoints = ([770, 260], [770, -15]))

    testSubject = Person(pos =  [600, 260], texture = persImg, id = 1, route = queueRoute)
    testSubject2 = Person(pos =  [450, 260], texture = persImg, id = 2, route = queueRoute)
    testSubject3 = Person(pos =  [390, 260], texture = persImg, id = 3, route = queueRoute)
    testSubject4 = Person(pos =  [320, 260], texture = persImg, id = 4, route = queueRoute)
    testSubject5 = Person(pos =  [250, 260], texture = persImg, id = 5, route = queueRoute)
    testSubject6 = Person(pos =  [200, 260], texture = persImg, id = 6, route = queueRoute)
    testSubject7 = Person(pos =  [100, 260], texture = persImg, id = 7, route = queueRoute)
    testSubject8 = Person(pos =  [400, 390], texture = persImg, id = 8, facing = 'UP', infected = True)
    renderList = []
    renderList.append(testSubject)
    renderList.append(testSubject2)
    renderList.append(testSubject3)
    renderList.append(testSubject4)
    renderList.append(testSubject5)
    renderList.append(testSubject6)
    renderList.append(testSubject7)
    renderList.append(testSubject8)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:

                    newViruses = testSubject8.cough()
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
        render(renderList, metricsSrfc, bgr, persImg)