import pygame
import sys
import math

size = ((600, 600))

pygame.init()
pygame.display.set_caption('Wavy Circles')
screen = pygame.display.set_mode(size)

divs = 16
n = 0
nInc = 2 * math.pi / 1000

h = 0
hInc = 2

def bg():
    screen.fill((0, 0, 0))

def point(pos, col):
    col = pygame.Color(0)
    col.hsva = (h%360, 100, 100, 100)
    pygame.draw.circle(screen, col, [ int(x) for x in pos ], 1)

def draw():
    for x in range(divs):
        for y in range(divs):
            if x == 0 and y == 0:
                continue
            if x == 0:
                point((size[0]/divs/2*0.9 * math.cos(n * (y)) + (size[0]/divs) * (x+0.5), size[1]/divs/2*0.9 * math.sin(n * (y)) + (size[1]/divs) * (y+0.5)), (255, 255, 255))
            elif y == 0:
                point((size[0]/divs/2*0.9 * math.cos(n * (x)) + (size[0]/divs) * (x+0.5), size[1]/divs/2*0.9 * math.sin(n * (x)) + (size[1]/divs) * (y+0.5)), (255, 255, 255))
            else:
                point((size[0]/divs/2*0.9 * math.cos(n * (x)) + (size[0]/divs) * (x+0.5), size[1]/divs/2*0.9 * math.sin(n * (y)) + (size[1]/divs) * (y+0.5)), (255, 255, 255))

clock = pygame.time.Clock()
while True:
    deltaTime = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw()
    n += nInc
    h += hInc
    #print(n)

    pygame.display.update()