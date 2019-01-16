# The base game is written with the help of Python Tutorials: https://pythonspot.com/snake-with-pygame/

from pygame.locals import *
from random import randint
from snake_agent import snakeAgent
import pygame
import time
 

WINDOW_W = 880
WINDOW_H = 880

HUMAN = 0
AGENT_Q = 1

class Apple:
    x = 0
    y = 0
    step = 44
 
    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y))

    def reset(self,x,y):
      self.x = x * self.step
      self.y = y * self.step
 
 
class Player:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length):
       self.length = length
       for i in range(0,2000):
           self.x.append(-100)
           self.y.append(-100)
 
       # initial positions, no collision.
       self.x[1] = 1*44
       self.x[2] = 2*44

    def reset(self):
      self.x = [0]
      self.y = [0]
      self.step = 44
      self.direction = 0
      self.length = 3
  
      self.updateCountMax = 2
      self.updateCount = 0

      for i in range(0,2000):
        self.x.append(-100)
        self.y.append(-100)
 
      # initial positions, no collision.
      self.x[1] = 1*44
      self.x[2] = 2*44

 
    def update(self):
 
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:
 
            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]
 
            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step
 
            self.updateCount = 0
 
 
    def moveRight(self):
      if self.direction is not 1:
        self.direction = 0
 
    def moveLeft(self):
      if self.direction is not 0:
        self.direction = 1
 
    def moveUp(self):
      if self.direction is not 3:
        self.direction = 2
 
    def moveDown(self):
      if self.direction is not 2:
        self.direction = 3 
 
    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 
 
class Game:
    def isCollision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize-1:
            if y1 >= y2 and y1 <= y2 + bsize-1:
                return True
        return False
 
class App:
    gameMode = AGENT_Q
    windowWidth = WINDOW_W
    windowHeight = WINDOW_H
    player = 0
    apple = 0
 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(3) 
        self.apple = Apple(5,5)

    def restart(self):
      self.player.reset()
      self._running = True
      self._display_surf = None
      self._image_surf = None
      self._apple_surf = None
  
      self.on_init()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('Smart snake')
        self._running = True
        self._image_surf = pygame.image.load("assets/snake.png").convert()
        self._apple_surf = pygame.image.load("assets/apple.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        self.player.update()

        print('X:', self.player.x[0])
        print('Y:', self.player.y[0])
        print('----------------------')

        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.apple.x, self.apple.y, self.player.x[i], self.player.y[i], 44):
                self.apple.x = randint(2,9) * 44
                self.apple.y = randint(2,9) * 44
                self.player.length = self.player.length + 1
 
 
        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],self.player.x[i], self.player.y[i],40):
                print("Collision: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                
                if self.gameMode == AGENT_Q:
                  self.restart()
                else:
                  exit(0)

        # Left side collision check.
        if self.game.isCollision(self.player.x[0],self.player.y[0], -44, self.player.y[0], 44):
          print("Collision left side:", self.player.x[0], ',', self.player.y[0])

          if self.gameMode == AGENT_Q:
            self.restart()
          else:
            exit(0)

        # Right side collision check.
        if self.game.isCollision(self.player.x[0], self.player.y[0], WINDOW_W, self.player.y[0], 44):
          print("Collision right side:", self.player.x[0], ',', self.player.y[0])

          if self.gameMode == AGENT_Q:
            self.restart()
          else:
            exit(0)
          

        # Top side collision check.
        if self.game.isCollision(self.player.x[0], self.player.y[0], self.player.x[0], -44, 44):
          print("Collision top side:", self.player.x[0], ',', self.player.y[0])
          
          if self.gameMode == AGENT_Q:
            self.restart()
          else:
            exit(0)

        # Bottom side collision check.
        if self.game.isCollision(self.player.x[0], self.player.y[0], self.player.x[0], WINDOW_H, 44):
          print("Collision bottom side:", self.player.x[0], ',', self.player.y[0])
          
          if self.gameMode == AGENT_Q:
            self.restart()
          else:
            exit(0)

        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
      if self.on_init() == False:
          self._running = False

      if self.gameMode == HUMAN:
        while( self._running ):
          
          state = agent.getState(self.player, self.apple, self)
          print(state)


          pygame.event.pump()
          keys = pygame.key.get_pressed() 
          if (keys[K_RIGHT]):
              self.player.moveRight()
          if (keys[K_LEFT]):
              self.player.moveLeft()
          if (keys[K_UP]):
              self.player.moveUp()
          if (keys[K_DOWN]):
              self.player.moveDown()
          if (keys[K_ESCAPE]):
              self._running = False
          self.on_loop()
          self.on_render()
          time.sleep (50.0 / 1000.0)
        self.on_cleanup()
      
      elif self.gameMode == AGENT_Q:
        while(self._running):
          pygame.event.pump()

          state = agent.getState(self.player, self.apple, self)
          action = agent.getAction(state)

          if self.player.direction == 0:
            if action == 1:
              self.player.moveUp()
            elif action == 2:
              self.player.moveDown()
          
          elif self.player.direction == 1:
            if action == 1:
              self.player.moveDown()
            elif action == 2:
              self.player.moveUp()
          
          elif self.player.direction == 2:
            if action == 1:
              self.player.moveLeft()
            elif action == 2:
              self.player.moveRight()

          elif self.player.direction == 3:
            if action == 1:
              self.player.moveRight()
            elif action == 2:
              self.player.moveLeft()
            
          newState = agent.getState(self.player, self.apple, self)
          agent.rewardPlayer(state, newState, action)

          print(state)

          self.on_loop()
          self.on_render()
          time.sleep (5.0 / 1000.0)

 
if __name__ == "__main__" :
    agent  = snakeAgent()
    theApp = App()
    theApp.on_execute()