# import libraries
import pygame
from pygame import mixer
#initialize fonts and functionalities
pygame.init()

# beatmaker display dimension
WIDTH = 1400
HEIGHT = 800
# color display
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)
# screen display settings
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('BEAT MAKER')
label_font = pygame.font.Font('freesansbold.ttf', 28) # search for other cool .ttf fonts
medium_font = pygame.font.Font('freesansbold.ttf', 22)
timer = pygame.time.Clock()

# frame rate
fps = 60
beats = 8
instruments = 6
# variables for moving the Beat Tracker
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True
# empty list developed for saving click patterns on the beat board layout--current inactive  
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
# set different beat channels
pygame.mixer.set_num_channels(instruments * 3)

# audio file loads in display-order
high_hat = mixer.Sound("sounds\kit1\hi_hat.WAV")
snare = mixer.Sound("sounds\kit1\snare.WAV")
kick = mixer.Sound("sounds\kit1\kick.WAV")
crash = mixer.Sound("sounds\kit1\crash.WAV")
clap = mixer.Sound("sounds\kit1\clap.WAV")
tom = mixer.Sound("sounds\kit1\\tom.WAV")


#%% FUNCTION --to define beats-board layout

def draw_grid(clicks, beat):
    """
    Args:
    =====
    clicked  -- empty list of patterns to be displayed 
    beat     -- total beats (8)

    Return:
    =======
    boxes   -- to display clicked boxes for music pattern

    - Layout of beatbox for defining types of beats
    - Pads for each beat to determine beat-pattern
    - Summary & information box at the bottom
    """
    # beat types column
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT-200], 5)
    # summary & info row
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT-200, WIDTH, 200], 5)
    # used for detecting movements
    boxes = [] 
    colors = [gray, white, gray]
    
    # draw partitions between beat types
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i)*100), (200, (i)*100), 3)
    
    # setup display - 6 basic beat types
    hihat_text = label_font.render('High Hat', True, white)
    screen.blit(hihat_text, (30, 30))
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

    # draw boxes for the board to set a music pattern
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green
            
            rect = pygame.draw.rect(screen, color, 
                                    [i*((WIDTH-200)//beats)+205, (j*100)+5, 
                                    ((WIDTH-200)//beats)-10, 
                                    ((HEIGHT-200)//instruments)-10], 0, 5)

            pygame.draw.rect(screen, black, 
                                    [i*((WIDTH-200)//beats)+200, (j*100), 
                                     ((WIDTH-200)//beats), 
                                     ((HEIGHT-200)//instruments)], 5, 5)
            pygame.draw.rect(screen, gold, 
                                    [i*((WIDTH-200)//beats)+200, (j*100), 
                                     ((WIDTH-200)//beats), 
                                     ((HEIGHT-200)//instruments)], 2, 5)
            boxes.append((rect, (i,j)))
    
        # draw moving-beat-tracker grid lines
        active = pygame.draw.rect(screen, blue, 
                                        [beat*((WIDTH-200)//beats)+200, 0, 
                                        ((WIDTH-200)//beats), instruments*100], 5, 3)

    return boxes


#%% FUNCTION to play notes

def play_notes():
    """
    plays audio according to notes selected in draw_grid() clicked list
    """
    # scan through range of clicked buttons
    for i in range(len(clicked)):
        # scan columns
        if clicked[i][active_beat] == 1:
            # scan rows
            if i == 0:
                high_hat.play()
            elif i == 1:
                snare.play()
            elif i == 2:
                kick.play()
            elif i == 3:
                crash.play()
            elif i == 4:
                clap.play()
            else:
                tom.play()


#%% DISPLAY settings for actions - Play/Pause, BPM, Beats

# loop to run the beats continuously
run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)

    # Play/Pause display-buttons and fonts
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT - 100))

    # BPM display - buttons and fonts
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (310, HEIGHT - 130))
    bpm_text2 = label_font.render(f"{bpm}", True, white)
    screen.blit(bpm_text2, (370, HEIGHT - 100))
    # BPM adjustment by +/- 5 - button and fonts
    bpm_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 100, 48, 48], 0, 5)
    add_bpm = medium_font.render('+5', True, white)
    sub_bpm = medium_font.render('-5', True, white)
    screen.blit(add_bpm, (520, HEIGHT - 140))
    screen.blit(sub_bpm, (520, HEIGHT - 90))

    # Beats adjustment display - button and fonts
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 180, 100], 5, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (618, HEIGHT - 130))
    beats_text2 = label_font.render(f"{beats}", True, white)
    screen.blit(beats_text2, (680, HEIGHT - 100))
    # Beats grid adjustment by +/- 1 - button and fonts
    beats_add_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
    add_beat = medium_font.render('+1', True, white)
    sub_beat = medium_font.render('-1', True, white)
    screen.blit(add_beat, (820, HEIGHT - 140))
    screen.blit(sub_beat, (820, HEIGHT - 90))


#%% EVENTS/Functionality

    # play audio once per beat
    if beat_changed:
        play_notes()
        beat_changed = False

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

        # for one-click events - Play/Pause, BPM, Beats
        # detect Play/Pause click
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos): 
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            
            # add/subtract BPM
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            
            # add/subtract Beat 
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                # automatically builds Beats grid
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                # automatically reduces Beats grid
                for i in range(len(clicked)):
                    clicked[i].pop(-1)

    beat_length = 3600 // bpm
    
    # if-else condition to move tracker 60times/min
    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True
    # shows everything on the screen
    pygame.display.flip() 
pygame.quit()
# %%
