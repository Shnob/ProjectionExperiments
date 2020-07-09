import pygame
import numpy as np
from random import random
import sys

ORTHO = False
RANDDELS = False
TIMEDELS = False

size = (1600, 800)
scl = 3 / (100 * ORTHO + 1)
fullDist = 3

spd = 0.03
maxSpd = 0.003

angles = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
]

delAngles = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0
]

centerMatrix = np.matrix([[250], [250], [250]])

pygame.init()
pygame.display.set_caption('5D to 4D to 3D to 2D Projection')
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pointCol = (255, 255, 255)
lineCol = (255, 255, 255)

def mapp(n, A, B, C, D):
    return (n-A)/(B-A) * (D-C) + C

if RANDDELS:
    for i in range(len(delAngles)):
        delAngles[i] = mapp(random(), 0, 1, -1, 1)

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

def showObject(obj, orig, offset):
    if orig['type'] == 0:
        def dist(a, b):
            return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2+(a[3]-b[3])**2+(a[4]-b[4])**2)
        for i in range(len(obj)):
            point((obj[i][0] * size[1] * scl + offset[0], obj[i][1] * size[1] * scl + offset[1]))

            
            curr = orig['verts'][i]
            for other in range(len(orig['verts'])):
                if dist(curr, orig['verts'][other]) <= orig['conn']:
                    line((obj[i][0] * size[1] * scl + offset[0], obj[i][1] * size[1] * scl + offset[1]), (obj[other][0] * size[1] * scl + offset[0], obj[other][1] * size[1] * scl + offset[1]))
    elif orig['type'] == 1:
        for i in range(len(obj)):
            sphere(obj[i], 0)
        

def draw():
    bg()

    projectAndDraw(penteract, (size[0]/4, size[1]/2))
    projectAndDraw(penteract, (size[0]*3/4, size[1]/2))

def projectObject5Dto4D(obj, offset):
    newObj = []
    for vert in obj:
        distance = fullDist

        s = np.sin
        c = np.cos
        a = angles

        rots = [
            np.matrix( [[c(a[0]), -s(a[0]), 0, 0, 0], [s(a[0]), c(a[0]), 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]] ),   # XY
            np.matrix( [[c(a[1]), 0, -s(a[1]), 0, 0], [0, 1, 0, 0, 0], [s(a[1]), 0, c(a[1]), 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]] ),   # XZ
            np.matrix( [[c(a[2]), 0, 0, -s(a[2]), 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [s(a[2]), 0, 0, c(a[2]), 0], [0, 0, 0, 0, 1]] ),   # XW
            np.matrix( [[c(a[3]), 0, 0, 0, -s(a[3])], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [s(a[3]), 0, 0, 0, c(a[3])]] ),   # XV
            np.matrix( [[1, 0, 0, 0, 0], [0, c(a[4]), -s(a[4]), 0, 0], [0, s(a[4]), c(a[4]), 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]] ),   # YZ
            np.matrix( [[1, 0, 0, 0, 0], [0, c(a[5]), 0, -s(a[5]), 0], [0, 0, 1, 0, 0], [0, s(a[5]), 0, c(a[5]), 0], [0, 0, 0, 0, 1]] ),   # YW
            np.matrix( [[1, 0, 0, 0, 0], [0, c(a[6]), 0, 0, -s(a[6])], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, s(a[6]), 0, 0, c(a[6])]] ),   # YV
            np.matrix( [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, c(a[7]), -s(a[7]), 0], [0, 0, s(a[7]), c(a[7]), 0], [0, 0, 0, 0, 1]] ),   # ZW
            np.matrix( [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, c(a[8]), 0, -s(a[8])], [0, 0, 0, 1, 0], [0, 0, s(a[8]), 0, c(a[8])]] ),   # ZV
            np.matrix( [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, c(a[9]), -s(a[9])], [0, 0, 0, s(a[9]), c(a[9])]] )    # WV
        ]

        pVert = np.matrix([ [vert[0] + offset[0]/size[0]], [vert[1] + offset[1]/size[1]], [vert[2]], [vert[3]], [vert[4]] ])
        
        for rot in rots:
            pVert = rot * pVert

        d = distance
        if not ORTHO:        
            d = 1/(distance - pVert.item(4))

        projMatrix = np.matrix([[d, 0, 0, 0, 0], [0, d, 0, 0, 0], [0, 0, d, 0, 0], [0, 0, 0, d, 0]])

        pVert = projMatrix * pVert

        newObj.append([pVert.item(0), pVert.item(1), pVert.item(2), pVert.item(3)])
    return newObj

def projectObject4Dto3D(obj, offset):
    newObj = []
    for vert in obj:
        distance = fullDist

        pVert = np.matrix([[vert[0]], [vert[1]], [vert[2]], [vert[3]]])

        d = distance
        if not ORTHO:        
            d = 1/(distance - pVert.item(3))

        projMatrix = np.matrix([[d, 0, 0, 0], [0, d, 0, 0], [0, 0, d, 0]])

        #pVert = (pVert * 300)
        pVert = projMatrix * pVert

        #newObj.append([pVert.item((0))+250, pVert.item((1))+250])
        newObj.append([pVert.item((0)), pVert.item((1)), pVert.item((2))])
    return newObj

def projectObject3Dto2D(obj, offset):
    newObj = []
    for vert in obj:
        distance = fullDist

        pVert = np.matrix([[vert[0]], [vert[1]], [vert[2]]])
        
        d = distance
        if not ORTHO:        
            d = 1/(distance - pVert.item(2))
        #mapp(vert[2], 0, 500, 0, 1)

        projMatrix = np.matrix([[d, 0, 0], [0, d, 0]])

        #pVert = (pVert * size[0] * scl)
        pVert = projMatrix * pVert

        newObj.append([pVert.item(0), pVert.item(1)])
    return newObj

def projectAndDraw(obj, pos):
    obj4D = projectObject5Dto4D(obj['verts'], pos)
    obj3D = projectObject4Dto3D(obj4D, pos)
    obj2D = projectObject3Dto2D(obj3D, pos)

    showObject(obj2D, obj, pos)

h = 1
l = -1
"""
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
"""

penteract = {
    'type' : 0,
    'conn' : 2,
    'verts' : [
        [l, l, l, l, l],
        [l, l, l, l, h],
        [l, l, l, h, l],
        [l, l, l, h, h],
        [l, l, h, l, l],
        [l, l, h, l, h],
        [l, l, h, h, l],
        [l, l, h, h, h],
        [l, h, l, l, l],
        [l, h, l, l, h],
        [l, h, l, h, l],
        [l, h, l, h, h],
        [l, h, h, l, l],
        [l, h, h, l, h],
        [l, h, h, h, l],
        [l, h, h, h, h],
        [h, l, l, l, l],
        [h, l, l, l, h],
        [h, l, l, h, l],
        [h, l, l, h, h],
        [h, l, h, l, l],
        [h, l, h, l, h],
        [h, l, h, h, l],
        [h, l, h, h, h],
        [h, h, l, l, l],
        [h, h, l, l, h],
        [h, h, l, h, l],
        [h, h, l, h, h],
        [h, h, h, l, l],
        [h, h, h, l, h],
        [h, h, h, h, l],
        [h, h, h, h, h]
    ]
}

while True:
    deltaTime = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw()

    if TIMEDELS:
        for i in range(len(delAngles)):
            delAngles[i] += np.clip(mapp(random(), 0, 1, -spd, spd), -1, 1)
            angles[i] += delAngles[i] * maxSpd

    pygame.display.update()