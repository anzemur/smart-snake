import random

from genetic_algorithm import N_PARENTS, crossover, selection, POPULATION_SIZE
from neural_network import NeuralNetwork,WEIGHTS_ROW_SIZE

import numpy as np
print(WEIGHTS_ROW_SIZE)
nns = [NeuralNetwork() for i in range(POPULATION_SIZE)]


# nn = NeuralNetwork(weights=test_array)

# arr = nn.output_weights()

# offsprings = crossover(nns)
# for k in range(50):
#     print(offsprings[k].predict_snake_direction(np.array([random.uniform(0,1) for i in range(7)]).reshape(-1, 7)))

e = selection(nns,list(range(POPULATION_SIZE)))



k = 0