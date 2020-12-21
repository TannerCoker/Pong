'''
'''

import pygame as pg
pg.init()

Screen = (1500, 900)
window = pg.display.set_mode(Screen)
buttonWidth = 200
buttonHeight = 75
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



singleButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]/2-150,buttonWidth,buttonHeight, '1 Player')
multiButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]/2,buttonWidth,buttonHeight,'2 Player')
quitButton = button((0,0,255), Screen[0]/2-buttonWidth/2,Screen[1]-buttonHeight-75, buttonWidth, buttonHeight, 'Exit')
font = pg.font.SysFont('comicsans', 60)
title = font.render('PONG', 1, (255,255,255))
def mainMenu():

    viewing = True
    while viewing:
        window.fill((35,35,35))
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
                    pg.quit()
                    quit()
                if singleButton.isOver(pos):
                    viewing = False
                    print('clicked')
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

        pg.display.update()

def gameRun():
    viewing = True
    print('run')
    while viewing:
        window.fill((255,255,255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        pg.display.update()

def main():

    pg.display.set_caption("Pong")
    pg.display.flip()
    mainMenu()


main()
