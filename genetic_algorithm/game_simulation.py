import random

import time
import numpy as np

import contextlib
with contextlib.redirect_stdout(None):
    import pygame

from copy import copy

class SnakeGame:

    def __init__(self,neural_network,size=(20,20),max_steps=3000):
        self.size = size
        self.max_steps = max_steps
        self.neural_network = neural_network
        self.fitness = 0

        self.window_width = self.window_height = 880
        self.step = self.window_height / size[0]
        # snake is a list of coordinates where the of it is
        self.snake = self.init_snake()
        self.food = [4,9]

        # direction is from 0 to 3 in clockwise
        #   1
        # 0 S 2
        #   3
        self.direction = 1



    def play_game(self,gui=False):

        fitness = 0.
        previous_direction = 0

        if gui:
            self.on_init()

        for _ in range(self.max_steps):

            if gui:
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    break
            # check if we are blocked in any directions and get the direction vectors of head of the snake and the apple
            front_blocked, left_blocked, right_blocked = self.blocked_directions()
            apple_direction_vector, snake_direction_vector = self.direction_vectors()

            # input the snake arguments to the neural network to get the next turn

            turn = self.neural_network.predict_snake_direction(np.array([front_blocked,left_blocked,right_blocked,
                                                                        apple_direction_vector[0],apple_direction_vector[1],
                                                                        snake_direction_vector[0],snake_direction_vector[1]]))

            # turn the snake and save previous direction
            previous_direction = self.direction
            self.change_direction(turn)

            # check for collision with self or the wall and end the game + penalise
            if self.check_if_blocked():
                fitness -= 50 # penalise if it crashes with itself
                break

            # check if the food is eaten, then move and extend the snake + generate new food
            if self.check_if_food_eaten():
                self.move_snake(False)
                self.food = self.generate_new_food()
                # reward if it eats the food
                fitness += 10
            else:
                self.move_snake(True)

            # check if we moved towards the food or away -> reward or penalize
            if self.moved_toward_food():
                fitness += 1
            else:
                fitness -= 1.5

            if gui:
                self.on_render()
                time.sleep(50.0 / 1000.0)
            # print(f"Direction: {self.direction} | snake: {self.snake}")
        self.on_cleanup()
        return fitness


    def blocked_directions(self):

        front_blocked = 1 if self.check_if_blocked() else 0

        # check if left is blocked
        self.change_direction(-1)
        left_blocked = 1 if self.check_if_blocked() else 0
        self.change_direction(1)

        # check if right is blocked
        self.change_direction(1)
        right_blocked = 1 if self.check_if_blocked() else 0
        self.change_direction(-1)

        return front_blocked,left_blocked,right_blocked

    def direction_vectors(self):
        snake_direction_vector = np.array(self.snake[1]) - np.array(self.snake[0])
        apple_direction_vector = np.array(self.food) - np.array(self.snake[0])
        norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
        norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)
        if norm_of_apple_direction_vector == 0:
            norm_of_apple_direction_vector = 10
        if norm_of_snake_direction_vector == 0:
            norm_of_snake_direction_vector = 10

        apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
        snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector

        return apple_direction_vector_normalized, snake_direction_vector_normalized

    # check if the snake moved towards food
    def moved_toward_food(self):
        dist_now = abs(self.snake[0][0] - self.food[0]) + abs(self.snake[0][1] - self.food[1])
        dist_before = abs(self.snake[1][0] - self.food[0]) + abs(self.snake[1][1] - self.food[1])
        return dist_now < dist_before

    def check_if_blocked(self):
        return ((self.direction == 0 and self.snake[0][0] == 0) or
         (self.direction == 1 and self.snake[0][1] == 0) or
         (self.direction == 2 and self.snake[0][0] == self.size[0] - 1) or
         (self.direction == 3 and self.snake[0][1] == self.size[1] - 1) or
         self.new_head_pos() in self.snake)

    def generate_new_food(self):
        food_loc = [random.randint(1,self.size[0] - 1),random.randint(1,self.size[1] - 1)]
        # try to generate food outside the snake body
        while food_loc in self.snake:
            food_loc = [random.randint(1, self.size[0] - 1), random.randint(1, self.size[1] - 1)]
        return food_loc

    def init_snake(self):
        # (x,y)
        return [[4,10],[4,11],[4,12]]

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

    def draw_snake(self,surface,image):
        head = self._snake_head_up
        if self.direction == 0:
            head = self._snake_head_left
        elif self.direction == 1:
            head = self._snake_head_up
        elif self.direction == 2:
            head = self._snake_head_right
        elif self.direction == 3:
            head = self._snake_head_down

        surface.blit(head, (self.snake[0][0] * self.step, self.snake[0][1] * self.step))

        for i in range(1,len(self.snake)):
            surface.blit(image,(self.snake[i][0] * self.step,self.snake[i][1] * self.step))

    def draw_apple(self,surface,image):
        surface.blit(image, (self.food[0] * self.step, self.food[1] * self.step))

    def on_init(self):
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Italic', 30)
        self._display_surf = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE)

        pygame.display.set_caption('Smart snake')
        self._running = True
        self._image_surf = pygame.image.load("../game/assets/snake.png").convert()
        self._apple_surf = pygame.image.load("../game/assets/apple.png").convert()
        self._snake_head_up = pygame.image.load("../game/assets/snake_head_up.png").convert()
        self._snake_head_right = pygame.image.load("../game/assets/snake_head_right.png").convert()
        self._snake_head_down = pygame.image.load("../game/assets/snake_head_down.png").convert()
        self._snake_head_left = pygame.image.load("../game/assets/snake_head_left.png").convert()


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.draw_snake(self._display_surf,self._image_surf)
        self.draw_apple(self._display_surf, self._apple_surf)
        textsurface = self.myfont.render(
            'Score: ' + str(len(self.snake) - 2) + " | Press q to stop.",
            True, (255, 255, 255))
        self._display_surf.blit(textsurface, (3, 3))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()




