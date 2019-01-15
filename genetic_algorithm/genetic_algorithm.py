import numpy as np
import random

from neural_network import WEIGHTS_ROW_SIZE, NeuralNetwork


POPULATION_SIZE = 50
N_PARENTS = 10
MUTATION_PROB = 0.1



def fitness(population):
    pass

def selection(population,fitness):
    pop_fit_tuple = [(nn,fit) for nn,fit in zip(population,fitness)]
    pop_fit_tuple = sorted(pop_fit_tuple,key=lambda x: x[1],reverse=True)
    return [nn for nn,fit in pop_fit_tuple[:N_PARENTS]]

# parents is a list of of neural networks
def crossover(parents):
    #elitism -> keep the best fit agent in the population
    offsprings = [parents[0]]

    for _ in range(POPULATION_SIZE - 1):
        # select two random parents
        p1_idx = random.randint(0,N_PARENTS - 1)
        p2_idx = random.randint(0,N_PARENTS - 1)

        p1 = parents[p1_idx].output_weights()
        p2 = parents[p2_idx].output_weights()

        # perform 2-point crossover
        fold_point_1 = random.randint(3,int(WEIGHTS_ROW_SIZE / 2))
        fold_point_2 = random.randint(fold_point_1 + 3,WEIGHTS_ROW_SIZE)

        offspring = np.vstack((p1[:fold_point_1],p2[fold_point_1:fold_point_2],p1[fold_point_2:]))

        # mutate offspring and create the network again
        offsprings.append(NeuralNetwork(weights=mutation(offspring)[0]))

    return offsprings





def mutation(offspring):
    for i in range(WEIGHTS_ROW_SIZE):
        if random.random() < MUTATION_PROB:
            offspring[0,i] = random.uniform(-1.0,1.0)
    return offspring