import pygame
import numpy as np
from random import random
import sys
from procedualRotationalMatrices import *

ORTHO = False
KB = True

mousePos = None

size = (1000, 600)
scl = 0.6 / (100 * ORTHO + 1)
fullDist = 3

rotMat = RotMatsN(4)

rots = [
    0,
    0,
    0,
    0,
    0,
    0
]

deltaRot = [
    0,
    0,
    0,
    0,
    0,
    0,
]
 
for i in range(len(rots)):
    deltaRot[i] = random() * 2 - 1#*np.pi

#deltaRot[4] = 0
#deltaRot[5] = 0

maxSpd = 0.02

centerMatrix = np.matrix([[250], [250], [250]])

pygame.init()
pygame.display.set_caption('4D to 3D to 2D Projection')
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pointCol = (255, 255, 255)
lineCol = (255, 255, 255)

def mapp(n, A, B, C, D):
    return (n-A)/(B-A) * (D-C) + C

def bg():
    screen.fill((0, 0, 0))

def point(pos, dist):

    pos = [ int(x) for x in pos ]

    pygame.draw.circle(screen, pointCol, pos, int(dist * 14)) #14

def sphere(pos, team):

    pos = [ int(x) for x in pos ]

    pygame.draw.circle(screen, pointCol, pos, 10)

def line(pos1, pos2):
    pos1 = [ int(x) for x in pos1 ]
    pos2 = [ int(x) for x in pos2 ]

    pygame.draw.line(screen, lineCol, pos1, pos2, 1)

def showObject(obj, orig, dists):
    if orig['type'] == 0:
        def dist(a, b):
            return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2+(a[3]-b[3])**2)
        for i in range(len(obj)):
            point(obj[i], dists[i])

            
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
    dists = []
    for vert in obj:
        distance = fullDist

        pVert = np.matrix([[vert[0]], [vert[1]], [vert[2]], [vert[3]]])

        pVert = rotMat.rotMat(pVert, rots)

        d = distance
        if not ORTHO:        
            d = 1/(distance - pVert.item(3))
        dists.append(d)

        projMatrix = np.matrix([[d, 0, 0, 0], [0, d, 0, 0], [0, 0, d, 0]])

        #pVert = (pVert * 300)
        pVert = projMatrix * pVert

        #newObj.append([pVert.item((0))+250, pVert.item((1))+250])
        newObj.append([pVert.item((0)), pVert.item((1)), pVert.item((2))])
    return newObj, dists

ang1 = 0
ang2 = 0
ang3 = 0

'''
ang1 = random()
ang2 = random()
ang3 = random()
'''
def projectObject3Dto2D(obj, off = None):
    newObj = []
    for vert in obj:
        distance = fullDist

        s = np.sin
        c = np.cos

        pVert = np.matrix([[vert[0]], [vert[1]], [vert[2]]])
        
        r1 = np.matrix([ [c(ang1), -s(ang1), 0], [s(ang1), c(ang1), 0], [0, 0, 1] ])
        r2 = np.matrix([ [c(ang2), 0, -s(ang2)], [0, 1, 0], [s(ang2), 0, c(ang2)] ])
        r3 = np.matrix([ [1, 0, 0], [0, c(ang3), -s(ang3)], [0, s(ang3), c(ang3)] ])

        pVert = r3* (r2 * (r1 * pVert))

        if off is not None:
            pVert = pVert - off

        d = distance
        if not ORTHO:        
            d = 1/(distance - pVert.item(2))
        #mapp(vert[2], 0, 500, 0, 1)

        projMatrix = np.matrix([[d, 0, 0], [0, d, 0]])

        pVert = (pVert * size[0] * scl)
        pVert = projMatrix * pVert

        pVert = pVert - np.matrix([ [440 * off.item(0)], [0] ])

        newObj.append([pVert.item((0))+size[0]/2, pVert.item((1))+size[1]/2])
    return newObj

def projectAndDraw(obj):
    obj3D, dists = projectObject4Dto3D(obj['verts'])
    left = projectObject3Dto2D(obj3D, np.matrix([ [-0.3], [0], [0] ]))
    right = projectObject3Dto2D(obj3D, np.matrix([ [0.3], [0], [0] ]))

    showObject(left, obj, dists)
    showObject(right, obj, dists)



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
fiveCell = {
    'type' : 0,
    'conn' : 3,
    'verts' : [
        [1, 1, 1, -1/q(5)],
        [1, -1, -1, -1/q(5)],
        [-1, 1, -1, -1/q(5)],
        [-1, -1, 1, -1/q(5)],
        [0, 0, 0, q(5) - 1/q(5)]
    ]
}
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
    ],
    'dists' : []
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
    mousePos = pygame.mouse.get_pos()

    draw()

    p = lambda x : 1 if pygame.key.get_pressed()[x[0]] else -1 if pygame.key.get_pressed()[x[1]] else 0

    if KB:
        deltaRot[0] = p((pygame.K_e, pygame.K_q))
        deltaRot[1] = p((pygame.K_a, pygame.K_d))
        deltaRot[2] = p((pygame.K_w, pygame.K_s))
        deltaRot[3] = p((pygame.K_u, pygame.K_o))
        deltaRot[4] = p((pygame.K_j, pygame.K_l))
        deltaRot[5] = p((pygame.K_i, pygame.K_k))
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            for i in range(len(rots)):
                rots[i] = 0

    for i in range(len(rots)):
        pass#deltaRot[i] = 0
    for i in range(len(rots)):
        rots[i] += deltaRot[i] * maxSpd

    pygame.display.update()