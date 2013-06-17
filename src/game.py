"""By Michael Cabot, Steven Laan, Richard Rozeboom"""

import pygame
import pygame.locals as pg
import time 

# Own modules
import objects
import world
import utils

DEBUG = False
DEBUG_ANGLE = False
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

#current level
level_nr = 1
#freeze when we win or lose
freeze = False
#game started after intro
game_started = False
#add a bus!, that goes left to right
level.create_bus_left_to_right((-150,100), (1130,100), 5)

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

    level.game_objects.clear(screen, background)
    if  not freeze:
        level.update_objects()

    level.mouse_control() #mouse controls, like dropping object into level
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
            level.player.animation = level.player.walk_animation()
    if not freeze:
        level.move_player(dx*2, dy*2)
    level.player.update(level)


    dirty = level.game_objects.draw(screen)
    overlays.draw(screen)
    if not freeze:
        pygame.display.update(dirty)
    
    if not game_started:
        any_key_pressed = False 
        freeze = True
        if level_nr == 1:
            any_key_pressed = level.Intro1(screen)
        if level_nr == 2:
            any_key_pressed = level.Intro2(screen)
            
            
        """
            done_reading = level.win(screen)
            if done_reading:
                done_reading = False
                time.sleep(1)
                level = world.Level(screen_size, 'level2.map')
                any_key_pressed = level.Intro2(screen)
                print "in reading loop"
                print any_key_pressed
        """        
        if any_key_pressed:
            freeze = False
            game_started = True
            any_key_pressed = False
            
    # Get mouse position
    click = pygame.mouse.get_pressed()
    
    if DEBUG:
        level.draw_nav_mesh(screen)
        for obj in level.game_objects:
            pygame.draw.rect(screen, red, obj.real_rect, 2)
            int_pos = (int(obj.pos[0]), int(obj.pos[1]))
            pygame.draw.circle(screen, blue, int_pos, 2)
           # pygame.draw.circle(screen, red, obj.final_goal, 3)

            try:
                pygame.draw.lines(screen, blue, False, obj.path, 2)
            except:
                pass

        for rect in level.wall_rects:
            pygame.draw.rect(screen, red, rect, 2)
            
    if DEBUG_ANGLE:
        for obj in level.game_objects:
            if isinstance(obj, objects.Person):
                dx = obj.move_vector[0]*obj.cone_length
                dy = obj.move_vector[1]*obj.cone_length
                angle = obj.cone_angle
                obj_pos = utils.Point(obj.real_rect.center[0],obj.real_rect.center[1])#obj.pos
                pygame.draw.line(screen, red, obj_pos , obj_pos + (dx, dy), 3) #line of direction
                dx, dy = utils.rot_vector((dx,dy),-1*angle)
                pygame.draw.line(screen, green, obj_pos , obj_pos + (dx, dy), 3) #left boundary
                dx, dy = utils.rot_vector((dx,dy), 2*angle)
                pygame.draw.line(screen, blue, obj_pos , obj_pos + (dx, dy), 3) #right boundary
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    # Limit to 60 frames per second
    clock.tick(30)
    
    if level_nr == 1:
        if not level.bus_objects:
            freeze = True
            if level.player.pos[0] < 0: # player is teleported outside window when he enters bus, dirty hack, i know..
                done_reading = level.win(screen)
                if done_reading:
                    time.sleep(0.5)
                    level_nr +=1
                    game_started = False
                    level = world.Level(screen_size, 'level2.map')
            else:
                level.lose(screen)
                
    if level_nr == 2:
        if level.lost == 1:
            freeze = True
            level.lose2(screen)
        if level.won == 1:
            freeze = True
            level.win2(screen)
            #level.won = 0  
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()


