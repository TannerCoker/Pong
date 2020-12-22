'''
'''

import pygame as pg
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
    speedx = 7
    speedy = 7
    def __init__(self, color, x, y, radius):
        super().__init__(x, y,radius,radius)
        self.color = color
        self.radius = radius

    #draws the ball to the window
    def draw(self, window):
        pg.draw.ellipse(window, self.color, self, self.radius)

    #moves the balls x,y pos. If it hits a boundary then it bounces off of it.
    def updateBall(self):
        self.x += self.speedx
        self.y += self.speedy
        if self.x+self.radius >= Screen[0] or self.x <= 0:
            self.speedx *= -1
        if self.y+self.radius >= Screen[1] or self.y <= 0:
            self.speedy *= -1

    #checks to see if it hits one of the paddles. If so, then it bounces off of it
    def checkCollision(self, rect1, rect2):
        if self.colliderect(rect1) or self.colliderect(rect2):
            self.speedx *= -1



class paddle(pg.Rect):
    speed = 0
    def __init__(self, color, x, y):
        super().__init__(x,y-75,10,150)
        self.color = color

    def draw(self, window):
        pg.draw.rect(window, self.color, self)

    def update(self):
        self.y += self.speed
        if self.top <= 0:
            self.top = 0
        if self.bottom >= Screen[1]:
            self.bottom = Screen[1]




font = pg.font.SysFont('comicsans', 60)
def mainMenu():
    singleButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]/2-150,buttonWidth,buttonHeight, '1 Player')
    multiButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]/2,buttonWidth,buttonHeight,'2 Player')
    quitButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]-buttonHeight-75, buttonWidth, buttonHeight, 'Exit')
    title = font.render('PONG', 1, (255,255,255))

    b = ball((25, 252, 181), Screen[0]/2, Screen[1]/2, 30)
    viewing = True
    while viewing:
        window.fill((35,35,35))
        b.draw(window)
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
                    del b
                    pg.quit()
                    quit()
                if singleButton.isOver(pos):
                    del b
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
        b.updateBall()
        clock.tick(60)
        pg.display.update()




def singleRun():
    b = ball((25, 252, 181), Screen[0]/2, Screen[1]/2, 30)
    player = paddle((255, 207, 33), 20, Screen[1]/2)
    opponent = paddle((48, 246, 252), Screen[0]-30, Screen[1]/2)
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

        b.draw(window)
        player.draw(window)
        opponent.draw(window)
        b.checkCollision(player,opponent)
        player.update()
        opponent.speed = 0
        if opponent.top < b.y:
            opponent.speed += 7
        if opponent.bottom > b.y:
            opponent.speed -= 7
        opponent.update()
        b.updateBall()

        pg.display.update()
        clock.tick(60)

def main():

    pg.display.set_caption("Pong")
    pg.display.flip()
    mainMenu()


main()
