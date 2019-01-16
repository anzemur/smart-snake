import os
import psutil
import numpy as np
import random

from game_simulation import SnakeGame
from neural_network import WEIGHTS_ROW_SIZE, NeuralNetwork
from concurrent.futures import ProcessPoolExecutor



POPULATION_SIZE = 150
N_PARENTS = 15
MUTATION_PROB = 0.07
ITERATIONS = 700

best_score = 0
best_nn = None

def limit_cpu():
    p = psutil.Process(os.getpid())
    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)


def fitness(population):
    # Spread the workload among the cores of processors to speed up processing
    pop_fit_tuple = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        for fit,nn in zip(executor.map(single_nn_fitness,population),population):
            pop_fit_tuple.append((nn,fit))
    return pop_fit_tuple

def single_nn_fitness(nn):
    limit_cpu()
    return SnakeGame(nn).play_game()

def selection(pop_fit_tuple,old_best_score):
    pop_fit_tuple = sorted(pop_fit_tuple,key=lambda x: x[1],reverse=True)
    best_nn = None
    best_score = -100
    if(pop_fit_tuple[0][1] > old_best_score):
        best_score = pop_fit_tuple[0][1]
        best_nn = pop_fit_tuple[0][0]
    return [nn for nn,fit in pop_fit_tuple[:N_PARENTS]],best_score,best_nn

# parents is a list of of neural networks
def crossover(parents,best_nn):
    #elitism -> keep the best fit agent in the population
    if best_nn is not None:
        offsprings = [best_nn]
        offset = 1
    else:
        offsprings = []
        offset = 0

    for _ in range(POPULATION_SIZE - 1):
        # select two random parents
        p1_idx = random.randint(0,N_PARENTS - 1)
        p2_idx = random.randint(0,N_PARENTS - 1)

        p1 = parents[p1_idx].output_weights()
        p2 = parents[p2_idx].output_weights()

        # perform 2-point crossover
        fold_point_1 = random.randint(3,int(WEIGHTS_ROW_SIZE / 2))
        # fold_point_2 = random.randint(fold_point_1 + 3,WEIGHTS_ROW_SIZE)

        # offspring = np.vstack((p1[:fold_point_1],p2[fold_point_1:fold_point_2],p1[fold_point_2:]))
        offspring = np.vstack((p1[:fold_point_1],p2[fold_point_1:]))

        # mutate offspring and create the network again
        offsprings.append(NeuralNetwork(weights=mutation(offspring)[0]))

    return offsprings





def mutation(offspring):
    for i in range(WEIGHTS_ROW_SIZE):
        if random.random() < MUTATION_PROB:
            offspring[0,i] = random.uniform(-1.0,1.0)
    return offspring