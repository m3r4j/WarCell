import pygame
import os
import sys
import random

# Initialize all the pygame functions needed for the game
pygame.init()
pygame.font.init()
pygame.mixer.init()

font = pygame.font.SysFont(None, 40) # Create a font object, set its font-style to None (plain-text) and set the font-size to 40

# Some RGB (Red-Green-Blue) colours
white = (255, 255, 255) # Used for the background colour
red = (255, 0, 0) # The colour that is used to show the points

width, height = 800, 600 # The width and height for the screen (should be set to 800x600)

window = pygame.display.set_mode((width, height)) # The window for the game

pygame.display.set_caption('WarCell') # The title for the game

game_icon = pygame.image.load('icon.png') # The icon for the game, it is in a .png format because pygame can't read .ico

pygame.display.set_icon(game_icon) # Set it to the given game icon above

fps = 60 # This is the fps count, should be set to 60 because it runs smooth on most devices

clock = pygame.time.Clock() # The clock which sets the fps count

# The player sprites width and height
player_width = 100
player_height = 100

# Their are two sides for the player, left and right, we want to load them in as a surface object because everything in pygame is a surface object
player_right = pygame.image.load(os.path.join('sprites', 'player_right.png'))
player_left = pygame.image.load(os.path.join('sprites', 'player_left.png'))

# Resize both sprites to the given width and height (player_width, player_height)
player_right = pygame.transform.scale(player_right, (player_width, player_height))
player_left = pygame.transform.scale(player_left, (player_width, player_height))

gravity = 0.75 # This is the gravity, it pulls the player down to the lava if the player does not hold the space bar

lava_height = 120 # The height of the lava

# The lava surface object must be loaded in
lava = pygame.image.load(os.path.join('sprites', 'lava.png'))
lava = pygame.transform.scale(lava, (width, lava_height))

# The balls width and height
ball_width = 50
ball_height = 50

ball = pygame.image.load(os.path.join('sprites', 'pokemon_ball.png')) # Load in the ball (pokemon ball) as a surface object

ball = pygame.transform.scale(ball, (ball_width, ball_height)) # Set the size of the pokemon ball with given values

max_balls = 3 # The max amount of balls that generate on the screen (can be changed so more can be generated)

boulder = pygame.image.load(os.path.join('sprites', 'boulder.png')) # This is the boulder image that needs to be loaded in

# The boulders width and height
boulder_width = 100
boulder_height = 100

boulder = pygame.transform.scale(boulder, (boulder_width, boulder_height)) # Resize it to the given values above

amount_of_pts = 5 # This is the amount of points that need to be reached to start a new round (increase difficulty)

# Lava rect object which is created so that it can use the .colliderect function so if the player collides with the lava then it's game over
lava_rect = pygame.Rect(0, height - lava_height + 20, width, lava_height)

boulder_speed_add = 1 # This is the amount that the boulders speed adds by (can be changed)

player_speed_add = 0.50 # This is the amount that the players speed adds by every new round

# This class is dedicated to all the noises that come out of the game
class sounds:
	def get_ball(): # When the user captures a ball (pokemon ball)
		pygame.mixer.music.load(os.path.join('audio','get_ball.wav'))
		pygame.mixer.music.play()

	def game_over(): # When it's game over for the user
		pygame.mixer.music.load(os.path.join('audio','game_over.wav'))
		pygame.mixer.music.play()

	def a_round(): # When one round is over
		pygame.mixer.music.load(os.path.join('audio','a_round.wav'))
		pygame.mixer.music.play()

# This function generates pokemon balls
def generate_pokemon_balls(amount):
	global balls

	if random.random() < 0.01: # The likelihood of this if statement being triggered is small so that's how the auto generated balls (pokemon balls) work
		if len(balls) < max_balls:
			for i in range(amount):
				x = random.randint(1, width - 100)
				y = random.randint(100, height - lava_height - 100)
				ball_rect = pygame.Rect(x, y, ball_width, ball_height)
				balls.append(ball_rect)

# This simply draws out all of the balls with a list of balls (list of pygame.Rect objects that represent the ball)
def draw_balls(balls):
	for i in balls:
		window.blit(ball, (i)) # Blit it with the ball image, i is just the rect object which gives it the randomly generated x and y coordinates

# This function draws the points in the top left of the screen with the colour red
def draw_points(points):
	text = font.render('Points: ' + str(points), True, red)
	window.blit(text, (0, 0)) # 0, 0 is the top-left of the screen because that's where the computers x and y coordinates starts at


# The main game loop which starts everything
def game_loop():
	global balls

	scores = [] # These are all the scores, for every new round, add the score of the user onto here

	boulder_speed = 1 # This is the speed that the boulder currently goes in when you run the game

	# Center the player in the middle of the screen
	player_x = width // 2.5
	player_y = height // 3

	# Generate the boulders position
	boulder_x = random.randint(1, width - 100)
	boulder_y = -boulder_height

	points = 0 # This is the points that the user gets when they capture the pokemon balls

	started = False # If the user presses the space bar this will become true which turns on all the functionality of the game

	balls = [] # This is where all the balls (pokemon balls) rect objects are stored in for the time that it's on the screen

	current_image = player_right # The current image it's either that the user is facing the right side or the left side, this variable determines it and can be changed

	player_speed = 5 # The speed of the player when the game runs, this increases in every new round

	while True:
		clock.tick(fps) # Run this at the given fps count

		for event in pygame.event.get():
			if event.type == pygame.QUIT: # Check for the quit event (when the user presses the red close button on the window)
				pygame.quit()
				sys.exit() # Terminates the program if it's an .exe

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE: # If the space bar is pressed then that means the game has started
					started = True


		keys = pygame.key.get_pressed() # Gets all the keys that are being pressed

		window.fill(white) # Fills the screen with the white background colour
		window.blit(current_image, (player_x, player_y)) # Displays the player


		if started: # If the user has pressed the space bar this variable was triggered which means everything below would run
			if keys[pygame.K_a] and not player_x - player_speed < 0: # Goes left
				current_image = player_left
				player_x -= player_speed

			if keys[pygame.K_d] and not player_x + player_speed > width - player_width: # Goes right
				current_image = player_right
				player_x += player_speed


			if keys[pygame.K_SPACE] and not player_y - player_speed < 0: # Goes up
				player_y -= player_speed

			else:
				if player_y + player_speed * gravity < height - player_height: # Automatically pulls the user down (goes down)
					player_y += player_speed * gravity



			window.blit(boulder, (boulder_x, boulder_y)) # Display the boulder onto the screen
			boulder_y += boulder_speed # Bring it down by adding to its y axis

			player_rect = pygame.Rect(player_x, player_y, player_width, player_height) # Player rect object
			boulder_rect = pygame.Rect(boulder_x, boulder_y, boulder_width, boulder_height) # Boulder rect object

			# Checks if the player has hit the boulder or the boulder has hit the player
			if player_rect.x >= boulder_rect.left and player_rect.x <= boulder_rect.right and player_rect.y >= boulder_rect.top and player_rect.y <= boulder_rect.bottom or boulder_rect.x >= player_rect.left and boulder_rect.x <= player_rect.right and boulder_rect.y >= player_rect.top and boulder_rect.y <= player_rect.bottom:	
				sounds.game_over() # Make the game over sound effect
				game_loop() # Restart the game
			
			# Decrease the player rect objects x and y to player sound cause we need to do some checking (this doesn't effect the output on the game)
			player_rect.x -= player_speed 
			player_rect.y -= player_speed * gravity

			# Check if the user has gotten a pokemon ball (increase the point when the user captures a ball)
			for i in balls:
				if i.x >= player_rect.left and i.x <= player_rect.right and i.y >= player_rect.top and i.y <= player_rect.bottom:
					if i in balls:
						balls.remove(i)
						points += 1 # Increase the number of points by 1
						sounds.get_ball() # Make a sound whenever the user gets a ball (point)

			# Check if the player touched the lava
			if player_rect.colliderect(lava_rect):
				sounds.game_over() # Make the game over sound effect
				game_loop() # Restart the game

			# Check if the boulder has went off the screen, if so, then generate its new x axis and reset its y axis
			if boulder_y > height:
				boulder_x = random.randint(1, width - 100)
				boulder_y = -100

			# If the points is divisible by a given number then do the following
			if points % amount_of_pts == 0:
				if points != 0: # Check if it doesn't equal to zero
					if points not in scores: # Check if it's not in the records of scores
						scores.append(points) # Add it to scores
						boulder_speed += boulder_speed_add # Increase the boulder speed
						player_speed += player_speed_add # Increase the player speed
						sounds.a_round() # Make a sound effect when a new round starts

			generate_pokemon_balls(1) # Generate one pokemon ball each time in the loop
			draw_balls(balls) # If it generates then draw it onto the screen because it gets added to the balls array

		draw_points(points) # Draw the points onto the screen
		window.blit(lava, (0, height - lava_height)) # Display the lava
		pygame.display.update() # Keep updating the screen by the frames per second

game_loop() # Run the main game loop



