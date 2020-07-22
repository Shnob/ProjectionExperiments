from procedualRotationalMatrices import *
from procedualProjectionalMatrices import *
import numpy as np
import sys
from random import random
import pygame

size = (600, 600)

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

    print(pos)

    pos = [ int(mapp(x, -1, 1, 20, size[0] - 20)) for x in pos ]

    print(pos)

    pygame.draw.circle(screen, (255, 255, 255), pos, 2) #14

def show(obj):
    obj6 = []

    for i in range(len(obj['verts'])):
        p = []
        for j in range(len(obj['verts'][i])):
            p.append([obj['verts'][i][j]])
        obj6.append(np.matrix(p))

    print(obj6)

    obj5 = proj6.projMatList(obj6)
    obj4 = proj5.projMatList(obj5)
    obj3 = proj4.projMatList(obj4)
    obj2 = proj3.projMatList(obj3)

    for p in range(len(obj2)):
        a = (obj2[i].item(0), obj2[i].item(1))
        point(a)

def draw():
    bg()

    show(nCube)

clock = pygame.time.Clock()
while True:
    deltaTime = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw()

    for i in range(len(rots)):
        pass#deltaRot[i] = 0
    for i in range(len(rots)):
        rots[i] += deltaRot[i] * maxSpd

    pygame.display.update()

    exit()