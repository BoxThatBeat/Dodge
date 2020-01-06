#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

import pygame, os
import time
import random
import sys


#os.environ['SDL_VIDEO_CENTERED'] = '1'
os.environ['SDL_VIDEO_WINDOW_POS'] = str(735) + "," + str(22)

#### ====================================================================================================================== ####
#############                                         INITIALIZE                                                   #############
#### ====================================================================================================================== ####

ScreenSize = [800,800]
lives = 3
is_open = True

def initialize():
	''' Central Initialize function. Calls helper functions to initialize Pygame and then the game_data dictionary.
	handle_input: None
	Output: game_data Dictionary
	'''
	screen = initialize_pygame()
	pygame.display.set_caption("Dodge")
	return initialize_data(screen)

#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####

def initialize_data(screen):
    ''' Initializes the game_data dictionary. Includes: Entity Data and Logistical Data (is_open).
    Input: pygame screen
    Output: game_data Dictionary
    '''
    # Initialize game_data Dictionary
    game_data = {"screen": screen,
                "entities":[],
				'playing': True,
				'start': False}
    entities = []
    
    # Generate 'Ball' Entities
	# range (random.randint(3, 6))
    for i in range(22):
        entities.append({'type': 'ball',
                         'location': [random.randint(10, 790), random.randint(0, 300)],
                         'velocity': [random.randint(2, 3), random.randint(4,5)],
						 'color': (random.randint(0,200),random.randint(0,200),random.randint(0,200)),
						 'radius': random.randint(6,12)}) #norm rad = 12
        
    # Generate 'Paddle' Entity
    entities.append({'type': 'paddle',
                     'location': [300, 780],
                     'velocity': 10,
                     'size': [50, 20],
                     'color': (0, 0, 0),
                     'current_action': 'NA'})
    game_data["entities"] = entities
    return game_data

def initialize_pygame():
    ''' Initializes Pygame.
    Input: None
    Output: pygame screen
    '''
    pygame.init()
    pygame.key.set_repeat(1, 1)
    return pygame.display.set_mode((ScreenSize[0],ScreenSize[1]))

#### ====================================================================================================================== ####
#############                                           handle_input                                                    #############
#### ====================================================================================================================== ####

def handle_input(game_data):
	
	global is_open
	
	events = pygame.event.get()
	for event in events:
		# Handle [x] Press
		if event.type == pygame.QUIT:
			is_open = False
			
		# Handle Key Presses
		if event.type == pygame.KEYDOWN:
		
			if event.key == pygame.K_LEFT:
				handle_key_left(game_data)
			elif event.key == pygame.K_RIGHT:
				handle_key_right(game_data)
			elif event.key == pygame.K_ESCAPE:
				handle_key_escape(game_data)
			elif event.key == pygame.K_SPACE:
				handle_key_space(game_data)

#############                                           HANDLERS                                                   #############
#### ---------------------------------------------------------------------------------------------------------------------- ####

def handle_key_space(game_data):
	
	game_data['start'] = True
	
def handle_key_left(game_data):
    
	for entity in game_data["entities"]:
        
		if entity['type'] == 'paddle':
			entity['current_action'] = 'left'
			

def handle_key_right(game_data):

	for entity in game_data["entities"]:
		
		if entity['type'] == 'paddle':
			entity['current_action'] = 'right'


def handle_key_escape(game_data):
	global is_open
	is_open = False
    
#### ====================================================================================================================== ####
#############                                            UPDATE                                                    #############
#### ====================================================================================================================== ####
    
def update(game_data):
	
	for entity in game_data["entities"]:
		if entity['type'] == 'paddle':
			posx = entity['location'][0]
			
	for entity in game_data["entities"]:
		# Handle 'Ball' Entity
		if entity['type'] == 'ball':
			update_ball(posx,game_data,entity)
			
		# Handle 'Paddle' Entity
		elif entity['type'] == 'paddle':
			update_paddle(entity)
			
			
#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####

def update_ball(posx,game_data,entity):
	
	global lives

	if entity['location'][1] >= ScreenSize[1]-20 and entity['location'][0] >= posx and entity['location'][0] <= posx + 50:
		#Add score each time the ball hits the paddle
		lives = lives -1
		entity['location'][1] = 0
		print("Lives: " + str(lives+1))
		time.sleep(.5)
		
		if lives <= 0:
			game_data['playing'] = False
			
	#Boundry collision checking
	#For x pos and velocity
	if entity['location'][0] <= 0:
		entity['velocity'][0] = entity['velocity'][0]*-1
		
	if entity['location'][0] >= ScreenSize[1]:
		entity['velocity'][0] = entity['velocity'][0]*-1
		
	#For y pos and velocity
	if entity['location'][1] <= 0:
		entity['velocity'][1] = entity['velocity'][1]*-1
		
	if entity['location'][1] >= ScreenSize[1]:
		entity['location'][1] = 0
		
	entity['location'][0] += entity['velocity'][0]
	entity['location'][1] += entity['velocity'][1]
	
	return

def update_paddle(entity):
	# Handle No Movement
	if entity['current_action'] == 'NA':
		return
	if entity['current_action'] == 'left':
		#- entity['size'][0]/12
		if not(entity['location'][0]  < 0):

			entity['location'][0] -= entity['velocity']
			
	if entity['current_action'] == 'right':
		if not(entity['location'][0] + entity['size'][0] > ScreenSize[0]):
	
			entity['location'][0] += entity['velocity']
		
#### ====================================================================================================================== ####
#############                                            RENDER                                                    #############
#### ====================================================================================================================== ####

def render(game_data):
    ''' Central Render function. Calls helper functions to render various views.
    Input: game_data Dictionary
    Output: None
    '''
    render_raw_data(game_data)
    render_pygame(game_data)

#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####

def render_raw_data(game_data):
    ''' Please replace this and the return with your code. '''
    return

def render_pygame(game_data):
	''' Please replace this and the return with your code. '''
	#print(game_data)
	#print("\n")
	
	localscreen = game_data['screen']
	
	localscreen.fill((220,220,220))
	
	for entity in game_data["entities"]:
        
		if entity['type'] == 'ball':
			
			pygame.draw.circle(localscreen,entity['color'],entity['location'],entity['radius'])
            
		elif entity['type'] == 'paddle':
			
			pygame.draw.rect(localscreen,entity['color'],[entity['location'][0],entity['location'][1],entity['size'][0],entity['size'][1]])
			
	#localscreen.blit(text, textrect)
	
	pygame.display.update()
	return
	
def high(listOfScores, score):
	max = 0
	
	for score in listOfScores:
		if score > max:
			max = score
	return max

"""	
class Menu(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("dodge_pic.png")    
		self.rect = self.image.get_rect()
"""
		
#### ====================================================================================================================== ####
#############                                             MAIN                                                     #############
#### ====================================================================================================================== ####

def main():
	''' Main function of script - calls all central functions above via a Game Loop code structure.
	Input: None
	Output: None
	'''
	
	score = 0
	global lives
	listOfScores = []
	highScore = 0
	
	check2 = False
	while check2 == False:
		name = input("What is your name?: ")
		
		if len(name) > 0:
			check2 = True
			
	#later maybe take this name and write to a file the best score the player achieved
	while is_open:
				
		# Initialize Data and Pygame
		game_data = initialize()
		
		clock = pygame.time.Clock()
		# Begin Central Game Loop
		print("press Space to start")
		
		localscreen1 = game_data['screen']
		menu = pygame.image.load("dodge_pic.png").convert()
		localscreen1.blit(menu, (0,0))
		pygame.display.update()	
		
		#menu = pygame.sprite.RenderPlain(menu) 
		#menu.update() 
		#menu.draw()
		
		pygame.mixer.init()
		#pygame.mixer.music.volume(0.2)
		pygame.mixer.music.load("DodgeMusic.mp3")
		
		
		#basicfont = pygame.font.sysFont(None,48)
		#text = basicfont.render('Score: ', True, (0,0,0), (255,255,255))
		
		playMusic = True
		
		while game_data['playing']:
			
			for entity in game_data["entities"]:
			
				if entity['type'] == 'paddle':
					entity['current_action'] = 'NA'
					
			handle_input(game_data)
		
			
			if game_data['start']:
				
				if playMusic == True:
					pygame.mixer.music.play(-1)
					playMusic = False
				
				update(game_data)
				render(game_data)
				time.sleep(0.01) # Small Time delay to slow down frames per second
				score += 1
				clock.tick(144)
			
			# Exit Pygame and Python
			if not is_open:
				print(name + ", you're highscore this playthrough was: " + str(highScore) + " points")
				pygame.quit()
				sys.exit()
				
			
		pygame.mixer.music.stop()
		 
		print("Score: " + str(score))
		listOfScores.append(score)
		highScore = high(listOfScores, score)
		print("HighScore: " + str(highScore))
		
		#Game Over reseting vars
		lives = 3
		score = 0
		
		localscreen2 = game_data['screen']
		over = pygame.image.load("dodge_gameover.png").convert()
		localscreen2.blit(over, (0,0))
		pygame.display.update()
		time.sleep(2)
		
	
if __name__ == "__main__":
		main()
		