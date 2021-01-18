'''
@Author Tanner Coker

This my creation of the classic pong game. It will start the game in a simple menu that will display the 2 game modes and a exit button.
User can choose to play a singleplayer game against a bot or they can play with another user locally.


'''

import pygame as pg
import random
pg.init()

Screen = (1500, 900)
window = pg.display.set_mode(Screen)
buttonWidth = 200
buttonHeight = 75

clock = pg.time.Clock()

font = pg.font.SysFont('comicsans', 60)
titleFont = pg.font.SysFont('comicsans', 250)
scoreFont = pg.font.SysFont('comicsans', 200)


#this class is to act as a button for the game. It will input an x,y-coor, a width&height and a text to display.
class button():
    def __init__(self, color, x,y,width,height,text ='', textColor = (0,0,0)):
        self.color=color
        self.x = x
        self.y = y
        self.width = width
        self.height=height
        self.text = text
        self.textColor = textColor

    def draw(self, window, outline=None):
        if outline:
            pg.draw.rect(window, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pg.draw.rect(window, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pg.font.SysFont('comicsans', 45)
            text = font.render(self.text, 1, self.textColor)
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False



#this class will be the ball that is bounced around during gameplay. It will bounce off of the walls and off of the paddles
class ball(pg.Rect):
    speedx = 10
    speedIncrease = 0
    hitCounter = 0
    speedy = 8
    def __init__(self, color, x, y, radius):
        super().__init__(x, y,radius,radius)
        self.color = color
        self.radius = radius
        self.newDir()

    #draws the ball to the window
    def draw(self, window):
        pg.draw.ellipse(window, self.color, self, self.radius)

    #moves the balls x,y pos. If it hits a boundary then it bounces off of it.
    def updateBall(self):
        self.x += self.speedx + self.speedIncrease
        self.y += self.speedy
        if self.x+self.radius >= Screen[0] or self.x <= 0:
            self.speedx *= -1
        if self.y+self.radius >= Screen[1] or self.y <= 0:
            self.speedy *= -1
        if self.bottom >= Screen[1]:
            self.bottom = Screen[1] -1
        if self.top <= 0:
            self.top = 1

    #checks to see if it hits one of the paddles. If so, then it bounces off of it
    def checkCollision(self, rect1, rect2):
        if self.colliderect(rect1) or self.colliderect(rect2):
            self.speedx *= -1
            self.hitCounter += 1
            if self.hitCounter == 10 and self.speedIncrease < 6:
                self.hitCounter = 0
                self.speedIncrease += 1
            if self.x < Screen[0]/2 and self.y > rect1.center[1]:
                self.speedy = 7
            elif self.x < Screen[0]/2 and self.y < rect1.center[1]:
                self.speedy = -7
            elif self.x > Screen[0]/2 and self.y > rect2.center[1]:
                self.speedy = 7
            elif self.x > Screen[0]/2 and self.y < rect2.center[1]:
                self.speedy = -7

    def checkWallHit(self):
        if self.x+self.radius >= Screen[0] or self.x <= 0:
            self.speedIncrease = 0
            return True
        return False

    def newDir(self):
        self.speedx *= random.choice((-1,1))
        self.speedy *= random.choice((-1,1))


#class paddle is the paddle game object. They extend rectangles so that I can add a function specifically for updating the object.
class paddle(pg.Rect):
    speed = 0
    def __init__(self, color, x, y):
        super().__init__(x,y-75,10,150)
        self.color = color

    def draw(self, window):
        pg.draw.rect(window, self.color, self)

    #adds the speed value to the y value for the paddle. Stops it from going off of the bounds.
    def update(self):
        self.y += self.speed
        if self.top <= 0:
            self.top = 0
        if self.bottom >= Screen[1]:
            self.bottom = Screen[1]

    #resets the pos of the paddle back to starting. Used when a score is made so that player has a better chance of hitting the ball once it
    #respawns in the game.
    def resetPos(self):
        self.center = (self.center[0], Screen[1]/2)





#displays a the game menu. Provides user with various buttons that will be highlighted when hovering over them.
#Can choose to either go into a singleplayer game, multiplayer game, or exit the game.
def mainMenu():
    #buttons used navigate the game menu
    singleButton = button((255, 207, 33), Screen[0]/2-buttonWidth/2,Screen[1]/2-150,buttonWidth,buttonHeight, '1 Player', (35,35,35))
    multiButton = button((48, 246, 252), Screen[0]/2-buttonWidth/2,Screen[1]/2,buttonWidth,buttonHeight,'2 Player', (35,35,35))
    quitButton = button((25, 252, 181), Screen[0]/2-buttonWidth/2,Screen[1]/2+150, buttonWidth, buttonHeight, 'Exit', (35,35,35))

    #rendering of the title to display on the menu.
    title = titleFont.render('P   NG', 1, (150,150,150))

    #creates a ball to bounce around the menu just for visual appeal.
    pong = ball((25, 252, 181), Screen[0]/2, Screen[1]/2, 30)

    #menu loop. If player is viewing the menu then this will draw the menu and it's components until the menu is left, or the game is exited.
    viewing = True
    while viewing:
        #colors the window background, draws the buttons and pong ball on the screen, and draw the title to the screen.
        window.fill((35,35,35))
        pong.draw(window)
        singleButton.draw(window)
        multiButton.draw(window)
        quitButton.draw(window)
        window.blit(title, (Screen[0]/2-title.get_width()/2, 20))
        pg.draw.circle(window, (25,252,181), (Screen[0]/2-title.get_width()/2 + 190, 16+title.get_height()/2), 65)

        #checks all of the game events to see if the game is being exited, a button is being hovered over, or if a button is clicked.
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            #checks to see if a button is being clicked.
            if event.type == pg.MOUSEBUTTONDOWN:
                if quitButton.isOver(pos):
                    del pong
                    pg.quit()
                    quit()
                if singleButton.isOver(pos):
                    del pong
                    del singleButton
                    del multiButton
                    del quitButton
                    del title
                    viewing = False
                    singleRun()
                if multiButton.isOver(pos):
                    del pong
                    del singleButton
                    del multiButton
                    del quitButton
                    del title
                    viewing = False
                    multiRun()
            #checks to see if a button is being hovered over. If so then it will change the colors to 'highlight' it.
            if event.type == pg.MOUSEMOTION:
                if singleButton.isOver(pos):
                    singleButton.color = (222, 174, 0)
                else:
                    singleButton.color = (255, 207, 33)
                if multiButton.isOver(pos):
                    multiButton.color = (2, 201, 207)
                else:
                    multiButton.color = (48, 246, 252)
                if quitButton.isOver(pos):
                    quitButton.color = (0, 204, 140)
                else:
                    quitButton.color = (25, 252, 181)

        pong.updateBall()
        clock.tick(60)
        pg.display.update()



#this function runs the single player game once it has been selected in the main menu
def singleRun():
    #component creation needed for the game.
    pong = ball((25, 252, 181), Screen[0]/2, Screen[1]/2, 30)
    player = paddle((255, 207, 33), 20, Screen[1]/2)
    opponent = paddle((230,230,230), Screen[0]-30, Screen[1]/2)
    playerScore = opponentScore = 0

    #makes the rectangle that the menu&replay button will be in along with button creation.
    endRect = pg.Rect(Screen[0]/2-250,Screen[1]/2-150, 500,300)
    menuButton = button((255, 207, 33), endRect.x + 20, endRect.y + 200, 150, 75, 'Menu')
    replayButton = button ((48, 246, 252), endRect.x+endRect.width - 170, endRect.y + 200, 150, 75, 'Replay')

    #singleplayer game loop. Runs while it is being viewed.
    viewing = True
    gameDone = False
    while viewing:
        #checks all of the events in the game to see if it has been exited, if the user is returning to the menu after the game,
        #if a button is being hovered over it, and if user is providing keyboard input.
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            #moves the player up/down depending on the key input.
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    player.speed -= 7
                if event.key == pg.K_s:
                    player.speed += 7
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    player.speed += 7
                if event.key == pg.K_s:
                    player.speed -= 7
            #allows the player to select the buttons after the game is done.
            if event.type == pg.MOUSEBUTTONDOWN and gameDone:
                #deletes the components and returns to the game menu.
                if menuButton.isOver(pos):
                    del pong
                    del player
                    del opponent
                    del endRect
                    del menuButton
                    del replayButton
                    viewing = False
                    mainMenu()
                #resets the game components and scores so that another game starts.
                if replayButton.isOver(pos):
                    player.resetPos()
                    opponent.resetPos()
                    playerScore = 0
                    opponentScore = 0
                    gameDone = False
            #highlights the button when being hovered over.
            if event.type == pg.MOUSEMOTION:
                if replayButton.isOver(pos):
                    replayButton.color = (2, 201, 207)
                else:
                    replayButton.color = (48, 246, 252)
                if menuButton.isOver(pos):
                    menuButton.color = (222, 174, 0)
                else:
                    menuButton.color = (255, 207, 33)
        #creates the background and draws the score to the window.
        window.fill((35,35,35))
        pg.draw.line(window, (100,100,100), (Screen[0]/2,0), (Screen[0]/2,Screen[1]), 3)
        scoreString = str(playerScore)
        scoreDisplay = scoreFont.render(scoreString, 1 , (100,100,100))
        window.blit(scoreDisplay, (Screen[0]/4-scoreDisplay.get_width(), Screen[1]/2-scoreDisplay.get_height()/2))

        scoreString = str(opponentScore)
        scoreDisplay = scoreFont.render(scoreString, 1 , (100,100,100))
        window.blit(scoreDisplay, (Screen[0]-Screen[0]/4-scoreDisplay.get_width(), Screen[1]/2-scoreDisplay.get_height()/2))

        #draws the pong ball and two paddles to the screen
        pong.draw(window)
        player.draw(window)
        opponent.draw(window)

        #if neither player or bot haven't reached the score limit then the game will continue.
        if playerScore < 7 and opponentScore < 7:

            pong.checkCollision(player,opponent) #checks if pong hit a paddle
            player.update() #updates the player paddle. i.e. moves it to the new location based on user input

            #moves the computer paddle based on the location of the ball location.
            opponent.speed = 0
            if opponent.top < pong.center[1]:
                opponent.speed += 7
            elif opponent.bottom > pong.center[1]:
                opponent.speed -= 7


            pong.updateBall() #updates the pong ball
            opponent.update() #updates the opponent/ball paddle

            #checks to see if the pong ball hit a wall. If so then it will increment the score for either the player or bot.
            #also re-centers the paddles, the pong ball and randomizes its direction.
            if pong.checkWallHit():
                if pong.x < Screen[0]/2:
                    opponentScore += 1
                else:
                    playerScore += 1
                pong.center = (Screen[0]/2,Screen[1]/2)
                player.center = (player.center[0], Screen[1]/2)
                opponent.center = (opponent.center[0], Screen[1]/2)
                pong.newDir()
        #if the score limit is reached then it will draw the game over message and display the buttons. It will also allow the user
        #to select the buttons
        else:
            gameDone = True
            endDisplay = ''
            endMessage = ''
            pg.draw.rect(window, (60,60,60), endRect,0)
            if playerScore == 7:
                endDisplay = 'Player has won!'
                endMessage = font.render(endDisplay, 1, (255, 207, 33))
            else:
                endDisplay = 'Bot has won!'
                endMessage = font.render(endDisplay, 1, (48, 246, 252))
            window.blit(endMessage, (Screen[0]/2-endMessage.get_width()/2, endRect.y + endMessage.get_height()+5))
            menuButton.draw(window)
            replayButton.draw(window)


        pg.display.update()
        clock.tick(60)


#this function runs the 2-player version of the singleplayer gamemode. It allows for additional keyboard input so that two people can play locally.
def multiRun():
    #component creation needed for the game.
    pong = ball((25, 252, 181), Screen[0]/2, Screen[1]/2, 30)
    player1 = paddle((255, 207, 33), 20, Screen[1]/2)
    player2 = paddle((48, 246, 252), Screen[0]-30, Screen[1]/2)
    player1Score = player2Score = 0

    #makes the rectangle that the menu&replay button will be in along with button creation.
    endRect = pg.Rect(Screen[0]/2-250,Screen[1]/2-150, 500,300)
    menuButton = button((255, 207, 33), endRect.x + 20, endRect.y + 200, 150, 75, 'Menu')
    replayButton = button ((48, 246, 252), endRect.x+endRect.width - 170, endRect.y + 200, 150, 75, 'Replay')

    #multiplayer game loop. Runs while it is being viewed.
    viewing = True
    gameDone = False
    while viewing:
        #checks all of the events in the game to see if it has been exited, if the user is returning to the menu after the game,
        #if a button is being hovered over it, and if user is providing keyboard input.
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            #moves the players up/down depending on the key input.
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    player1.speed -= 7
                if event.key == pg.K_s:
                    player1.speed += 7
                if event.key == pg.K_UP:
                    player2.speed -= 7
                if event.key == pg.K_DOWN:
                    player2.speed += 7
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    player1.speed += 7
                if event.key == pg.K_s:
                    player1.speed -= 7
                if event.key == pg.K_UP:
                    player2.speed += 7
                if event.key == pg.K_DOWN:
                    player2.speed -= 7
            #allows the player to select the buttons after the game is done.
            if event.type == pg.MOUSEBUTTONDOWN and gameDone:
                #deletes the components and returns to the game menu.
                if menuButton.isOver(pos):
                    del pong
                    del player1
                    del player2
                    del endRect
                    del menuButton
                    del replayButton
                    viewing = False
                    mainMenu()
                #resets the game components and scores so that another game starts.
                if replayButton.isOver(pos):
                    player1.resetPos()
                    opponent.resetPos()
                    player1Score = 0
                    opponentScore = 0
                    gameDone = False
            #highlights the button when being hovered over.
            if event.type == pg.MOUSEMOTION:
                if replayButton.isOver(pos):
                    replayButton.color = (2, 201, 207)
                else:
                    replayButton.color = (48, 246, 252)
                if menuButton.isOver(pos):
                    menuButton.color = (222, 174, 0)
                else:
                    menuButton.color = (255, 207, 33)

        #creates the background and draws the score to the window.
        window.fill((35,35,35))
        pg.draw.line(window, (100,100,100), (Screen[0]/2,0), (Screen[0]/2,Screen[1]), 3)
        scoreString = str(player1Score)
        scoreDisplay = scoreFont.render(scoreString, 1 , (100,100,100))
        window.blit(scoreDisplay, (Screen[0]/4-scoreDisplay.get_width(), Screen[1]/2-scoreDisplay.get_height()/2))

        scoreString = str(player2Score)
        scoreDisplay = scoreFont.render(scoreString, 1 , (100,100,100))
        window.blit(scoreDisplay, (Screen[0]-Screen[0]/4-scoreDisplay.get_width(), Screen[1]/2-scoreDisplay.get_height()/2))

        #draws the pong ball and two paddles to the screen
        pong.draw(window)
        player1.draw(window)
        player2.draw(window)

        #if neither player has reached the score limit then the game will continue.
        if player1Score < 7 and player2Score < 7:

            pong.checkCollision(player1,player2) #checks if pong hit a paddle
            player1.update() #updates the player paddle. i.e. moves it to the new location based on user input
            player2.update() #updates the player2 paddle
            pong.updateBall() #updates the pong ball

            #checks to see if the pong ball hit a wall. If so then it will increment the score for either the player1 or player2.
            #also re-centers the paddles, the pong ball and randomizes its direction.
            if pong.checkWallHit():
                if pong.x < Screen[0]/2:
                    player2Score += 1
                else:
                    player1Score += 1
                pong.center = (Screen[0]/2,Screen[1]/2)
                player1.center = (player1.center[0], Screen[1]/2)
                player2.center = (player2.center[0], Screen[1]/2)
                pong.newDir()

        #if the score limit is reached then it will draw the game over message and display the buttons. It will also allow the user
        #to select the buttons
        else:
            gameDone = True
            endDisplay = ''
            endMessage = ''
            pg.draw.rect(window, (60,60,60), endRect,0)
            if player1Score == 7:
                endDisplay = 'Player 1 has won!'
                endMessage = font.render(endDisplay, 1, (255, 207, 33))
            else:
                endDisplay = 'Player 2 has won!'
                endMessage = font.render(endDisplay, 1, (48, 246, 252))
            window.blit(endMessage, (Screen[0]/2-endMessage.get_width()/2, endRect.y + endMessage.get_height()+5))
            menuButton.draw(window)
            replayButton.draw(window)


        pg.display.update()
        clock.tick(60)



def main():

    pg.display.set_caption("Pong")
    pg.display.flip()
    mainMenu()


main()
