
import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Angry Birds')

game_images = {}
game_sounds = {}
FPS = 30

# Function Area
# getting welcome screen
def start():
    while True:
        screen.blit(game_images["background"], (0, 0))
        screen.blit(game_images["base"], (0, baseY))
        screen.blit(game_images["message"], (messageX, messageY))
        screen.blit(game_images["playerUpFlap"], (playerX, playerY))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                return


def game_loop():
    new_pipe1 = pipe_generator()
    new_pipe2 = pipe_generator()
    upper_pipes = [
        {"x": SCREEN_WIDTH, "y": new_pipe1[0]["y"]},
        {"x": SCREEN_WIDTH * 1.5, "y": new_pipe2[0]["y"]}
    ]
    lower_pipes = [
        {"x": SCREEN_WIDTH, "y": new_pipe1[1]["y"]},
        {"x": SCREEN_WIDTH * 1.5, "y": new_pipe2[1]["y"]}
    ]

    pipe_speedX = -10
    """
    Frames  pipeX
    1       1400
    2       1405
    3       1410
    4       1415

    30      1550
    """
    player_speedY = -20
    player_flying_speedY = -30
    gravity = 5
    player_falling_speed_limit = 10
    player_flying = False
    score = 0
    playerY = SCREEN_HEIGHT/2 - 100
    flap_up = 0
    game_sounds["playback"].play(loops=-1)
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_UP:
                if playerY > -5:
                    player_speedY = player_flying_speedY
                    player_flying = True
                    game_sounds["flap"].play()
                    flap_up = 5

        # blitting:
        screen.blit(game_images["background"], (0, 0))
        
        if flap_up > 0:
            screen.blit(game_images["playerUpFlap"], (playerX, playerY))
        else:
            screen.blit(game_images["playerDownFlap"], (playerX, playerY))
        
        for lower_pipe, upper_pipe in zip(lower_pipes, upper_pipes):
            screen.blit(game_images["pipe"][0], (upper_pipe["x"], upper_pipe["y"]))
            screen.blit(game_images["pipe"][1], (lower_pipe["x"], lower_pipe["y"]))

        screen.blit(game_images["base"], (0, baseY))
        

        pygame.time.Clock().tick(FPS)
        pygame.display.update()

        # Moving player up
        playerY = playerY + player_speedY
        flap_up -= 1
        if player_flying:
            player_flying = False

        # Gravity
        if not player_flying and player_speedY <= player_falling_speed_limit:
           player_speedY = player_speedY + gravity

        # Moving the pipes
        for lower_pipe, upper_pipe in zip(lower_pipes, upper_pipes):
            lower_pipe["x"] = lower_pipe["x"] + pipe_speedX
            upper_pipe["x"] = upper_pipe["x"] + pipe_speedX
            # Adding new pipes
            if lower_pipe["x"] < 0:
                new_pipe = pipe_generator()
                upper_pipes.append(new_pipe[0])
                lower_pipes.append(new_pipe[1])
            # Removing old pipes
                upper_pipes.pop(0)
                lower_pipes.pop(0)

        # Player dies
        if player_dies(playerX, playerY, upper_pipes, lower_pipes):
            print("Player_dies called")
            screen.blit(game_images["background"], (0, 0))

            screen.blit(game_images["playerDead"], (playerX, playerY))
        
            for lower_pipe, upper_pipe in zip(lower_pipes, upper_pipes):
                screen.blit(game_images["pipe"][0], (upper_pipe["x"], upper_pipe["y"]))
                screen.blit(game_images["pipe"][1], (lower_pipe["x"], lower_pipe["y"]))

            screen.blit(game_images["base"], (0, baseY))
    
            pygame.time.Clock().tick(FPS)
            pygame.display.update()
            game_sounds["die"].play()
            pygame.time.delay(5000)
            return


def pipe_generator():
    gap = player_height * 3
    y2 = randint(gap, baseY)
    y1 = y2 - gap - pipe_height
    pipe = [
        {"x": SCREEN_WIDTH, "y": y1},
        {"x":SCREEN_WIDTH, "y": y2}
    ]
    return pipe

def player_dies(playerX, playerY, upper_pipes, lower_pipes):
    # if playerY < 0:
    #     return True
    
    # colliding with ground
    if playerY + player_height > baseY+10:
        return True
    
    for lower_pipe, upper_pipe in zip(lower_pipes, upper_pipes):
        # colliding with upper pipes
        if playerY < upper_pipe["y"] + pipe_height - 20 and upper_pipe["x"]-player_width+20 < playerX < upper_pipe["x"]+pipe_width-20:
            return True
        # colliding with lower pipes
        if playerY > lower_pipe["y"] - 20 and lower_pipe["x"]-player_width+20 < playerX < lower_pipe["x"]+pipe_width-20:
            return True

def game_over_screen():
    print("Game Over Called")
    game_sounds["game_over"].play()
    pygame.time.delay(3000)
    return

# loading all the images

game_images["background"] = pygame.image.load("images/bg1.png").convert_alpha()
game_images["base"] = pygame.image.load("images/base.png").convert_alpha()
game_images["playerUpFlap"] = pygame.image.load("images/bird3.png").convert_alpha()
game_images["playerDownFlap"] = pygame.image.load("images/bird3_downflaps.png").convert_alpha()
game_images["playerDead"] = pygame.image.load("images/bird3_dead.png").convert_alpha()
game_images["message"] = pygame.image.load("images/message.png").convert_alpha()
game_images["pipe"] = [
            pygame.transform.rotate(pygame.image.load("images/pipe.png"), 180),
            pygame.image.load("images/pipe.png")
    ]
game_images["numbers"] = (
    pygame.image.load("images/0.png").convert_alpha(),
    pygame.image.load("images/1.png").convert_alpha(),
    pygame.image.load("images/2.png").convert_alpha(),
    pygame.image.load("images/3.png").convert_alpha(),
    pygame.image.load("images/4.png").convert_alpha(),
    pygame.image.load("images/5.png").convert_alpha(),
    pygame.image.load("images/6.png").convert_alpha(),
    pygame.image.load("images/7.png").convert_alpha(),
    pygame.image.load("images/8.png").convert_alpha(),
    pygame.image.load("images/9.png").convert_alpha()
)


# loading sounds
game_sounds["playback"] = pygame.mixer.Sound("sounds/playback.wav")
game_sounds["flap"] = pygame.mixer.Sound("sounds/flap.wav")
game_sounds["point"] = pygame.mixer.Sound("sounds/point.wav")
game_sounds["die"] = pygame.mixer.Sound("sounds/die.wav")
game_sounds["game_over"] = pygame.mixer.Sound("sounds/game_over.wav")

base_height = game_images["base"].get_height()
baseY = SCREEN_HEIGHT - base_height

message_width = game_images["message"].get_width()
message_height = game_images["message"].get_height()
messageX = (SCREEN_WIDTH - message_width)/2
messageY = (SCREEN_HEIGHT - message_height)/2

playerX = SCREEN_WIDTH/5
playerY = SCREEN_HEIGHT/2 - 100

player_width = game_images["playerUpFlap"].get_width()
player_height = game_images["playerUpFlap"].get_height()

pipe_width = game_images["pipe"][1].get_width()
pipe_height = game_images["pipe"][1].get_height()


start()
game_loop()
game_over_screen()
print("Game Ended")
"""
l1 = [1, 2, 3]
l2 = ["a", "b", "c"]
print(list(zip(l1, l2)))
for i, j in zip(l1, l2):
    print(i)

l3 = ["A", "B", "C"]
print(list(zip(l1, l2, l3)))
"""