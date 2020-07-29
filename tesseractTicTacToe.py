from procedualRotationalMatrices import *
from procedualProjectionalMatrices import *
import numpy as np
import sys
from random import random
import pygame
from math import sqrt

teamCols = [
    (0, 90, 255),
    (255, 165, 0)
]

KB = False
maxSpd = 0.005

size = (600, 600)

dist = 3
scl = 2.8

pygame.init()
pygame.display.set_caption('Tesseract TicTacToe')
screen = pygame.display.set_mode((size[0] * 2, size[1]))

game = pygame.Surface(size)
two = pygame.Surface(size)

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

for x in range(3):
    board.append([])
    for y in range(3):
        board[x].append([])
        for z in range(3):
            board[x][y].append([])
            for w in range(3):
                board[x][y][z].append((random() * 255, random() * 255, random() * 255))#-1)#int(random() * 4 - 1)) #-1

proj4 = ProjMatN(4, dist)
proj3 = ProjMatN(3, dist)
rot = RotMatsN(4)

def mapp(n, A, B, C, D):
    return (n-A)/(B-A) * (D-C) + C

def bg(side):
    side.fill((0, 0, 0))

def point(p):
    pos = p[0]

    pos = [ int(mapp(x, -1 / scl, 1 / scl, 0, size[0])) for x in pos ]

    pCol = (0, 0, 0)#(70, 70, 70)
    #pCol = (p[3][0], p[3][1], p[3][2])
    if p[3] == 0:
        pCol = teamCols[0]
    elif p[3] == 1:
        pCol = teamCols[1]
     #14
    pygame.draw.circle(game, (255, 255, 255), pos, int(p[2]*p[1]*100) + 2)
    pygame.draw.circle(game, pCol, pos, int(p[2]*p[1]*100))

def gameShow():
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

def twoShow():
    for x in range(3):
        for y in range(3):
            for z in range(3):
                for w in range(3):
                    sCol = (70, 70, 70)
                    if board[x][y][z][w] == 0:
                        sCol = teamCols[0]
                    elif board[x][y][z][w] == 1:
                        sCol = teamCols[1]
                    pygame.draw.circle(two, sCol, (int(x * size[0]/3 + z * size[0]/9 + size[0]/18), int(y * size[1]/3 + w * size[1]/9 + size[1]/18)), 20)
    lCol = (255, 255, 255)
    pygame.draw.line(two, lCol, (size[0]/3, 0), (size[0]/3, size[1]))
    pygame.draw.line(two, lCol, (2 * size[0]/3, 0), (2 * size[0]/3, size[1]))

    pygame.draw.line(two, lCol, (0, size[0]/3), (size[1], size[0]/3))
    pygame.draw.line(two, lCol, (0, 2 * size[0]/3), (size[1], 2 * size[0]/3))

def draw():
    if frame % 10 == 0:
        bg(two)
        twoShow()

    bg(game)
    gameShow()

def regClick(pos):
    x = int(mapp(pos[0], 0, size[0], 0, 3))
    z = int(mapp(pos[0], 0, size[0], 0, 9)%3)
    y = int(mapp(pos[1], 0, size[1], 0, 3))
    w = int(mapp(pos[1], 0, size[1], 0, 9)%3)
    return (x, y, z, w)

turn = 0

frame = 0
clock = pygame.time.Clock()
while True:
    deltaTime = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] < size[0]:
                p = regClick(event.pos)
                board[p[0]][p[1]][p[2]][p[3]] = turn
                turn = (turn+1)%2

    draw()

    if KB:
        p = lambda x : 1 if pygame.key.get_pressed()[x[0]] else -1 if pygame.key.get_pressed()[x[1]] else 0
        deltaRots[0] = p((pygame.K_e, pygame.K_q))
        deltaRots[1] = p((pygame.K_a, pygame.K_d))
        deltaRots[2] = p((pygame.K_w, pygame.K_s))
        deltaRots[3] = p((pygame.K_o, pygame.K_u))
        deltaRots[4] = p((pygame.K_j, pygame.K_l))
        deltaRots[5] = p((pygame.K_i, pygame.K_k))
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            for i in range(len(rots)):
                rots[i] = 0
    
    for i in range(len(rots)):
        pass#deltaRot[i] = 0
    for i in range(len(rots)):
        rots[i] += deltaRots[i] * maxSpd

    screen.blit(two, (0, 0))
    screen.blit(game, (size[0], 0))
    pygame.display.update()
    frame += 1