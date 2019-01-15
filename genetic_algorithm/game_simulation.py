from copy import copy


class SnakeGame:

    def __init__(self,size=(20,20),max_steps=1000):
        self.size = size
        self.max_steps = max_steps
        # snake is a list of coordinates where the of it is
        self.snake = self.init_snake()
        self.food = (10,10)

        # direction is from 0 to 3 in clockwise
        #   1
        # 0 S 2
        #   3
        self.direction = 1



    def play_game(self):

        for _ in range(self.max_steps):
            pass


    def init_snake(self):
        # (x,y)
        return [(4,4),(4,5),(4,6)]

    # turn is specified as -1 for turn left, 0 for go straight and 1 for turn right
    def change_direction(self,turn):
        if turn == 0: return
        elif turn == -1:
            self.direction = 3 if self.direction == 0 else self.direction - 1
        elif turn == 1:
            self.direction = 0 if self.direction == 3 else self.direction + 1
        else:
            exit(1)

    def move_snake(self,delete_end):
        # insert the new snake at the beggining and delete at the end if no apple was eaten
        self.snake.insert(0,self.new_head_pos())
        if delete_end:
            del self.snake[len(self.snake) - 1]

    def check_if_food_eaten(self):
        return self.new_head_pos() == self.food

    def new_head_pos(self):
        new_head = copy(self.snake[0])
        if self.direction == 0:
            new_head[0] -= 1
        elif self.direction == 1:
            new_head[1] -= 1
        elif self.direction == 2:
            new_head[0] += 1
        elif self.direction == 3:
            new_head[1] += 1
        return new_head

    def check_for_collision(self):
        # check for collision with the wall and with self
        return (self.direction == 0 and self.snake[0][0] == 0 or
                self.direction == 1 and self.snake[0][1] == 0 or
                self.direction == 2 and self.snake[0][0] == self.size[0] - 1 or
                self.direction == 3 and self.snake[0][1] == self.size[1] - 1 or
                self.new_head_pos() in self.snake)




