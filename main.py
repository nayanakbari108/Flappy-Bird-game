import random
import pygame
import sys# sys.exit to exit the game
import time

from pygame.locals import * # basic pygame imports

#global variables

fps=32
screenwidth= 288
screenheight= 512
screen =pygame.display.set_mode((screenwidth,screenheight))
ground_y=screenheight*0.8
game_sprites={}
game_sounds={}

background0='gallery\\images\\background-1.png'
background1='gallery\\images\\background-2.png'
pipe1='gallery\\images\\pipe-red.png'
pipe0='gallery\\images\\pipe-green.png'


def bird(i,playerx,playery,playervel=0,crash=False,scale=1):
    if crash==False:
     if scale==0:
       screen.blit(pygame.transform.scale(game_sprites['player'][i],(40,28)), (playerx,playery))
     else:  
       screen.blit(pygame.transform.rotate(game_sprites['player'][i],-playervel*2.5), (playerx,playery))
    else:
     screen.blit(pygame.transform.rotate(game_sprites['player'][1],-playervel*7), (playerx,playery))
   
def onclick(x,y,pos):
    
    if x+3<=pos[0]<=(x+game_sprites['restart'].get_width()-4) and y+3<=pos[1]<=(y+game_sprites['restart'].get_height()-3):
         
      if pygame.mouse.get_pressed()[0]==1:
         game_sounds['click'].play()
         
         return True
      else :
         return False
        


def welcomeScreen():
        startx=int((screenwidth-game_sprites['start'].get_width())/2)+2
        starty=335
        playery=int((screenheight-game_sprites['player'][0].get_height())/2)-23
        playerx=int((screenwidth-game_sprites['player'][0].get_width())/2)-5
        messagex=int((screenwidth-game_sprites['message'].get_width())/2)
        messagey=int(screenheight*0.13)-10
        basex=0
        i=0
        counter=0
        
        while True:
            screen.blit(game_sprites['background'],(0,0))
            screen.blit(game_sprites['message'],(messagex,messagey))
            counter+=1
            if counter%4==0:
             i+=1
             if i==3:
               i=0
            bird(i,playerx,playery,0,False,0)

            screen.blit(game_sprites['base'],(basex,ground_y))
            basex=basex-2
            if basex<=-48:
             basex=0

            screen.blit(game_sprites['start'],(startx,starty))
             

            
            for event in pygame.event.get():
                # if user presses close than close the game
                if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                    game_sounds['click'].play()
                    time.sleep(0.5)
                    pygame.quit()
                    sys.exit()
                # if user presses space or up key than start the game
                elif event.type ==KEYDOWN and(event.key == K_SPACE or event.key==K_UP):
                    game_sounds['click'].play()
                    return
                
                pos=pygame.mouse.get_pos()# mouse position
                if onclick(startx,starty,pos)==True:
                    time.sleep(0.2)
                    return
                     
            
            pygame.display.update()
            fpsclock.tick(fps)
           
def mainGame():
        print("--------------New Game-----------------")
        crash=False
        counter=0
        
        i=0
        score=0
        playerx= int(screenwidth/5)
        playery=int(screenheight/2)
        basex=0
        # create 2 pipes for bliting on screen
        newPipe1=getRandomPipe(score)
        newPipe2=getRandomPipe(score)

        # list of upper pipes
        upper_pipes=[
             {'x':screenwidth+200,'y':newPipe1[0]['y']},
             {'x':screenwidth+200+(screenwidth/2),'y':newPipe2[0]['y']}
        ]
        lower_pipes=[
             {'x':screenwidth+200,'y':newPipe1[1]['y']},
             {'x':screenwidth+200+(screenwidth/2),'y':newPipe2[1]['y']}
        ]
        pipe_speed=-4
        playerVel=-9
        playerMaxVel=10
        playerMinVel=-8
        playerAccY=1
        playerFlapAccV=-8
        playerFlapped=False
         
        while True:
            for event in pygame.event.get():
                  if event.type== QUIT or (event.type== KEYDOWN and event.key==K_ESCAPE):
                       game_sounds['click'].play()
                       time.sleep(0.5)
                       pygame.quit()
                       sys.exit()
                  if event.type==KEYDOWN and (event.key==K_SPACE or event.key== K_UP):
                       if crash==False:
                        if playery>0:
                            playerVel=playerFlapAccV
                            playerFlapped=True
                            game_sounds['jump'].play()
            if 30<=score<=60:
                pipe_speed=-4.5
            if 61<=score<=100:
                pipe_speed=-5
            if 101<=score<=200:
                pipe_speed=-5.5
            if 201<=score<=1000:
                pipe_speed=-5.9
            
            if crash==False:
             crashTest=isCollide(playerx,playery,upper_pipes,lower_pipes)
             if crashTest:
                 crash=True
                 
            
            # check for score
            if crash == False:
                playerMidPos = playerx + game_sprites['player'][0].get_width()/2
                for pipe in upper_pipes:
                  pipeMidPos = pipe['x'] + game_sprites['pipe'][0].get_width()/2
                  if pipeMidPos<= playerMidPos < pipeMidPos +4:
                    score +=1
                    print(f"Your score is {score}") 
                    game_sounds['point'].play()

            if playerVel<playerMaxVel and not playerFlapped:
                 playerVel+=playerAccY
            if playerFlapped:
                 playerFlapped=False
            playerHeight=game_sprites['player'][0].get_height()   
            playery=playery+min(playerVel,ground_y-playery-playerHeight)                

            if crash == False:
            # move pipes to left
                for upper_pipe,lower_pipe in zip(upper_pipes,lower_pipes):
                     upper_pipe['x']+=pipe_speed
                     lower_pipe['x']+=pipe_speed
                if 0<upper_pipes[0]['x']<5:
                     newpipe=getRandomPipe(score)
                     upper_pipes.append(newpipe[0])
                     lower_pipes.append(newpipe[1])

                #  if pipe out of screen then rem0ve it
                if upper_pipes[0]['x'] <-game_sprites['pipe'][0].get_width():
                     upper_pipes.pop(0)
                     lower_pipes.pop(0)
            
            # let blit the sprites:
            if(playery!=ground_y):
                screen.blit(game_sprites['background'],(0,0))
                for upper_pipe,lower_pipe in zip(upper_pipes,lower_pipes):
                      screen.blit(game_sprites['pipe'][0],(upper_pipe['x'],upper_pipe['y']))
                      screen.blit(game_sprites['pipe'][1],(lower_pipe['x'],lower_pipe['y']))
                  
                
                screen.blit(game_sprites['base'],(basex,ground_y))
                if crash==False:
                 basex=basex+pipe_speed
                 if basex<=-48:
                  basex=0
            # screen.blit(game_sprites['player'],(playerx,playery))
                counter+=1
                if counter%4==0:
                 i+=1
                 if i==3:
                   i=0
                bird(i,playerx,playery,playerVel,crash)
  
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
               width += game_sprites['numbers'][digit].get_width()
            Xoffset = (screenwidth - width)/2


            for digit in myDigits:
              screen.blit(game_sprites['numbers'][digit], (Xoffset, screenheight*0.12))
              Xoffset += game_sprites['numbers'][digit].get_width()

            if (playery + 26 >=ground_y and crash== True):

                    restart_x=int(screenwidth-game_sprites['restart'].get_width())/2
                    restart_y=int(screenheight-game_sprites['restart'].get_height())/2
                    screen.blit(game_sprites['restart'],(restart_x,restart_y))
                    screen.blit(game_sprites['game_over'],(int(screenwidth-game_sprites['game_over'].get_width())/2,int(screenheight-100-game_sprites['game_over'].get_height())/2))

                    pos=pygame.mouse.get_pos()# mouse position
                    if onclick(restart_x,restart_y,pos)==True:
                     randomSpirites()
                     time.sleep(0.2)
                     return
                    pygame.display.update()
            

            pygame.display.update()
            fpsclock.tick(fps)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> ground_y - 25  or playery<0:
        game_sounds['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < (game_sprites['pipe'][0].get_width())/1.5):
            game_sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + game_sprites['player'][0].get_height() > pipe['y']) and abs(playerx - pipe['x']) < (game_sprites['pipe'][0].get_width())/1.5:
            game_sounds['hit'].play()
            return True

    return False


    

def getRandomPipe(score):
    if 0<=score<=60:
        div=4
    if 61<=score<=120:
        div=4.5
    if 121<=score<=1000:
        div=5
    #  generates postion of two pipes for bliting on screen:
    pipeHeight=game_sprites['pipe'][0].get_height()
    offset=screenheight/div
    y2=offset+random.randrange(int(game_sprites['pipe'][0].get_height()*0.10),int(screenheight-game_sprites['base'].get_height()-1.5*offset))
    pipe_x=screenwidth+10

    y1= y2-pipeHeight-offset
    pipe=[
         {'x':pipe_x,'y':y1},#upper pipe
         {'x':pipe_x,'y':y2}#lower pipe
    ]
    return pipe


def randomSpirites():
    num1=random.randrange(0,2)
    if num1==0:
        game_sprites['pipe']= (
        pygame.transform.rotate( pygame.image.load(pipe0).convert_alpha(),180),
        pygame.image.load(pipe0).convert_alpha()
          )
        game_sprites['background']= pygame.image.load(background0).convert()
        game_sprites['player']=(
        pygame.image.load('gallery\\images\\redbird-downflap.png').convert_alpha(),
        pygame.image.load('gallery\\images\\redbird-midflap.png').convert_alpha(),
        pygame.image.load('gallery\\images\\redbird-upflap.png').convert_alpha(),
        )
    else:
        game_sprites['pipe']= (
        pygame.transform.rotate( pygame.image.load(pipe1).convert_alpha(),180),
        pygame.image.load(pipe1).convert_alpha()
          )
        game_sprites['background']= pygame.image.load(background1).convert()
        game_sprites['player']=(
        pygame.image.load('gallery\\images\\yellowbird-downflap.png').convert_alpha(),
        pygame.image.load('gallery\\images\\yellowbird-midflap.png').convert_alpha(),
        pygame.image.load('gallery\\images\\yellowbird-upflap.png').convert_alpha(),
        )
    


if __name__=="__main__":
   #    main function
    pygame.init()# initialise all pygame modules
    fpsclock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by NA")
    game_sprites['numbers'] =(
        pygame.image.load('gallery\\images\\0.png').convert_alpha(),
        pygame.image.load('gallery\\images\\1.png').convert_alpha(),
        pygame.image.load('gallery\\images\\2.png').convert_alpha(),
        pygame.image.load('gallery\\images\\3.png').convert_alpha(),
        pygame.image.load('gallery\\images\\4.png').convert_alpha(),
        pygame.image.load('gallery\\images\\5.png').convert_alpha(),
        pygame.image.load('gallery\\images\\6.png').convert_alpha(),
        pygame.image.load('gallery\\images\\7.png').convert_alpha(),
        pygame.image.load('gallery\\images\\8.png').convert_alpha(),
        pygame.image.load('gallery\\images\\9.png').convert_alpha()
       
    )
    game_sprites['restart']=pygame.transform.scale(pygame.image.load('gallery\\images\\restart.png').convert_alpha(),(100,35))
    game_sprites['game_over']=pygame.image.load('gallery\\images\\gameover.png').convert_alpha()
    game_sprites['message']=pygame.image.load('gallery\\images\\message.png').convert_alpha()
    game_sprites['base']=pygame.image.load('gallery\\images\\base.png').convert_alpha()
    game_sprites['start']=pygame.transform.scale(pygame.image.load('gallery\\images\\start.png').convert_alpha(),(95,49))
    game_sprites['start1']=pygame.transform.scale(pygame.image.load('gallery\\images\\start.png').convert_alpha(),(98,51))
    randomSpirites()
    
    
#    game sounds
    game_sounds['die']=pygame.mixer.Sound('gallery\\audio\\die.mp3')
    game_sounds['flap']=pygame.mixer.Sound('gallery\\audio\\flap.mp3')
    game_sounds['hit']=pygame.mixer.Sound('gallery\\audio\\gameover.mp3')
    game_sounds['swoosh']=pygame.mixer.Sound('gallery\\audio\\swoosh.mp3')
    game_sounds['point']=pygame.mixer.Sound('gallery\\audio\\point.mp3')
    game_sounds['jump']=pygame.mixer.Sound('gallery\\audio\\jump.wav')
    game_sounds['click']=pygame.mixer.Sound('gallery\\audio\\click.wav')
    
   
    
    
    while True:

        welcomeScreen() #shows welcome screen to the user untill he presses a button
        mainGame()#this is a main game function
        