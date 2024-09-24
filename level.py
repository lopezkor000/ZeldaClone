import pygame as p
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon

class Level:
	def __init__(self):
		
		# Get the display surface
		self.display_surface = p.display.get_surface()
		
		# Sprite Group Setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = p.sprite.Group()
		
		# Sprite Setup
		self.create_map()
	
	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('map/map_Grass.csv'),
			'object': import_csv_layout('map/map_Objects.csv')
		}
		graphics = {
			'grass': import_folder("graphics/Grass"),
			'objects': import_folder("graphics/objects"),
		}

		for style, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x, y), [self.obstacle_sprites], 'invisble')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
		self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites, self.create_attack)
	
	def create_attack(self):
		Weapon(self.player, [self.visible_sprites])

	def run(self):
		# Update and draw the game
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		debug(self.player.status)


class YSortCameraGroup(p.sprite.Group):
	def __init__(self):
		# general setup
		super().__init__()
		self.display_surface = p.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = p.math.Vector2(100, 200)

		# creating the floor
		self.floor_surf = p.image.load('graphics/tilemap/ground.png')
		self.floot_rect = self.floor_surf.get_rect(topleft=(0,0))
	
	def custom_draw(self, player):
		# getting the offset
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height
		
		# drawing the floor
		floor_offset_pos = self.floot_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf, floor_offset_pos)

		for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)