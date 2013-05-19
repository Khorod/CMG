"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame
import copy
# Own imports
import objects
import utils
import world


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

screen = pygame.display.set_mode((424, 320))

level = world.Level()
level.load_file('level.map')

SPRITE_CACHE = world.TileCache(32, 32)
game_objects = pygame.sprite.RenderUpdates()
for pos, tile in level.items.iteritems():
    sprite = objects.GameObject((pos[0] * world.MAP_TILE_WIDTH, pos[1] *
        world.MAP_TILE_HEIGHT), SPRITE_CACHE[tile["sprite"]])
    game_objects.add(sprite)

# Create a player
player = objects.Player((5, 5), SPRITE_CACHE[tile["sprite"]])
game_objects.add(player)

non_player_objects = copy.deepcopy(game_objects)
non_player_objects.remove(player)
    
clock = pygame.time.Clock()

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

    dx = pressed[pygame.K_d] - pressed[pygame.K_a]
    dy = pressed[pygame.K_s] - pressed[pygame.K_w]

    if level.place_free(player, player.pos + (dx,dy)):
        player.move(dx, dy)

    # Perform the actions of each object
    for obj in game_objects:
        obj.update()
 
    # Set the screen background
    screen.fill(white)
 
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

    background, overlay_dict = level.render()
    overlays = pygame.sprite.RenderUpdates()
    for (x, y), image in overlay_dict.iteritems():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)
    screen.blit(background, (0, 0))
    overlays.draw(screen)
    
    #sprites.clear(screen, background)
    dirty = game_objects.draw(screen)
    overlays.draw(screen)
    #pygame.display.update(dirty)

    # Get mouse position
    click = pygame.mouse.get_pressed()

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
     
    # Limit to 20 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit ()


