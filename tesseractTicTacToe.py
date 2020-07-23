from procedualRotationalMatrices import *
from procedualProjectionalMatrices import *
import numpy as np
import sys
from random import random
import pygame
from math import sqrt

KB = False
maxSpd = 0.02

size = (600, 600)

dist = 3
scl = 2.8

pygame.init()
pygame.display.set_caption('Tesseract TicTacToe')
screen = pygame.display.set_mode(size)

board = []
shape = []

for x in range(3):
    for y in range(3):
        for z in range(3):
            for w in range(3):
                shape.append((x-1.5, y-1.5, z-1.5, w-1.5))

rots = [0, 0, 0, 0, 0, 0]
deltaRots = [0, 0, 0, 0, 0, 0]

deltaRots = [ random() * 2 - 1 for i in deltaRots ]

maxSpd = 0.02

for x in range(3):
    board.append([])
    for y in range(3):
        board[x].append([])
        for z in range(3):
            board[x][y].append([])
            for w in range(3):
                board[x][y][z].append(int(random() * 4 - 1)) #-1

proj4 = ProjMatN(4, dist)
proj3 = ProjMatN(3, dist)
rot = RotMatsN(4)

def mapp(n, A, B, C, D):
    return (n-A)/(B-A) * (D-C) + C

def bg():
    screen.fill((0, 0, 0))

def point(p):
    pos = p[0]

    pos = [ int(mapp(x, -1 / scl, 1 / scl, 0, size[0])) for x in pos ]

    pCol = (255, 255, 255)
    if p[3] == 0:
        pCol = (0, 0, 255)
    elif p[3] == 1:
        pCol = (255, 0, 0)
    pygame.draw.circle(screen, pCol, pos, int(p[2]*p[1]*50)) #14

def show():
    shapeMat = []
    for x in range(3):
        for y in range(3):
            for z in range(3):
                for w in range(3):
                    p3, d4 = proj4.projMat(rot.rotMat(np.matrix([ [x-1], [y-1], [z-1], [w-1] ]), rots))
                    p2, d3 = proj3.projMat(p3)

                    p = (p2.item(0), p2.item(1))

                    #p = [ int(mapp(x, -1 / scl, 1 / scl, 0, size[0])) for x in p ]

                    shapeMat.append((p, d3, d4, board[x][y][z][w]))
    
    shapeMat.sort(key = lambda x : x[1])

    for p in shapeMat:
        point(p)

def draw():
    bg()

    show()

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
        deltaRots[0] = p((pygame.K_1, pygame.K_2))
        deltaRots[1] = p((pygame.K_3, pygame.K_4))
        deltaRots[2] = p((pygame.K_5, pygame.K_6))
        deltaRots[3] = p((pygame.K_7, pygame.K_8))
        deltaRots[4] = p((pygame.K_9, pygame.K_0))
        deltaRots[5] = p((pygame.K_q, pygame.K_w))
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            for i in range(len(rots)):
                rots[i] = 0

    
    for i in range(len(rots)):
        pass#deltaRot[i] = 0
    for i in range(len(rots)):
        rots[i] += deltaRots[i] * maxSpd
    

    pygame.display.update()