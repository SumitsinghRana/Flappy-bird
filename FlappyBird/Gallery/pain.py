import sys
import random
import pygame
from pygame.locals import *
from pygame import mixer 
mixer.init()
mixer.music.load("Audio/arcade.mp3") 
mixer.music.set_volume(0.2) 

fps=45
screenWidth=900
screenHeight=600
screen=pygame.display.set_mode((screenWidth,screenHeight))
groundy=screenHeight*0.75
game_images={}
game_sounds={}
player='Images/bird11.png'
pipe='Images/pipe.png'
backGround='Images/back420.jpg'



def welcomeScreen():


    playerx = int(screenWidth/5)
    playery = int((screenHeight - game_images['player'].get_height())/2)
    messagex = int((screenWidth - game_images['message'].get_width())/2)
    messagey = int(screenHeight*0.0)
    basex = 0
    while True:
        for event in pygame.event.get():

            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                mixer.music.play() 
                return
            else:
                screen.blit(game_images['backGround'], (0, 0))    
                screen.blit(game_images['player'], (playerx, playery)) 
                screen.blit(game_images['message'], (messagex,messagey ))  
                screen.blit(game_images['base'], (basex, groundy))         
                pygame.display.update()
                FPSCLOCK.tick(fps)

def mainGame():
    score = 0
    playerx = int(screenWidth/5)
    playery = int(screenWidth/4)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': screenWidth+200, 'y':newPipe1[0]['y']},
        {'x': screenWidth+200+(screenWidth/2), 'y':newPipe2[0]['y']},
    ]

    lowerPipes = [
        {'x': screenWidth+200, 'y':newPipe1[1]['y']},
        {'x': screenWidth+200+(screenWidth/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 
    playerFlapped = False 


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    game_sounds['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) 
        if crashTest:
            return     

        
        playerMidPos = playerx + game_images['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_images['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Score->{score}") 
                game_sounds['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = game_images['player'].get_height()
        playery = playery + max(min(playerVelY, screenHeight - playerHeight - playery), -playery)


        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -game_images['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        screen.blit(game_images['backGround'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(game_images['base'], (basex, groundy))
        screen.blit(game_images['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_images['numbers'][digit].get_width()
        Xoffset = (screenWidth- width)/2

        for digit in myDigits:
            screen.blit(game_images['numbers'][digit], (Xoffset, screenHeight*0.12))
            Xoffset += game_images['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(fps)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    
    
    for pipe in upperPipes:
        pipeHeight = game_images['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < game_images['pipe'][0].get_width()):
            game_sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + game_images['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < game_images['pipe'][0].get_width():
            game_sounds['hit'].play()
            return True
        
    if playery + game_images['player'].get_height() >= groundy:
        game_sounds['hit'].play()
        return True    

    return False

def getRandomPipe():
    pipeHeight = game_images['pipe'][0].get_height()
    offset = screenWidth/6
    y2 = offset + random.randrange(0, int(screenHeight - game_images['base'].get_height()  - 1.1*offset))
    pipeX = screenWidth - 50
    
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, {'x': pipeX, 'y': y2}
    ]
    return pipe



if __name__ == '__main__':
    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Sumit,Vaibhav,Adarsh')
    game_images['numbers']=(
        pygame.image.load('Images/0.png').convert_alpha(),
        pygame.image.load('Images/1.png').convert_alpha(),
        pygame.image.load('Images/2.png').convert_alpha(),
        pygame.image.load('Images/3.png').convert_alpha(),
        pygame.image.load('Images/4.png').convert_alpha(),
        pygame.image.load('Images/5.png').convert_alpha(),
        pygame.image.load('Images/6.png').convert_alpha(),
        pygame.image.load('Images/7.png').convert_alpha(),
        pygame.image.load('Images/8.png').convert_alpha(),
        pygame.image.load('Images/9.png').convert_alpha(),

    )
    
    game_images['message'] =pygame.image.load('Images/message.jpg').convert_alpha()
    game_images['base'] =pygame.image.load('Images/base.png').convert_alpha()
    game_images['pipe'] =(pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180), 
    pygame.image.load(pipe).convert_alpha()
    )
    game_images['backGround'] = pygame.image.load(backGround).convert()
    game_images['player'] = pygame.image.load(player).convert_alpha()

    game_sounds['hit'] = pygame.mixer.Sound('Audio/hit.mp3')
    game_sounds['point'] = pygame.mixer.Sound('Audio/point.wav')
    game_sounds['wing'] = pygame.mixer.Sound('Audio/wing.wav')

   
    while True:
        welcomeScreen()
        mainGame() 




