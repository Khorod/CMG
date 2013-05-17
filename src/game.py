"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame

# Own imports
import objects
import utils

# Define some colors
black    = ( 10,  10,  10)
white    = (255, 255, 255)
green    = (  0, 255,   0)
red      = (230,  10,   0)
 
pygame.init()
  
# Set the height and width of the screen
size=[400, 400]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")
 
#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# List that contains every game object
game_objects = []

# Create a player
player = objects.Player(50,50)
game_objects.append(player)

# Main Program Loop
while done == False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    # Handle player movement
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_a] and player.pos.x > 0:
        player.pos -= (1,0)
    if pressed[pygame.K_d] and player.pos.x < size[0]:
        player.pos += (1,0)
    if pressed[pygame.K_w] and player.pos.y > 0:
        player.pos -= (0,1)
    if pressed[pygame.K_s] and player.pos.y < size[1]:
        player.pos += (0,1)

    # Perform the actions of each object
    for obj in game_objects:
        obj.step()
 
    # Set the screen background
    screen.fill(white)
 
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

    # Get mouse position
    click = pygame.mouse.get_pressed()

    for obj in game_objects:
        obj.draw(screen)

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
     
    # Limit to 20 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()
