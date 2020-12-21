'''
'''

import pygame as pg
pg.init()

Screen = (1500, 900)
window = pg.display.set_mode(Screen)
buttonWidth = 200
buttonHeight = 75

clock = pg.time.Clock()
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

class ball():
    speedx = 7
    speedy = 7
    def __init__(self, color, x, y, radius):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, window):
        pg.draw.circle(window, self.color, (self.x,self.y),self.radius)

    def updateBall(self):
        self.x += self.speedx
        self.y += self.speedy
        if self.x+self.radius > Screen[0] or self.x-self.radius < 0:
            self.speedx *= -1
        if self.y+self.radius > Screen[1] or self.y-self.radius < 0:
            self.speedy *= -1

singleButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]/2-150,buttonWidth,buttonHeight, '1 Player')
multiButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]/2,buttonWidth,buttonHeight,'2 Player')
quitButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]-buttonHeight-75, buttonWidth, buttonHeight, 'Exit')
font = pg.font.SysFont('comicsans', 60)
title = font.render('PONG', 1, (255,255,255))
def mainMenu():
    b = ball((25, 252, 181), Screen[0]/2, Screen[1]/2, 20)
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
                    gameRun()
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

def gameRun():
    b = ball((25, 252, 181), Screen[0]/2, Screen[1]/2, 20)
    viewing = True
    while viewing:
        window.fill((35,35,35))
        b.draw(window)
        b.updateBall()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        pg.display.update()
        clock.tick(60)

def main():

    pg.display.set_caption("Pong")
    pg.display.flip()
    mainMenu()


main()
