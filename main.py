import pygame as p
import sys
from settings import *
from level import Level


class Game:
	def __init__(self):
		
		# Setup
		p.init()
		self.screen = p.display.set_mode((WIDTH, HEIGHT))
		p.display.set_caption('Zelda')
		self.clock = p.time.Clock()
		
		self.level = Level()
	
	def run(self):
		while True:
			for event in p.event.get():
				if event.type == p.QUIT:
					p.quit()
					sys.exit()
			
			self.screen.fill('black')
			self.level.run()
			p.display.update()
			self.clock.tick(FPS)


if __name__ == '__main__':
	game = Game()
	game.run()