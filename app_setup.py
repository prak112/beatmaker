# import libraries
import pygame
from pygame import mixer

#initialize fonts and functionalities
pygame.init()

# beatmaker display dimension
width = 1400
height = 800

# color display
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)

# screen display settings
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('BEAT MAKER')
label_font = pygame.font.Font('freesansbold.ttf', 28) # search for other cool .ttf fonts

# frame rate
fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
 
# empty list developed for saving click patterns on the beat board layout--current inactive  
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]

# FUNCTION --to define beats-board layout
def draw_grid():
    """
    - Layout of beatbox for defining types of beats
    - Pads for each beat to determine beat-pattern
    - Summary & information box at the bottom
    """
    # beats column
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, height-200], 5)
    # summary & info row
    bottom_box = pygame.draw.rect(screen, gray, [0, height-200, width, 200], 5)
    boxes = [] # used for detecting movements
    colors = [gray, white, gray]

    # setup 6 basic beat types
    hiHat_text = label_font.render('High Hat', True, white)
    screen.blit(hiHat_text, (30, 30))
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30, 130))
    bass_text = label_font.render('Bass Drum', True, white)
    screen.blit(bass_text, (30, 230))
    crash_text = label_font.render('Cymbal', True, white)
    screen.blit(crash_text, (30, 330))    
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30, 430))
    floor_text = label_font.render('Floor Tom', True, white)
    screen.blit(floor_text, (30, 530)) 

    # draw partitions between beat types
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i+1)*100), (200, (i+1)*100), 2)

    # draw boxes for the board to set a music pattern
    for i in range(beats):
        for j in range(instruments):
            if clicked[j][i] == -1:
                color = gray
            else:
                color = green
            
            rect = pygame.draw.rect(screen, color, 
                                    [i*((width-200)//beats)+205, (j*100)+5, 
                                    ((width-200)//beats)-10, 
                                    ((height-200)//instruments)-10], 0, 5)

            pygame.draw.rect(screen, black, 
                                    [i*((width-200)//beats)+200, (j*100), 
                                     ((width-200)//beats), 
                                     ((height-200)//instruments)], 5, 5)
            pygame.draw.rect(screen, gold, 
                                    [i*((width-200)//beats)+200, (j*100), 
                                     ((width-200)//beats), 
                                     ((height-200)//instruments)], 2, 5)
            boxes.append((rect, (i,j)))
    
    return boxes


# start/stop the program, record/display the actions
run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid()


    for event in pygame.event.get():
        # checks for every movement/event
        if event.type == pygame.QUIT:
            run = False
        
        # detect mouse clicks on boxes used for building music pattern
        if event.type == pygame.MOUSEBUTTONDOWN: 
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1



    pygame.display.flip() # shows everything on the screen
pygame.quit()