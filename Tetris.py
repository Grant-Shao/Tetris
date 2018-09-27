#-*- coding:utf-8 -*-
from pyglet.gl import *
import pyglet
import random

def Vector(list1, list2, list3=[]):
    if list3==[]:
        if len(list1)==len(list2):
            list0=[]
            for i in range(len(list1)):
                list0.append(list1[i]+list2[i])
            return list0
        else:
            return 'two lists with different length'
    else:
        if len(list1)==len(list2)==len(list3):
            list0=[]
            for i in range(len(list1)):
                list0.append(list1[i]+list2[i]+list3[i])
            return list0
        else:
            return 'three lists with different length'

class Rect():
    def __init__(self, x, y, width, height, color=0):
        super(Rect, self).__init__()
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.color=color
        self.fix=False
        self.draw()
    
    def draw(self):
        if self.color==1:
            pyglet.graphics.draw(4, GL_QUADS,
            ('v2f', (self.x,self.y,self.x+self.width,self.y,self.x+self.width,self.y+self.height,self.x,self.y+self.height)), 
            ('c3B', (255, 255,255, 
                            255, 255,255, 
                            255, 255,255, 
                            255, 255,255)))
            pyglet.graphics.draw(4,GL_LINE_LOOP,
            ('v2f', (self.x,self.y,self.x+self.width,self.y,self.x+self.width,self.y+self.height,self.x,self.y+self.height)), 
            ('c3B', (0, 0,255, 
                            0, 0,255,
                            0, 0,255,
                            0, 0,255)))
        elif self.color==0:
            pyglet.graphics.draw(4,GL_LINE_LOOP,
            ('v2f', (self.x,self.y,self.x+self.width,self.y,self.x+self.width,self.y+self.height,self.x,self.y+self.height)),
            ('c3B', (0, 0,255,
                            0, 0,255,
                            0, 0,255,
                            0, 0,255)))

class Player():
    def __init__(self):
        super(Player, self).__init__()
        self.CurrRow=17
        self.CurrCol=4
        self.target=[]
        self.shape=[[0,0,0,0,
                        0,1,1,0,
                        0,0,1,1,
                        0,0,0,0], 
                        
                        [0,0,0,0,
                        0,1,1,0,
                        1,1,0,0,
                        0,0,0,0],
                        
                        [0,1,0,0,
                        0,1,0,0,
                        0,1,0,0,
                        0,1,0,0],
                        
                        [0,1,0,0,
                        0,1,0,0,
                        0,1,1,0,
                        0,0,0,0],
                        
                        [0,0,1,0,
                        0,0,1,0,
                        0,1,1,0,
                        0,0,0,0],
                        
                        [0,1,0,0,
                        0,1,1,0,
                        0,1,0,0,
                        0,0,0,0],
                        
                        [0,0,0,0,
                        0,1,1,0,
                        0,1,1,0,
                        0,0,0,0]]
    
    def Pending(self):
        self.targetReady=random.choice(self.shape)
    
    def Create(self):
        self.CurrRow=17
        self.CurrCol=4
        self.target=[]
        self.target=self.targetReady

class Game(pyglet.window.Window):
    def __init__(self):
        super(Game,self).__init__(width=550, height=600, resizable=False)
        self.score=0
        self.Menu()
        self.key='off'
        self.columns=12
        self.rows=21
        self.bricks={}
        self.push_handlers()
        self.player=Player()
        for r in range(self.rows):
            for c in range(self.columns):
                self.bricks['{:0>2}'.format(r)+'{:0>2}'.format(c)]=Rect(50+c*25, 50+r*25, 25., 25., 0)
        self.helper={}
        for r in range(4):
            for c in range(4):
                self.helper['{:0>2}'.format(r)+'{:0>2}'.format(c)]=Rect(400+c*25, 350+r*25, 25., 25., 0)

    def Menu(self):
        self.startLabel=pyglet.text.Label('Press S to start...',
                                                  font_name='Arial',
                                                  font_size=24,
                                                  x=self.width/2, y=self.height/2,
                                                  width=140,
                                                  align='center', 
                                                  anchor_x='center', 
                                                  anchor_y='center',
                                                  multiline=False)
        self.scoreLabel=pyglet.text.Label('score:'+str(self.score),
                                                  font_name='Arial',
                                                  font_size=16,
                                                  x=self.width*8/10, y=self.height*9/10,
                                                  width=140,
                                                  align='right', 
                                                  anchor_x='center', 
                                                  anchor_y='center',
                                                  multiline=False)

    def start(self):
        self.key='on'
        self.score=0
        self.player.Pending()
        self.player.Create()
        self.player.Pending()
        for r in range(self.rows):
                for c in range(self.columns):
                    self.Brick(r, c).fix=False
                    self.Brick(r, c).color=0
        pyglet.clock.schedule_interval(self.process, 1)
    
    def process(self, dt):
        #running with interval pace
        for c in range(12):
            if self.Brick(16, c).fix==True:
                pyglet.clock.unschedule(self.process)
                self.key='off'
                return False
        if self.CheckWall('bottom')==False:
            if self.CheckMove('bottom')==True:
                self.player.CurrRow-=1
        self.RemoveRow()
    
    def Pending(self):
        #generate the shape for next roound as preparation
        for r in range(4):
            for c in range(4):
                self.helper['{:0>2}'.format(r)+'{:0>2}'.format(c)].color=self.player.targetReady[4*(3-r)+c]
                self.helper['{:0>2}'.format(r)+'{:0>2}'.format(c)].draw()
    
    def on_draw(self):
        self.clear()
        if self.key=='on':
            for r in range(self.rows):
                for c in range(self.columns):
                    if self.Brick(r, c).fix==False:
                        if self.player.CurrRow<=r<self.player.CurrRow+4 and self.player.CurrCol<=c<self.player.CurrCol+4:
                            self.Brick(r, c).color=self.player.target[self.c2i(r-self.player.CurrRow, c-self.player.CurrCol)]
                        else:
                            self.Brick(r, c).color=0
                    self.Brick(r, c).draw()
            self.Pending()
            if self.CheckWall('bottom')==True or self.CheckMove('bottom')==False:
                self.SetFix()
            self.scoreLabel.text='score:'+str(self.score)
            self.scoreLabel.draw()
        else:
            for r in range(self.rows):
                for c in range(self.columns):
                    self.Brick(r, c).draw()
            for _, helper in self.helper.items():
                helper.draw()
            self.scoreLabel.draw()
            self.startLabel.draw()
                    
    def on_key_press(self, symbol, modifiers):
        if self.key=='on':
            if symbol==65362:  #up
                a=self.player.target
                #rotate
                b=[a[12], a[8], a[4], a[0], 
                    a[13], a[9], a[5], a[1],
                    a[14], a[10], a[6], a[2], 
                    a[15], a[11], a[7], a[3]]
                #check if new shape coordinates lay outside the canvas
                if self.player.CurrCol>0:
                    if self.player.CurrCol<=8 or \
                        (self.player.CurrCol<=10 and sum(b[2::4])==0) or \
                        (self.player.CurrCol<=9 and sum(b[3::4])==0):
                        self.player.target=b
                if self.player.CurrCol<8:
                    if self.player.CurrCol>=0 or \
                        (self.player.CurrCol>=-1 and sum(b[::4])==0) or\
                        (self.player.CurrCol>=-2 and sum(b[1::4])==0):
                        self.player.target=b
            elif symbol==65364:  #down
                if self.CheckWall('bottom')==False:
                    if self.CheckMove('bottom')==True:
                        self.player.CurrRow-=1
                        if self.CheckWall('bottom')==False:
                            if self.CheckMove('bottom')==True:
                                self.player.CurrRow-=1
            elif symbol==65361:  #left
                if self.CheckWall('left')==False:
                    if self.CheckMove('left')==True:
                        self.player.CurrCol-=1
            elif symbol==65363:  #right
                if self.CheckWall('right')==False:
                    if self.CheckMove('right')==True:
                        self.player.CurrCol+=1
        elif symbol==115:
                self.start()
            
    def Brick(self, r, c):
        #base on its row and column, return its object
        return self.bricks['{:0>2}'.format(r)+'{:0>2}'.format(c)]
    
    def c2i(self, r, c):
        #coordinates to index, r,c from left bottom to right up, index is from left up to right bottom
        return 4*(3-r)+c

    def i2c(self, index):
        #index to coordinates, coordinates from left bottom to up right, index from up left to right bottom
        return [(4-index//4)-1,index%4]
        
    def RectObj(self, r, c, index):
        #convert player coordinates to brick's coordinates
        row=r+(4-index//4)-1
        column=r+index%4
        return ['{:0>2}'.format(row)+'{:0>2}'.format(column), row, column]

    def SetFix(self):
        x=0
        for each in self.player.target:
            if each==1:
                self.Brick(*Vector([self.player.CurrRow, self.player.CurrCol], self.i2c(x))).fix=True
                self.Brick(*Vector([self.player.CurrRow, self.player.CurrCol], self.i2c(x))).color=1
            x+=1
        self.player.Create()
        self.player.Pending()
        
    def CheckWall(self, side):
        #check bottom  a[::-1]
        if side=='bottom':
            #a[12:16] , a[8:12]
            if max(self.player.target[12:16])==1 and self.player.CurrRow==0:
                return True
            elif max(self.player.target[8:12])==1 and self.player.CurrRow==-1:
                return True
            elif self.player.CurrRow==-2:
                return True
            else:
                return False
        elif side=='left':
            #check left  a[::4]+a[1::4]+a[2::4]+a[3::4]
            if max(self.player.target[::4])==1 and self.player.CurrCol==0:
                return True
            elif max(self.player.target[1::4])==1 and self.player.CurrCol==-1:
                return True
            elif self.player.CurrCol==-2:
                return True
            else:
                return False    
        elif side=='right':
            #check right  a[3::4]+a[2::4]+a[1::4]+a[::4]
            if max(self.player.target[3::4])==1 and self.player.CurrCol==8:
                return True
            elif max(self.player.target[2::4])==1 and self.player.CurrCol==9:
                return True
            elif self.player.CurrCol==10:
                return True
            else:
                return False

    def CheckMove(self, side):
        if side=='right':
            x=0
            for each in self.player.target:
                if each==1:
                    if self.Brick(*Vector(self.i2c(x), [self.player.CurrRow, self.player.CurrCol], [0, 1])).fix==True:
                        return False
                x+=1
            return True
        elif side=='left':
            x=0
            for each in self.player.target:
                if each==1:
                    if self.Brick(*Vector(self.i2c(x), [self.player.CurrRow, self.player.CurrCol], [0, -1])).fix==True:
                        return False
                x+=1
            return True
        elif side=='bottom':
            x=0
            for each in self.player.target:
                if each==1:
                    if self.Brick(*Vector(self.i2c(x), [self.player.CurrRow, self.player.CurrCol], [-1, 0])).fix==True:
                        return False
                x+=1
            return True

    def RemoveRow(self):
        for r in range(16):
            sum=0
            for c in range(self.columns):
                sum=sum+self.Brick(r, c).color
            if sum==12:
                self.score+=100
                for rr in range(r, 16):
                    for cc in range(self.columns):
                        self.Brick(rr, cc).color=self.Brick(rr+1, cc).color
                        self.Brick(rr, cc).fix=self.Brick(rr+1, cc).fix

if __name__ == "__main__":
    Game()
    pyglet.app.run()
    
