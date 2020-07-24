from procedualRotationalMatrices import *
from procedualProjectionalMatrices import *
import numpy as np
import sys
from random import random
import pygame
from math import sqrt

pCol = (255, 255, 255)
lCol = (255, 255, 255)

size = (600, 600)
KB = False
scl = 18

pygame.init()
pygame.display.set_caption('6D')
screen = pygame.display.set_mode(size)

dist = 3

rotMat = RotMatsN(6)

proj6 = ProjMatN(6, dist)
proj5 = ProjMatN(5, dist)
proj4 = ProjMatN(4, dist)
proj3 = ProjMatN(3, dist)

rots = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
deltaRot = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in range(len(deltaRot)):
    deltaRot[i] = random() * 2 - 1

maxSpd = 0.02

for i in range(len(deltaRot)):
    deltaRot[i] = random() * 2 - 1

nCube = {
    'conn' : 2,
    'verts' : []
}

for x in range(2):
    for y in range(2):
        for z in range(2):
            for w in range(2):
                for v in range(2):
                    for u in range(2):
                        nCube['verts'].append([int(x * 2 - 1), int(y * 2 - 1), int(z * 2 - 1), int(w * 2 - 1), int(v * 2 - 1), int(u * 2 - 1)])

def mapp(n, A, B, C, D):
    return (n-A)/(B-A) * (D-C) + C

def bg():
    screen.fill((0, 0, 0))

def point(pos):

    #print(pos)

    pos = [ int(mapp(x, -1 / scl, 1 / scl, 0, size[0])) for x in pos ]

    #print(pos)

    pygame.draw.circle(screen, pCol, pos, 2) #14

def line(pos1, pos2):
    pos1 = [ int(mapp(x, -1 / scl, 1 / scl, 0, size[0])) for x in pos1 ]
    pos2 = [ int(mapp(x, -1 / scl, 1 / scl, 0, size[0])) for x in pos2 ]

    pygame.draw.line(screen, lCol, pos1, pos2, 1)

def show(obj):
    obj6 = []

    for i in range(len(obj['verts'])):
        p = []
        for j in range(len(obj['verts'][i])):
            p.append([obj['verts'][i][j]])
        obj6.append(np.matrix(p))

    obj6 = rotMat.rotMatList(obj6, rots)

    obj5 = proj6.projMatList(obj6)
    obj4 = proj5.projMatList(obj5)
    obj3 = proj4.projMatList(obj4)
    obj2 = proj3.projMatList(obj3)

    dist = lambda a , b : sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2 + (a[3] - b[3])**2 + (a[4] - b[4])**2 + (a[5] - b[5])**2)

    for p in range(len(obj2)):
        a = (obj2[p].item(0), obj2[p].item(1))
        #point(a)
        a6 = (obj['verts'][p][0], obj['verts'][p][1], obj['verts'][p][2], obj['verts'][p][3], obj['verts'][p][4], obj['verts'][p][5])
        for e in range(len(obj['verts'])):
            b6 = (obj['verts'][e][0], obj['verts'][e][1], obj['verts'][e][2], obj['verts'][e][3], obj['verts'][e][4], obj['verts'][e][5])
            if p != e and dist(a6, b6) <= 2:
                b = (obj2[e].item(0), obj2[e].item(1))
                line(a, b)

def draw():
    bg()

    show(nCube)

    cube = {
        'verts' : [
            [-1, -1, -1],
            [-1, -1, 1],
            [-1, 1, -1],
            [-1, 1, 1],
            [1, -1, -1],
            [1, -1, 1],
            [1, 1, -1],
            [1, 1, 1],
        ]
    }

    #show(cube)

clock = pygame.time.Clock()
while True:
    deltaTime = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw()

    if KB:
        p = lambda x : 1 if pygame.key.get_pressed()[x[0]] else -1 if pygame.key.get_pressed()[x[1]] else 0
        deltaRot[0] = p((pygame.K_1, pygame.K_2))
        deltaRot[1] = p((pygame.K_3, pygame.K_4))
        deltaRot[2] = p((pygame.K_5, pygame.K_6))
        deltaRot[3] = p((pygame.K_7, pygame.K_8))
        deltaRot[4] = p((pygame.K_9, pygame.K_0))
        deltaRot[5] = p((pygame.K_q, pygame.K_w))
        deltaRot[6] = p((pygame.K_e, pygame.K_r))
        deltaRot[7] = p((pygame.K_t, pygame.K_y))
        deltaRot[8] = p((pygame.K_u, pygame.K_i))
        deltaRot[9] = p((pygame.K_o, pygame.K_p))
        deltaRot[10] = p((pygame.K_a, pygame.K_s))
        deltaRot[11] = p((pygame.K_d, pygame.K_f))
        deltaRot[12] = p((pygame.K_g, pygame.K_h))
        deltaRot[13] = p((pygame.K_j, pygame.K_k))
        deltaRot[14] = p((pygame.K_z, pygame.K_x))
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            for i in range(len(rots)):
                rots[i] = 0
    if pygame.key.get_pressed()[pygame.K_m]:
        pygame.image.save(screen, "screenshot.jpeg")

    for i in range(len(rots)):
        pass#deltaRot[i] = 0
    for i in range(len(rots)):
        rots[i] += deltaRot[i] * maxSpd

    pygame.display.update()

    #exit()