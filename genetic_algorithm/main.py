import random
import genetic_algorithm as ga
from game_simulation import SnakeGame
from genetic_algorithm import N_PARENTS, POPULATION_SIZE, ITERATIONS
from neural_network import NeuralNetwork,WEIGHTS_ROW_SIZE

import numpy as np

def learn_snake_nn():
    # initialize the population
    population = [NeuralNetwork() for i in range(POPULATION_SIZE)]

    for i in range(ITERATIONS):
        # calculate the fitness of generation
        population_fitness_tuples = ga.fitness(population)

        print(f"Iteration {i}: Best fitness: {sorted(population_fitness_tuples,key=lambda x: x[1],reverse=True)[0][1]}")
        # perform selection
        parents = ga.selection(population_fitness_tuples)

        #perform crossover to get the new population
        population = ga.crossover(parents)



if __name__ == '__main__':
    learn_snake_nn()

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