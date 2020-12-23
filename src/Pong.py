'''
'''

import pygame as pg
import random
pg.init()

Screen = (1500, 900)
window = pg.display.set_mode(Screen)
buttonWidth = 200
buttonHeight = 75

clock = pg.time.Clock()




#this class is to act as a button for the game. It will input an x,y-coor, a width&height and a text to display.
class button():
    def __init__(self, color, x,y,width,height,text =''):
        self.color=color
        self.x = x
        self.y = y
        self.width = width
        self.height=height
        self.text = text

    def draw(self, window, outline=None):
        if outline:
            pg.draw.rect(window, self.color, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pg.draw.rect(window, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pg.font.SysFont('comicsans', 45)
            text = font.render(self.text, 1, (0,0,0))
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

    #checks to see if it hits one of the paddles. If so, then it bounces off of it
    def checkCollision(self, rect1, rect2):
        if self.colliderect(rect1) or self.colliderect(rect2):
            self.speedx *= -1
            self.hitCounter += 1
            if self.hitCounter == 10:
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




font = pg.font.SysFont('comicsans', 60)
scoreFont = pg.font.SysFont('comicsans', 200)

def mainMenu():
    singleButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]/2-150,buttonWidth,buttonHeight, '1 Player')
    multiButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]/2,buttonWidth,buttonHeight,'2 Player')
    quitButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]-buttonHeight-75, buttonWidth, buttonHeight, 'Exit')
    title = font.render('PONG', 1, (255,255,255))

    pong = ball((25, 252, 181), Screen[0]/2, Screen[1]/2, 30)
    viewing = True
    while viewing:
        window.fill((35,35,35))
        pong.draw(window)
        singleButton.draw(window)
        multiButton.draw(window)
        quitButton.draw(window)
        window.blit(title, (Screen[0]/2-title.get_width()/2, 20))

        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if quitButton.isOver(pos):
                    del pong
                    pg.quit()
                    quit()
                if singleButton.isOver(pos):
                    del pong
                    viewing = False
                    singleRun()
            if event.type == pg.MOUSEMOTION:
                if singleButton.isOver(pos):
                    singleButton.color = (255,0,0)
                else:
                    singleButton.color = (0,0,255)
                if quitButton.isOver(pos):
                    quitButton.color = (255,0,0)
                else:
                    quitButton.color = (0,0,255)

        pong.updateBall()
        clock.tick(60)
        pg.display.update()




def singleRun():
    pong = ball((25, 252, 181), Screen[0]/2, Screen[1]/2, 30)
    player = paddle((255, 207, 33), 20, Screen[1]/2)
    opponent = paddle((48, 246, 252), Screen[0]-30, Screen[1]/2)
    playerScore = opponentScore = 0



    viewing = True
    while viewing:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
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

        window.fill((35,35,35))
        pg.draw.line(window, (100,100,100), (Screen[0]/2,0), (Screen[0]/2,Screen[1]), 3)
        scoreString = str(playerScore)
        scoreDisplay = scoreFont.render(scoreString, 1 , (100,100,100))
        window.blit(scoreDisplay, (Screen[0]/4-scoreDisplay.get_width(), Screen[1]/2-scoreDisplay.get_height()/2))

        scoreString = str(opponentScore)
        scoreDisplay = scoreFont.render(scoreString, 1 , (100,100,100))
        window.blit(scoreDisplay, (Screen[0]-Screen[0]/4-scoreDisplay.get_width(), Screen[1]/2-scoreDisplay.get_height()/2))

        pong.draw(window)
        player.draw(window)
        opponent.draw(window)
        if playerScore < 7 and opponentScore < 1:

            pong.checkCollision(player,opponent)
            player.update()
            opponent.speed = 0
            if opponent.top < pong.center[1]:
                opponent.speed += 7
            elif opponent.bottom > pong.center[1]:
                opponent.speed -= 7
            pong.updateBall()
            opponent.update()

            if pong.checkWallHit():
                if pong.x < Screen[0]/2:
                    opponentScore += 1
                else:
                    playerScore += 1
                pong.center = (Screen[0]/2,Screen[1]/2)
                player.center = (player.center[0], Screen[1]/2)
                opponent.center = (opponent.center[0], Screen[1]/2)
                pong.newDir()

        else:
            endDisplay = ''
            endRect = pg.Rect(Screen[0]/2-250,Screen[1]/2-150, 500,300)
            pg.draw.rect(window, (100,100,100), endRect,0)
            if playerScore == 7:
                endDisplay = 'Player has won!'
            else:
                endDisplay = 'Bot has won!'
            endMessage = font.render(endDisplay, 1, (35,35,35))
            window.blit(endMessage, (Screen[0]/2-endMessage.get_width()/2, endRect.y + endMessage.get_height()+5))

        pg.display.update()
        clock.tick(60)

def main():

    pg.display.set_caption("Pong")
    pg.display.flip()
    mainMenu()


main()
