import random
import genetic_algorithm as ga
from game_simulation import SnakeGame
from genetic_algorithm import N_PARENTS, POPULATION_SIZE, ITERATIONS
from neural_network import NeuralNetwork,WEIGHTS_ROW_SIZE

import numpy as np

def learn_snake_nn():
    # initialize the population
    population = [NeuralNetwork() for i in range(POPULATION_SIZE)]
    best_score = 0
    best_nn = None
    for i in range(ITERATIONS):
        # calculate the fitness of generation
        population_fitness_tuples = ga.fitness(population)

        # perform selection
        parents,new_score,new_best_nn = ga.selection(population_fitness_tuples,best_score)

        if new_score > best_score:
            best_score = new_score
            best_nn = new_best_nn

        best_of_generation_tup = sorted(population_fitness_tuples,key=lambda x: x[1],reverse=True)[0]

        # play the game with the best of generation
        if best_of_generation_tup[1] > 50:
            SnakeGame(best_of_generation_tup[0]).play_game(gui=True)

        print(f"Iteration {i}: Best fitness for this generation: {best_of_generation_tup[1]}, Best so far: {best_score}")

        #perform crossover to get the new population
        population = ga.crossover(parents,best_nn)



if __name__ == '__main__':
    learn_snake_nn()
    # SnakeGame(NeuralNetwork()).play_game(gui=True)

# # print(WEIGHTS_ROW_SIZE)
# nns = [NeuralNetwork() for i in range(POPULATION_SIZE)]
#
#
# # nn = NeuralNetwork(weights=test_array)
#
# # arr = nn.output_weights()
#
# # offsprings = crossover(nns)
# # for k in range(50):
# #     print(offsprings[k].predict_snake_direction(np.array([random.uniform(0,1) for i in range(7)]).reshape(-1, 7)))
#
# # e = selection(nns,list(range(POPULATION_SIZE)))
# for nn in nns:
#     print(SnakeGame(nn).play_game())
#
# k = 0