import pygame
import numpy as np
from random import random
import sys

ORTHO = False

size = (800, 800)
scl = 1.6 / (100 * ORTHO + 1)
fullDist = 3.2

"""
angXY = random() * np.pi * 2
angYZ = random() * np.pi * 2
angXZ = random() * np.pi * 2
angXU = random() * np.pi * 2
angYU = random() * np.pi * 2
angZU = random() * np.pi * 2
"""

angXY = 0
angYZ = 0
angXZ = 0
angXU = 0
angYU = 0
angZU = 0

spd = 0.0003
maxSpd = 0.003

centerMatrix = np.matrix([[250], [250], [250]])

pygame.init()
pygame.display.set_caption('3D to 2D Projection')
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pointCol = (255, 255, 255)
lineCol = (255, 255, 255)

def mapp(n, A, B, C, D):
    return (n-A)/(B-A) * (D-C) + C

"""
delXY = mapp(random(), 0, 1, -spd, spd)
delYZ = mapp(random(), 0, 1, -spd, spd)
delXZ = mapp(random(), 0, 1, -spd, spd)
delXU = mapp(random(), 0, 1, -spd, spd)
delYU = mapp(random(), 0, 1, -spd, spd)
delZU = mapp(random(), 0, 1, -spd, spd)
"""
delXY = 0
delYZ = 0
delXZ = 0
delXU = 0
delYU = 0
delZU = 0

def bg():
    screen.fill((0, 0, 0))

def point(pos):

    pos = [ int(x) for x in pos ]

    pygame.draw.circle(screen, pointCol, pos, 3)

def sphere(pos, team):

    pos = [ int(x) for x in pos ]

    pygame.draw.circle(screen, pointCol, pos, 10)

def line(pos1, pos2):
    pos1 = [ int(x) for x in pos1 ]
    pos2 = [ int(x) for x in pos2 ]

    pygame.draw.line(screen, lineCol, pos1, pos2, 1)

def showObject(obj, orig):
    if orig['type'] == 0:
        def dist(a, b):
            return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2+(a[3]-b[3])**2)
        for i in range(len(obj)):
            point(obj[i])

            
            curr = orig['verts'][i]
            for other in range(len(orig['verts'])):
                if dist(curr, orig['verts'][other]) <= orig['conn']:
                    line(obj[i], obj[other])
    elif orig['type'] == 1:
        for i in range(len(obj)):
            sphere(obj[i], 0)
        

def draw():
    bg()

    #projectAndDraw(fiveCell)
    projectAndDraw(hyperCube)
    #projectAndDraw(peasants)

def projectObject4Dto3D(obj):
    newObj = []
    for vert in obj:
        distance = fullDist

        s = np.sin
        c = np.cos

        rotXY = np.matrix([ [c(angXY), s(angXY), 0, 0], [-s(angXY), c(angXY), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1] ])
        rotYZ = np.matrix([ [1, 0, 0, 0], [0, c(angYZ), s(angYZ), 0], [0, -s(angYZ), c(angYZ), 0], [0, 0, 0, 1] ])
        rotXZ = np.matrix([ [c(angXZ), 0, -s(angXZ), 0], [0, 1, 0, 0], [s(angXZ), 0, c(angXZ), 0], [0, 0, 0, 1] ])
        rotXU = np.matrix([ [c(angXU), 0, 0, s(angXU)], [0, 1, 0, 0], [0, 0, 1, 0], [-s(angXU), 0, 0, c(angXU)] ])
        rotYU = np.matrix([ [1, 0, 0, 0], [0, c(angYU), 0, -s(angYU)], [0, 0, 1, 0], [0, s(angYU), 0, c(angYU)] ])
        rotZU = np.matrix([ [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, c(angZU), -s(angZU)], [0, 0, s(angZU), c(angZU)] ])

        pVert = np.matrix([[vert[0]], [vert[1]], [vert[2]], [vert[3]]])

        pVert = rotZU * (rotYU * (rotXU * (rotXZ * (rotYZ * (rotXY * pVert)))))

        d = distance
        if not ORTHO:        
            d = 1/(distance - pVert.item(3))

        projMatrix = np.matrix([[d, 0, 0, 0], [0, d, 0, 0], [0, 0, d, 0]])

        #pVert = (pVert * 300)
        pVert = projMatrix * pVert

        #newObj.append([pVert.item((0))+250, pVert.item((1))+250])
        newObj.append([pVert.item((0)), pVert.item((1)), pVert.item((2))])
    return newObj

def projectObject3Dto2D(obj):
    newObj = []
    for vert in obj:
        distance = fullDist

        pVert = np.matrix([[vert[0]], [vert[1]], [vert[2]]])
        
        d = distance
        if not ORTHO:        
            d = 1/(distance - pVert.item(2))
        #mapp(vert[2], 0, 500, 0, 1)

        projMatrix = np.matrix([[d, 0, 0], [0, d, 0]])

        pVert = (pVert * size[0] * scl)
        pVert = projMatrix * pVert

        newObj.append([pVert.item((0))+size[0]/2, pVert.item((1))+size[1]/2])
    return newObj

def projectAndDraw(obj):
    obj3D = projectObject4Dto3D(obj['verts'])
    obj2D = projectObject3Dto2D(obj3D)

    showObject(obj2D, obj)



"""
cube = [
    [l, l, l],
    [l, l, h],
    [l, h, l],
    [l, h, h],
    [h, l, l],
    [h, l, h],
    [h, h, l],
    [h, h, h]
]
"""
q = np.sqrt
fiveCell = [
    [1, 1, 1, -1/q(5)],
    [1, -1, -1, -1/q(5)],
    [-1, 1, -1, -1/q(5)],
    [-1, -1, 1, -1/q(5)],
    [0, 0, 0, q(5) - 1/q(5)]
]
del q

h = 1
l = -1
hyperCube = {
    'type' : 0,
    'conn' : 2,
    'verts' : [
        [l, l, l, l],
        [l, l, l, h],
        [l, l, h, l],
        [l, l, h, h],
        [l, h, l, l],
        [l, h, l, h],
        [l, h, h, l],
        [l, h, h, h],
        [h, l, l, l],
        [h, l, l, h],
        [h, l, h, l],
        [h, l, h, h],
        [h, h, l, l],
        [h, h, l, h],
        [h, h, h, l],
        [h, h, h, h]
    ]
}

peasants = {
    'type' : 1,
    'verts' : [
    ]
}

PSIZE = 3

for i in range(PSIZE):
    for x in range(PSIZE):
        for y in range(PSIZE):
            for z in range(PSIZE):
                for w in range(PSIZE):
                    tmp = [x, y, z, w]
                    tmp2 = []
                    for j in tmp:
                        tmp2.append(mapp(j, 0, PSIZE - 1, -1, 1))
                    peasants['verts'].append(tmp2)
                        
#print(peasants['verts'])

while True:
    deltaTime = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw()

    angXY += delXY
    angYZ += delYZ
    angXZ += delXZ
    angXU += delXU
    angYU += delYU
    angZU += delZU

    
    delXY = np.clip(delXY + mapp(random(), 0, 1, -spd, spd), -maxSpd, maxSpd)
    delYZ = np.clip(delYZ + mapp(random(), 0, 1, -spd, spd), -maxSpd, maxSpd)
    delXZ = np.clip(delXZ + mapp(random(), 0, 1, -spd, spd), -maxSpd, maxSpd)
    delXU = np.clip(delXU + mapp(random(), 0, 1, -spd, spd), -maxSpd, maxSpd)
    delYU = np.clip(delYU + mapp(random(), 0, 1, -spd, spd), -maxSpd, maxSpd)
    delZU = np.clip(delZU + mapp(random(), 0, 1, -spd, spd), -maxSpd, maxSpd)
    
    #print("{} {} {} {} {} {}".format(delXY, delYZ, delXZ, delXU, delYU, delZU))

    pygame.display.update()