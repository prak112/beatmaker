# import libraries
import typing
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
red = (255, 0, 0)
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
clicked_beats = [[-1 for _ in range(beats)] for _ in range(instruments)]
# instrument active list
active_instruments = [1 for _ in range(instruments)]
# set different beat channels
pygame.mixer.set_num_channels(instruments * 3)

# save-load menus
save_menu = False
beat_name = ''
typing = False
load_menu = False
# read and upload saved file
saved_beats = []
saved_file = open('code\saved_beats.txt', 'r')
for line in saved_file:
    saved_beats.append(line)



# load audio files
high_hat = mixer.Sound("sounds\kit1\hi_hat.WAV")
snare = mixer.Sound("sounds\kit1\snare.WAV")
kick = mixer.Sound("sounds\kit1\kick.WAV")
crash = mixer.Sound("sounds\kit1\crash.WAV")
clap = mixer.Sound("sounds\kit1\clap.WAV")
tom = mixer.Sound("sounds\kit1\\tom.WAV")


#%% FUNCTION --to define beats-board layout

def draw_grid(clicks, beat, actives):
    """
    Args:
    =====
    clicked_beats  -- empty list of patterns to be displayed 
    beat           -- total beats (8)
    actives        -- list of active instruments (i.e., ON/OFF)

    Return:
    =======
    boxes          -- to display clicked_beats boxes for music pattern

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
    colors = [gray, green, gray]
    
    # draw partitions between beat types
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i)*100), (200, (i)*100), 3)
    
    # setup display - 6 basic beat types and check for active instruments
    hihat_text = label_font.render('High Hat', True, colors[actives[0]])
    screen.blit(hihat_text, (30, 30))
    snare_text = label_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (30, 130))
    bass_text = label_font.render('Bass Drum', True, colors[actives[2]])
    screen.blit(bass_text, (30, 230))
    crash_text = label_font.render('Cymbal', True, colors[actives[3]])
    screen.blit(crash_text, (30, 330))    
    clap_text = label_font.render('Clap', True, colors[actives[4]])
    screen.blit(clap_text, (30, 430))
    floor_text = label_font.render('Floor Tom', True, colors[actives[5]])
    screen.blit(floor_text, (30, 530)) 

    #  Highlight Instruments OR Patterns to identify ON/OFF
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            elif active_instruments[j] == 1: 
                color = green
            else:
                color = dark_gray
            
            # draw boxes for the board to set a music pattern
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

#%% FUNCTION to display Save-Load Menus

def draw_save_menu(beat_name, typing):
    """
    Builds save menu display for saving beats

    Args:
    =====
    beat_name   --  saved file name
    typing      --  detect file name entry

    Returns:
    ========
    Display boxes for the user

    entry_rect  --  displays box to type file name  
    saving_rect --  displays save menu title and save button
    exit_rect   --  displays exit button
    """
    # basic save menu
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    title_text = label_font.render('SAVE Current Beat As...', True, blue)
    saving_rect = pygame.draw.rect(screen, gray, [440, HEIGHT-150, 400, 100], 0, 5)
    saving_text = label_font.render('Save Beat', True, blue)
    screen.blit(saving_text, (550, 680))
    screen.blit(title_text, (450, 100))

    # saving entries menu
    if typing:
        pygame.draw.rect(screen, dark_gray, [350, 250, 600, 200], 0, 5)
    entry_rect = pygame.draw.rect(screen, gray, [350, 250, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (450, 300))

    # exit button
    exit_rect =  pygame.draw.rect(screen, gray, [1150, HEIGHT - 150, 200, 100], 0, 5)
    exit_text = label_font.render('Exit', True, red)
    screen.blit(exit_text, (1220, HEIGHT - 120))


    return entry_rect, saving_rect, exit_rect


def draw_load_menu():
    """
    """    
    # basic load menu
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    title_text = label_font.render('LOAD Saved Beats...', True, blue)
    loading_rect = pygame.draw.rect(screen, gray, [500, HEIGHT-150, 450, 100], 0, 5)
    loading_text = label_font.render('Load Beat', True, blue)
    screen.blit(loading_text, (640, 680))
    screen.blit(title_text, (550, 100))

    # delete beat
    delete_rect = pygame.draw.rect(screen, gray, [100, HEIGHT-150, 300, 100], 0, 5)
    delete_text = label_font.render('DELETE Beat', True, red)
    screen.blit(delete_text, (150, HEIGHT-120))

    # saved entries
    saved_entry_rect = pygame.draw.rect(screen, gray, [150, 200, 1100, 400], 5, 5)

    # exit button
    exit_rect =  pygame.draw.rect(screen, gray, [1150, HEIGHT - 150, 200, 100], 0, 5)
    exit_text = label_font.render('Exit', True, red)
    screen.blit(exit_text, (1220, HEIGHT - 120))

    return loading_rect, delete_rect, saved_entry_rect, exit_rect


#%% FUNCTION to play notes

def play_notes():
    """
    plays audio according to notes selected in draw_grid() clicked_beats list
    """
    # scan through range of clicked_beats buttons
    for i in range(len(clicked_beats)):
        # scan columns
        if clicked_beats[i][active_beat] == 1 and active_instruments[i] == 1:
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


#%% DISPLAY settings for actions - 
# Play/Pause, BPM, Beats Grid, Instruments ON/OFF, Save, Load & Clear 

# loop to run the beats continuously
run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked_beats, active_beat, active_instruments)

    # Play/Pause display-buttons and fonts
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, green)
    else:
        play_text2 = medium_font.render('Paused', True, red)
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

    # Beats Grid adjustment display - button and fonts
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 180, 100], 5, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (618, HEIGHT - 130))
    beats_text2 = label_font.render(f"{beats}", True, white)
    screen.blit(beats_text2, (680, HEIGHT - 100))
    # Beats Grid adjustment by +/- 1 - button and fonts
    beats_add_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
    add_beat = medium_font.render('+1', True, white)
    sub_beat = medium_font.render('-1', True, white)
    screen.blit(add_beat, (820, HEIGHT - 140))
    screen.blit(sub_beat, (820, HEIGHT - 90))

    # Instrument ON/OFF (No Display, only for EVENT functionality to display ON/OFF)
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i*100), (200, 100))
        instrument_rects.append(rect)

    # Save and Load
    save_rect = pygame.draw.rect(screen, gray, [910, HEIGHT - 150, 200, 50], 0, 5)
    save_text = label_font.render('Save', True, blue)
    screen.blit(save_text, (965, HEIGHT - 140))
    load_rect = pygame.draw.rect(screen, gray, [910, HEIGHT - 95, 200, 50], 0, 5)
    load_text = label_font.render('Load', True, blue)
    screen.blit(load_text, (965, HEIGHT - 90))
    
    # Clear board
    clear_rect =  pygame.draw.rect(screen, gray, [1150, HEIGHT - 150, 200, 100], 0, 5)
    clear_text = label_font.render('Clear Board', True, red)
    screen.blit(clear_text, (1160, HEIGHT - 120))
    
    # Save-Load menus display
    if save_menu:
        entry_rect, saving_rect, exit_rect = draw_save_menu(beat_name, typing)
    if load_menu:
        loading_rect, delete_rect, saved_entry_rect, exit_rect = draw_load_menu()

#%% EVENTS/Functionality -
# Play/Pause, BPM, Beats Grid, Instruments ON/OFF, Save, Load & Clear 

    # play audio once per beat
    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        # checks for every movement/event
        if event.type == pygame.QUIT:
            run = False
        
        # detect mouse clicks on boxes used for building music pattern
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu: 
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked_beats[coords[1]][coords[0]] *= -1

        # for one-click events - Play/Pause, BPM, Beats Grid, Instruments ON/OFF
        # prevent menus covering screen
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            # detect Play/Pause click    
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
            
            # add/subtract Beats Grid
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                # automatically builds Beats grid
                for i in range(len(clicked_beats)):
                    clicked_beats[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                # automatically reduces Beats grid
                for i in range(len(clicked_beats)):
                    clicked_beats[i].pop(-1)
            
            # Clear beats
            elif clear_rect.collidepoint(event.pos):
                clicked_beats = [[-1 for _ in range(beats)] for _ in range(instruments)]

            # Save-Load buttons
            elif save_rect.collidepoint(event.pos):
                save_menu = True
                playing = False
            elif load_rect.collidepoint(event.pos):
                load_menu = True
                playing = False

        # Save menu
        elif event.type == pygame.MOUSEBUTTONUP:
            # default Save settings
            if exit_rect.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ''
                typing = False
            if entry_rect.collidepoint(event.pos):
                if typing:
                    typing = False
                elif not typing:
                    typing = True
            # Save beat_name and other information
            elif saving_rect.collidepoint(event.pos):
                with open('code\saved_beats.txt', 'w') as f:
                    saved_beats.append(f"\nname: {beat_name}, beats: {beats}, BPM: {bpm}, pattern: {clicked_beats}")
                    for i in range(len(saved_beats)):
                        f.write(str(saved_beats[i]))
                    # reset Save settings to default
                    save_menu = False
                    typing = False
                    beat_name = ''
                
        # detect and edit keyboard input
        if event.type == pygame.TEXTINPUT and typing: # type file name
            beat_name += event.text
        if event.type == pygame.KEYDOWN: # correcting file name
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing: 
               beat_name = beat_name[:-1]


        # Load menu



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
