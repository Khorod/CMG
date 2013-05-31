"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame
import pygame.locals as pg
# Own modules
import objects
import world


DEBUG = True
# Define some colors
black    = ( 10,  10,  10)
white    = (255, 255, 255)
green    = (  0, 255,   0)
red      = (230,  10,   0)
blue     = (0,     0, 255)

screen_width = 1120
screen_height = 320

pygame.init()

pygame.display.set_caption("My Game")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

screen_size = (1120, 320)
screen = pygame.display.set_mode(screen_size)

level = world.Level(screen_size, 'level_wonly.map')

#Loop until the user clicks the close button.
done = False

# Main Program Loop
while done == False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True



    # Set the screen background
    screen.fill(white)

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT



    background, overlay_dict = level.render()
    overlays = pygame.sprite.RenderUpdates()
    for (x, y), image in overlay_dict.iteritems():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * world.MAP_TILE_WIDTH, y * world.MAP_TILE_HEIGHT - world.MAP_TILE_HEIGHT)
    screen.blit(background, (0, 0))
    overlays.draw(screen)

    level.game_objects.clear(screen, background)
    level.update_objects()

    # Handle player movement
    pressed = pygame.key.get_pressed()

    dx = pressed[pygame.K_d] - pressed[pygame.K_a]
    dy = pressed[pygame.K_s] - pressed[pygame.K_w]


    if pressed[pygame.K_w]:
        level.walk_animation(0)
    elif pressed[pygame.K_s]:
        level.walk_animation(2)
    elif pressed[pygame.K_a]:
        level.walk_animation(3)
    elif pressed[pygame.K_d]:
        level.walk_animation(1)

    if dx is 0 and dy is 0:
        level.player.animation = None
    if dx is not 0 or dy is not 0:
        if level.player.animation is None:
            level.player.animation = level.player.walk_animation()#stand_animation(level.player.direction)
    level.move_player(dx*2, dy*2)
    level.player.update(level)

    dirty = level.game_objects.draw(screen)
    overlays.draw(screen)
    pygame.display.update(dirty)

    # Get mouse position
    click = pygame.mouse.get_pressed()

    if DEBUG:
        for obj in level.game_objects:
            #pygame.draw.rect(screen, red, obj.real_rect, 2)
            int_pos = (int(obj.pos[0]), int(obj.pos[1]))
            pygame.draw.circle(screen, blue, int_pos, 2)
            try:
                scale = (world.MAP_TILE_WIDTH, world.MAP_TILE_HEIGHT)
                scaled_path = [point.dot(scale) for point in obj.path]
                #print scaled_path
                pygame.draw.lines(screen, blue, False, scaled_path, 2)
            except:
                pass

        for rect in level.wall_rects:
            pygame.draw.rect(screen, red, rect, 2)
        level.draw_nav_mesh(screen)
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Limit to 20 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()


