import pygame
import os
import random

pygame.init()

WIDTH = 800

screen = pygame.display.set_mode((WIDTH,WIDTH))

Hero = pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))
green = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
blue = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
red = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
background = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,WIDTH))

# lasers images
green_laser = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
blue_laser =  pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
yellow_laser =  pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))
red_laser =  pygame.image.load(os.path.join("assets","pixel_laser_red.png"))

enemies = []
class Laser():
	def __init__(self,x,y,image):
		self.image = image
		self.x = x
		self.y = y
		self.mask = pygame.mask.from_surface(self.image)
		
	def draw(self):
		screen.blit(self.image,(self.x,self.y))
		
	def offscreen(self):
		return not(self.y>=0 and self.y<=WIDTH)
		
	def move(self,vel):
		self.y+=vel
		
	def collision(self,obj):
		return collide(self,obj)
		
	

class Player():
	COOLDOWN = 5
	def __init__(self,x,y,health=100):
		self.x = x
		self.y = y
		self.image = Hero
		self.cooldown_counter =0
		self.lasers = []
		self.mask = pygame.mask.from_surface(self.image)
		self.health = health

	def Draw(self,screen):
		screen.blit(self.image,(self.x,self.y))
		self.healthbar(screen)
		for laser in self.lasers:
			laser.draw()
		
	def move(self):
		self.y+=1
		
	def Move(self,s):
		if s=='w':
			self.y-=3
		if s == 's':
			self.y+=3
		if s == 'a':
			self.x-=3
		if s == 'd':
			self.x+=3
			
	def cooldown(self):
		if self.cooldown_counter>=self.COOLDOWN:
			self.cooldown_counter=0
		elif self.cooldown_counter>0:
			self.cooldown_counter+=1
			
	def Shoot(self):
		if self.cooldown_counter == 0:
			laser = Laser(self.x,self.y,yellow_laser)
			self.lasers.append(laser)
		self.cooldown_counter=1
		
	def get_height(self):
		return self.image.get_height()
		
	def get_width(self):
		return self.image.get_width()
		
	def move_laser(self,vel,objs):
		self.cooldown()
		for laser in self.lasers:
			laser.move(vel)
			if laser.offscreen():
				self.lasers.remove(laser)
			
			else:
				for obj in objs:
					if laser.collision(obj):
						obj.health-=1.5
						if(obj.health<=0):
							objs.remove(obj)
							if laser in self.lasers:
								self.lasers.remove(laser)
				
			
	def healthbar(self, window):
		pygame.draw.rect(screen, (255,0,0), (self.x, self.y + self.image.get_height() + 10, self.image.get_width(), 10))
		pygame.draw.rect(screen, (0,255,0), (self.x, self.y + self.image.get_height() + 10, self.image.get_width()*(self.health/100), 10))
		

class Enemy():
	COOLDOWN =30
	color_map = {"red":(red,red_laser),"green":(green,green_laser),"blue":(blue,blue_laser)}
	def __init__(self,x,y,color,health =100):
		self.x = x
		self.y = y
		self.image,self.laser_image = self.color_map[color]
		self.mask = pygame.mask.from_surface(self.image)
		self.enemy_lasers = []
		self.cooldown_counter =0
		self.health = health
		
	def Draw(self,screen):
		screen.blit(self.image,(self.x,self.y))
		self.healthbar(screen)
		
	def move_laser(self,vel,obj):
		self.cooldown()
		for laser in self.enemy_lasers:
			laser.move(vel)
			laser.draw()
			if laser.offscreen():
				self.enemy_lasers.remove(laser)
				
			elif laser.collision(obj):
				obj.health-=1.5
				self.enemy_lasers.remove(laser)
				
			
		
	def move(self):
		self.y+=1
		
	def Shoot(self):
		if self.cooldown_counter==0:
			laser = Laser(self.x-20,self.y,self.laser_image)
			self.enemy_lasers.append(laser)
			self.cooldown_counter =1

	def get_height(self):
		return self.image.get_height()
		
	def get_width(self):
		return self.image.get_width()
		
	def cooldown(self):
		if self.cooldown_counter>=self.COOLDOWN:
			self.cooldown_counter=0
		elif self.cooldown_counter>0:
			self.cooldown_counter+=1
			
	def healthbar(self, window):
		pygame.draw.rect(screen, (255,0,0), (self.x, self.y + self.image.get_height() + 10, self.image.get_width(), 10))
		pygame.draw.rect(screen, (0,255,0), (self.x, self.y + self.image.get_height() + 10, self.image.get_width()*(self.health/100), 10))


def collide(obj1,obj2):
	offset_x = obj2.x-obj1.x
	offset_y = obj2.y -obj1.y
	return obj1.mask.overlap(obj2.mask,(offset_x,offset_y))!=None
	


def main():
	x = 350
	y = 600
	FPS = 60
	lives = 5
	space_ship = Player(x,y)
	wave_length = 5
	player_vel_laser = 5
	enemy_vel_laser = 3
	lost = False
	lost_count=0
	def Re_Draw():
		space_ship.Draw(screen)
		for enemy in enemies:
			enemy.Draw(screen)

	Run  = True
	space_ship = Player(x,y)
	while Run:
		screen.blit(background,(0,0))
		
		if lives<=0 or space_ship.health<=0:
			lost=True
			lost_count+=1
			
		if lost:
			if lost_count>FPS*3:
				Run = False
			
			else:
				continue
		
		
		if(len(enemies) == 0):
			wave_length+=5
			for i in range(wave_length):
				enemy = Enemy(random.randrange(50, WIDTH-100),random.randrange(-1500,-100),random.choice(["red","green","blue"]))
				enemies.append(enemy)
		
		
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Run = False
		
		
		keys = pygame.key.get_pressed()
		
		
		if(keys[pygame.K_w]) and space_ship.y-3>0:
			space_ship.Move('w')
		if(keys[pygame.K_a]) and space_ship.x-3>0:
			space_ship.Move('a')
		if(keys[pygame.K_s]) and space_ship.y+30+space_ship.get_height()<WIDTH:
			space_ship.Move('s')
		if(keys[pygame.K_d]) and space_ship.get_width()+space_ship.x+15<WIDTH:
			space_ship.Move('d')
			
		if keys[pygame.K_SPACE]:
			space_ship.Shoot()
			
		
		for enemy in enemies[:]:
			enemy.move()
			enemy.move_laser(enemy_vel_laser,space_ship)
			if random.randrange(0,120)==1:
				enemy.Shoot()
			
			
			if collide(enemy,space_ship):
				space_ship.health-=1.5
				enemies.remove(enemy)
			elif enemy.y+enemy.get_height()>WIDTH:
				lives-=1
				enemies.remove(enemy)
		
		space_ship.move_laser(-player_vel_laser,enemies)
		
		
		Re_Draw()
		
		pygame.display.update()
		
main()
