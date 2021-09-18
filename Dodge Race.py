import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 220)

bright_green = (0, 255, 0)
bright_red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Dodge Race')
clock = pygame.time.Clock()
carImg = pygame.image.load('racecar.png')
pygame.display.set_icon(carImg)

crash_sound = pygame.mixer.Sound('crash.wav')
pygame.mixer.music.load('Fun.wav')

pause = False
h = False
intro = True

def game_intro():
    pygame.mixer.music.stop()
    global h
    h = False
    intro = True
    while intro:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                
        gameDisplay.fill(white)
        display_text('freesansbold.ttf', 100, 'Dodge Race', (display_width/2), (display_height/2))

        button('GO!', 150, 440, 100, 50, green, bright_green, game_loop)
        button('Quit', 550, 440, 100, 50, red, bright_red, quitgame)
        button('Help', 350, 500, 100, 50, white, white, help_screen)
        clock.tick(15)
        pygame.display.update()

def help_screen():
    global pause
    global intro
    global h
    intro = False
    h = True
    while h:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if pause == False:
                        game_loop()
                    else:
                        unpause()
        gameDisplay.fill(white)
        display_text('freesansbold.ttf', 50, 'Help', (display_width/2), 30)
        display_text('freesansbold.ttf', 20, 'Use arrows to move the car;', 150, 70)
        display_text('freesansbold.ttf', 20, 'Avoid the blocks and the edges to score;', 210, 110)
        display_text('freesansbold.ttf', 20, "Press 'P' if you want to pause the game;", 210, 150)
        display_text('freesansbold.ttf', 20, "Pressing 'ENTER' is the same action as clicking the green buttons and", 360, 190)
        display_text('freesansbold.ttf', 20, "Have fun :)", 70, 230)

        if pause == False:
            button('GO!', 150, 390, 100, 50, green, bright_green, game_loop)
            button('Back', 550, 390, 100, 50, red, bright_red, game_intro)
        else:
            button('Continue', 150, 390, 100, 50, green, bright_green, unpause)
            button('Restart', 550, 390, 100, 50, red, bright_red, game_loop)
        clock.tick(15)
        pygame.display.update()
        

def paused():
    global h
    h = False
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    unpause()
                
        display_text('freesansbold.ttf', 100, 'Paused', (display_width/2), (display_height/2))

        button('Continue', 150, 440, 100, 50, green, bright_green, unpause)
        button('Restart', 550, 440, 100, 50, red, bright_red, game_loop)
        button('Help', 390, 350, 40, 20, white, white, help_screen)
        clock.tick(15)
        pygame.display.update()

def unpause():
    
    global pause
    global h
    pause = False
    h = False
    

def button(msg, x, y, width, height, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, width, height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, width, height))
    display_text('freesansbold.ttf', 20, msg, (x+width/2), (y+height/2))

def quitgame():
    pygame.quit()
    quit()

def things(x, y, width, height, color):
    pygame.draw.rect(gameDisplay, color, [x, y, width, height])

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text, (0, 0))

def car(x, y):
    gameDisplay.blit(carImg, (x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def display_text(font, fontSize, text, text_x, text_y):
    largeText = pygame.font.Font(font, fontSize)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (text_x,text_y)
    gameDisplay.blit(TextSurf, TextRect)

def crash():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                
        display_text('freesansbold.ttf', 80, 'CRASH!!!', (display_width/2), (display_height/2))

        button('Play again', 350, 440, 100, 50, green, bright_green, game_loop)
        clock.tick(15)
        pygame.mixer.music.stop()
        pygame.display.update()

def game_loop():
    global h
    global pause
    global intro
    intro = False
    h = False
    pygame.mixer.music.play(-1)

    x = display_width * 0.45
    y = display_height * 0.7
    x_change = 0
    
    thing_x = random.randrange(0, display_width - 100)
    thing_x2 = 0
    thing_y = -600
    thing_speed = 5
    thing_height = 100
    thing_width = 100
    
    
    crashed = False
    dodged = 0
    
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -thing_speed
                    
                if event.key == pygame.K_RIGHT:
                    x_change = thing_speed

                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT and pygame.key.get_pressed()[pygame.K_RIGHT] == 0 or event.key == pygame.K_RIGHT and pygame.key.get_pressed()[pygame.K_LEFT] == 0):
                    x_change = 0
                    

        x += x_change
        gameDisplay.fill(white)
        things(thing_x, thing_y, thing_width, thing_height, blue)
        if dodged % 3 == 0:
            things(thing_x2, thing_y, thing_width, thing_height, blue)
        thing_y += thing_speed
        car(x,y)
        things_dodged(dodged)
        if x > display_width - 109 or x < 0:
            pygame.mixer.Sound.play(crash_sound)
            crash()
            
        if thing_y > display_height:
            thing_y = 0 - thing_height
            thing_x = random.randrange(0, display_width - 100)
            thing_x2 = random.randrange(0, display_width - 100)
            if dodged <= 11:
                thing_speed += 0.8
            else:
                thing_speed += 0.05
            if dodged > 10:
                thing_width += 2.6
            dodged += 1
            
            
        if thing_y + thing_height > y + 10:
            if (x + 3 > thing_x and x + 3 < thing_x + thing_width or x+106 > thing_x and x+106 < thing_x + thing_width) or ((x + 3 > thing_x2 and x + 3 < thing_x2 + thing_width or x+106 > thing_x2 and x+106 < thing_x2 + thing_width) and dodged % 3 == 0):
                pygame.mixer.Sound.play(crash_sound)
                crash()
            
        pygame.display.update()
        clock.tick(60)
game_intro()


