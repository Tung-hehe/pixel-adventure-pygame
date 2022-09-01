import sys

import pygame

from level import Level

map = [
'              ',
'              ',
'              ',
' XX    XXX    ',
' XX           ',
' XXXX         ',
' XXXX       XX',
' XX    X  XXXX',
'       X  XXXX',
'  P XXXX  XXXX',
'XXXXXXXX  XXXX']

tileSize = (64, 64)
playerSize = (32, 64)

screenWidth = len(map[0]) * tileSize[0]
screenHeight = len(map) * tileSize[1]

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screenWidth,screenHeight))
clock = pygame.time.Clock()
level = Level(map, tileSize, playerSize)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill('black')
	level.update(screen)

	pygame.display.update()
	clock.tick(60)
