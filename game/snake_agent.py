from copy import copy
from random import randint, random

#Actions
FORWARD = 0
LEFT = 1
RIGHT = 2

class snakeAgent():
  learingRate = 0.1
  discountFactor = 0.8
  greedyEpsilon = 1
  QTable = {}

  # Get current state of the agent.
  def getState(self, player, apple, game):
    # State is an array of values:
    # clearAhead
    # clearLeft
    # clearRight
    # appleAhead
    # appleLeft
    # appleRight

    tmpP = tmpPlayer(copy(player.x), copy(player.y), copy(player.step), copy(player.direction), copy(player.length))
    collisionAhead = self.isCollisionSelf(tmpP)
    # Right
    if player.direction is 0:
      tmpP = tmpPlayer(copy(player.x), copy(player.y), copy(player.step), 2, copy(player.length))
      tmpP = self.updatePosition(tmpP)
      collisionLeft = self.isCollisionSelf(tmpP)

      tmpP = tmpPlayer(copy(player.x), copy(player.y), copy(player.step), 3, copy(player.length))
      tmpP = self.updatePosition(tmpP)
      collisionRight = self.isCollisionSelf(tmpP)

      clearAhead = 0 if collisionAhead or self.isCollision(player.x[0] + player.step, player.y[0], game.windowWidth, player.y[0], 44) else 1
      clearLeft =  0 if collisionLeft or self.isCollision(player.x[0], player.y[0] - player.step, player.x[0], -44, 44) else 1
      clearRight = 0 if collisionRight or self.isCollision(player.x[0], player.y[0] + player.step, player.x[0], game.windowHeight, 44) else 1

      appleAhead = 1 if apple.y == player.y[0] else 0
      appleLeft = 1 if apple.y < player.y[0] else 0
      appleRight = 1 if apple.y > player.y[0] else 0

    # Left
    if player.direction is 1:
      tmpP = tmpPlayer(copy(player.x), copy(player.y), copy(player.step), 3, copy(player.length))
      tmpP = self.updatePosition(tmpP)
      collisionLeft = self.isCollisionSelf(tmpP)

      tmpP = tmpPlayer(copy(player.x), copy(player.y), copy(player.step), 2, copy(player.length))
      tmpP = self.updatePosition(tmpP)
      collisionRight = self.isCollisionSelf(tmpP)

      clearAhead = 0 if collisionAhead or self.isCollision(player.x[0] - player.step, player.y[0], -44, player.y[0], 44) else 1
      clearLeft =  0 if collisionLeft or self.isCollision(player.x[0], player.y[0] + player.step, player.x[0], game.windowHeight, 44) else 1
      clearRight =  0 if collisionRight or self.isCollision(player.x[0], player.y[0] - player.step, player.x[0], -44, 44) else 1

      appleAhead = 1 if apple.y == player.y[0] else 0
      appleLeft = 1 if apple.y > player.y[0] else 0
      appleRight = 1 if apple.y < player.y[0] else 0

    # Up
    if player.direction is 2:
      tmpP = tmpPlayer(copy(player.x), copy(player.y), copy(player.step), 1, copy(player.length))
      tmpP = self.updatePosition(tmpP)
      collisionLeft = self.isCollisionSelf(tmpP)

      tmpP = tmpPlayer(copy(player.x), copy(player.y), copy(player.step), 0, copy(player.length))
      tmpP = self.updatePosition(tmpP)
      collisionRight = self.isCollisionSelf(tmpP)

      clearAhead = 0 if collisionAhead or self.isCollision(player.x[0], player.y[0] - player.step, player.x[0], -44, 44) else 1
      clearLeft =  0 if collisionLeft or self.isCollision(player.x[0] - player.step, player.y[0], -44, player.y[0], 44) else 1
      clearRight =  0 if collisionRight or self.isCollision(player.x[0] + player.step, player.y[0], game.windowWidth, player.y[0], 44) else 1

      appleAhead = 1 if apple.x == player.x[0] else 0
      appleLeft = 1 if apple.x < player.x[0] else 0
      appleRight = 1 if apple.x > player.x[0] else 0

    # Down
    if player.direction is 3:
      tmpP = tmpPlayer(copy(player.x), copy(player.y), copy(player.step), 0, copy(player.length))
      tmpP = self.updatePosition(tmpP)
      collisionLeft = self.isCollisionSelf(tmpP)

      tmpP = tmpPlayer(copy(player.x), copy(player.y), copy(player.step), 1, copy(player.length))
      tmpP = self.updatePosition(tmpP)
      collisionRight = self.isCollisionSelf(tmpP)

      clearAhead = 0 if collisionAhead or self.isCollision(player.x[0], player.y[0] + player.step, player.x[0], -44, 44) else 1
      clearLeft =  0 if collisionLeft or self.isCollision(player.x[0] + player.step, player.y[0], game.windowWidth, player.y[0], 44) else 1
      clearRight =  0 if collisionRight or self.isCollision(player.x[0] - player.step, player.y[0], -44, player.y[0], 44) else 1

      appleAhead = 1 if apple.x == player.x[0] else 0
      appleLeft = 1 if apple.x > player.x[0] else 0
      appleRight = 1 if apple.x < player.x[0] else 0

    state = [
      clearAhead,
      clearLeft,
      clearRight,
      appleAhead,
      appleLeft,
      appleRight
    ]

    return state

  def rewardPlayer(self, state, futureState, action):
    # Set initial reward to 0.
    reward = 0

    if state != futureState:
      # Reward -1 if snake collided.
      if (state[0] == 0 and action == FORWARD) or (state[1] == 0 and action == LEFT) or (state[2] == 0 and action == RIGHT):
        reward = -1
      
      # Reward +1 if snake moved towards apple.
      if (state[0] == 1 and action == FORWARD and state[3] == 1) or (state[1] == 1 and action == LEFT and state[4] == 1) or (state[2] == 1 and action == RIGHT and state[5] == 1):
        reward = 1
      # if (state[0] == 1 and action == FORWARD and state[3] == 1):
      #   reward += 10
      # else:
      #   reward = -1
                    
      # Get the optimal learned future value for future state.
      optimalLearnedValue = max(self.getQ(futureState, FORWARD), self.getQ(futureState, LEFT), self.getQ(futureState, RIGHT))
      learnedValue = self.learingRate * ( reward + self.discountFactor * optimalLearnedValue - self.getQ(state, action))
      self.addQ(state, action, learnedValue)


  # Gets best action for current state.
  def getAction(self, state):
    qualityActions = []

    #Get Q values for current state.
    for action in range(3):
      qualityActions.append(qualityAction(action, self.getQ(state, action)))
      
    qualityActions.sort(key=lambda x: x.quality, reverse=True)

    # Include epsilon-greedy policy to ensure learing and exploration.
    if random() < self.greedyEpsilon:
      # if len(self.QTable) > 30:
      #   return qualityActions[0].action
      # else:
      self.greedyEpsilon *= 0.99
      return qualityActions[randint(0, 2)].action
    else:
      return qualityActions[0].action

  # Gets learned value for given state and action from Q table.
  def getQ(self, state, action):
    tmp = copy(state)
    tmp.append(action)
    tmp = map(str, tmp)    
    tmp = ''.join(tmp)

    return self.QTable.get(tmp, 0)


  # Adds new learned value to Q table for state and action.
  def addQ(self, state, action, learnedValue):
    tmp = copy(state)
    tmp.append(action)
    tmp = map(str, tmp)    
    tmp = ''.join(tmp)

    if tmp not in self.QTable:
      self.QTable[tmp] = 0
    else:
      self.QTable[tmp] += learnedValue



  # Helper functions
  def isCollision(self,x1, y1, x2, y2, bsize):
    if x1 >= x2 and x1 <= x2 + bsize-1:
      if y1 >= y2 and y1 <= y2 + bsize-1:
        return True
    return False

  def isCollisionSelf(self, tmpPlayer):
    for i in range(2, tmpPlayer.length):
      if self.isCollision(tmpPlayer.x[0], tmpPlayer.y[0], tmpPlayer.x[i], tmpPlayer.y[i], 40):
        return True
    return False

  def updatePosition(self, tmpPlayer):
    # Update previous positions
    for i in range(tmpPlayer.length-1, 0, -1):
      tmpPlayer.x[i] = tmpPlayer.x[i-1]
      tmpPlayer.y[i] = tmpPlayer.y[i-1]
 
    # Update position of head of snake
    if tmpPlayer.direction == 0:
      tmpPlayer.x[0] = tmpPlayer.x[0] + tmpPlayer.step
    if tmpPlayer.direction == 1:
      tmpPlayer.x[0] = tmpPlayer.x[0] - tmpPlayer.step
    if tmpPlayer.direction == 2:
      tmpPlayer.y[0] = tmpPlayer.y[0] - tmpPlayer.step
    if tmpPlayer.direction == 3:
      tmpPlayer.y[0] = tmpPlayer.y[0] + tmpPlayer.step

    return tmpPlayer


class tmpPlayer():
  def __init__(self, x, y, step, direction, length):
    self.x = x
    self.y = y
    self.step = step
    self.direction = direction
    self.length = length

class qualityAction():
  def __init__(self, action, quality):
    self.action = action
    self.quality = quality