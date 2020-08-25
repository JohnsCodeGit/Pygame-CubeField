from sys import exit
import pygame
import random
import pygame.freetype
from Player import *
from Obstacle import *

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
random.seed(None)

WIDTH = 1000
HEIGHT = 800

RED = (150, 0, 0)
LIGHT_RED = (255, 50, 50)
BLUE = (0, 0, 255)
GREEN = (0, 150, 0)
LIGHT_GREEN = (50, 220, 50)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CUBE_COUNT = 85
player_size = 20 

#Game state
state = 0
score = 0

player_pos = [WIDTH/2, HEIGHT - 4 * player_size]

#Create game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Create score text
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

enemy_list = []

def show_score(x, y):
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (x, y))


def make_enemy(cube_list, WIDTH):

        if len(cube_list) == 0:
            for x in range(CUBE_COUNT):
                cube = Obstacle(WIDTH)
                cube_list.append(cube)
            

def display_death_screen():
    screen.fill(BLACK)
    show_score(WIDTH/2.37, HEIGHT/2)
    death_text = font.render("YOU DIED", True, WHITE)
    screen.blit(death_text, (WIDTH/2.35, HEIGHT/2 - 50))


def check_collision(player_left_side, player_top_side, block_left_side, block_top_side, p_size, c_size):

        player_right_side = player_left_side + p_size
        player_bottom_side = player_top_side + p_size

        block_right_side = block_left_side + c_size
        block_bottom_side = block_top_side + c_size

        #Block is to the left of the player and top of block is higher than player's top
        if ((block_left_side <= player_left_side and block_right_side >= player_left_side
        and block_top_side <= player_top_side and block_bottom_side >= player_top_side and block_top_side <= player_bottom_side)

        #Block is to the right of the player and top of block is higher than player's top
        or (block_left_side <= player_right_side and block_right_side >= player_right_side
        and block_top_side >= player_top_side and block_bottom_side >= player_top_side and block_top_side <= player_bottom_side)

        #Block is to the left of the player and top of block is lower than player's top
        or (block_left_side <= player_left_side and block_right_side >= player_left_side
        and block_top_side >= player_top_side and block_bottom_side >= player_top_side and block_top_side <= player_bottom_side)

        #Block is to the right of the player and top of block is lower than player's top
        or (block_left_side <= player_right_side and block_right_side >= player_right_side
        and block_top_side <= player_top_side and block_bottom_side >= player_top_side and block_top_side <= player_bottom_side)

        #BLOCK IN PLAYER
        or (block_left_side >= player_left_side and block_right_side <= player_right_side
        and block_top_side >= player_top_side and block_bottom_side >= player_top_side and block_top_side <= player_bottom_side)

        #BLOCK IN PLAYER
        or (block_left_side >= player_left_side and block_right_side <= player_right_side
        and block_top_side >= player_top_side and block_bottom_side >= player_top_side and block_top_side <= player_bottom_side)):

            return 2

        else:
            return 1      


def update_list(cube_list, WIDTH):
    #index = length of list
    if len(cube_list) < CUBE_COUNT:    
        cube = Obstacle(WIDTH)
        cube_list.append(cube)


def draw_enemies(cube_list):

    for x in range(len(cube_list)):
        pygame.draw.rect(screen, cube_list[x].color, (cube_list[x].x_pos, cube_list[x].y_pos, cube_list[x].size, cube_list[x].size), 0)


def move_enemy(cube_list, score):

    for x in range(len(cube_list)):

        if(cube_list[x].y_pos > player_pos[1]):
            score += 1

        if cube_list[x].y_pos < HEIGHT:

            if(cube_list[x].y_pos < HEIGHT / 2):
                cube_list[x].size = 1
                cube_list[x].y_pos += 5 
            
            else:
                cube_list[x].y_pos += 5 * (cube_list[x].size * .1) # acceleration

                if cube_list[x].size < 80:
                    cube_list[x].size += (cube_list[x].size) * .03 # = scaling factor

        else:
            cube_list.pop(x)
            update_list(cube_list, WIDTH)
        
    return score


def start_screen(state, clicked, enter):
    mouse = pygame.mouse.get_pos()

    screen.fill(BLACK)
    font = pygame.font.Font('freesansbold.ttf', 64)
    death_text = font.render("Cubefield 2D", True, WHITE)
    screen.blit(death_text, (WIDTH/3.3, HEIGHT/2 - 100))

    font = pygame.font.Font('freesansbold.ttf', 32)
    death_text = font.render("By John Melton", True, WHITE)
    screen.blit(death_text, (WIDTH/2.7, HEIGHT/2))

    #GREEN BUTTON
    restart_text = font.render("Start", True, WHITE)
    textRect = (250 + 12, (HEIGHT - 250)+(50/4))
    
    if (250+100) > mouse[0] > 250 and (HEIGHT - 250 + 50) > mouse[1] > (HEIGHT - 250):
        rect_start = pygame.draw.rect(screen, LIGHT_GREEN, (250, HEIGHT - 250, 100, 50), 0)
        if clicked:
            state = 1
    else:
        rect_start = pygame.draw.rect(screen, GREEN, (250, HEIGHT - 250, 100, 50), 0)
    screen.blit(restart_text, textRect)

    #RED BUTTON
    restart_text = font.render("Quit", True, WHITE)
    textRect = (WIDTH - 350 + 15 , (HEIGHT - 250)+(50/4))
    
    if (WIDTH - 350 + 100) > mouse[0] > (WIDTH - 350) and (HEIGHT - 250 + 50) > mouse[1] > (HEIGHT - 250):
        rect_stop = pygame.draw.rect(screen, LIGHT_RED, (WIDTH - 350, HEIGHT - 250, 100, 50), 0)
        if clicked:
            pygame.quit()
            exit()
    else:
        rect_stop = pygame.draw.rect(screen, RED, (WIDTH - 350, HEIGHT - 250, 100, 50), 0)
    screen.blit(restart_text, textRect)

    pygame.display.update()
    if enter:
        state = 1
        score = 0
        print("ENTER")
    return state


def run_game(cube_list, score):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and (player_pos[0] > 0):
        player_pos[0] -= 6
    if keys[pygame.K_RIGHT] and (player_pos[0] < (WIDTH - player_size)):
        player_pos[0] += 6

    screen.fill(BLACK)
    
    #Move the enemies
    make_enemy(enemy_list, WIDTH)
    draw_enemies(enemy_list)
    score = move_enemy(enemy_list, score)

    for x in range(len(cube_list)):
        state = check_collision(player_pos[0], player_pos[1], cube_list[x].x_pos, cube_list[x].y_pos, player_size, cube_list[x].size)
        if state == 2:
            enemy_list.clear()
            break
        else:
            pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], player_size, player_size), 0)
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT / 2), 0)
            show_score(textX, textY)

    pygame.display.update()
        
    return state, score


def dead_player(score, clicked, enter):
    mouse = pygame.mouse.get_pos()
    state = 2
    display_death_screen()

    #GREEN BUTTON
    restart_text = font.render("Start", True, WHITE)
    textRect = (250 + 12, (HEIGHT - 250)+(50/4))
    
    if (250+100) > mouse[0] > 250 and (HEIGHT - 250 + 50) > mouse[1] > (HEIGHT - 250):
        rect_start = pygame.draw.rect(screen, LIGHT_GREEN, (250, HEIGHT - 250, 100, 50), 0)
        if clicked:
            state = 1
            score = 0
    else:
        rect_start = pygame.draw.rect(screen, GREEN, (250, HEIGHT - 250, 100, 50), 0)
    screen.blit(restart_text, textRect)

    #RED BUTTON
    restart_text = font.render("Quit", True, WHITE)
    textRect = (WIDTH - 350 + 15 , (HEIGHT - 250)+(50/4))
    
    if (WIDTH - 350 + 100) > mouse[0] > (WIDTH - 350) and (HEIGHT - 250 + 50) > mouse[1] > (HEIGHT - 250):
        rect_stop = pygame.draw.rect(screen, LIGHT_RED, (WIDTH - 350, HEIGHT - 250, 100, 50), 0)
        #get_click = pygame.mouse.get_pressed()
        if clicked:
            pygame.quit()
            exit()
    else:
        rect_stop = pygame.draw.rect(screen, RED, (WIDTH - 350, HEIGHT - 250, 100, 50), 0)
    screen.blit(restart_text, textRect)

    pygame.display.update()

    if enter:
        state = 1
        score = 0

    return state, score

#Game loop
while True:

    get_click = False
    enterPressed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exiting...")
            pygame.quit()
            exit()     
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            get_click = True
            #print("CLICK")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            enterPressed = True

    #Start Menu
    if state == 0:
        score = 0
        state = start_screen(state, get_click, enterPressed)
    #Game 
    elif state == 1:
        result = run_game(enemy_list, score)
        state = result[0]
        score = result[1]
    #Death Menu
    elif state == 2:
        result = dead_player(score, get_click, enterPressed)
        state = result[0]
        score = result[1] 
        
    clock.tick(60)   


    
