from genetic_algorithm.neural_network import *

import numpy as np
print(WEIGHTS_COLUMN_SIZE)
test_array = np.array(list(range(0,WEIGHTS_COLUMN_SIZE)))


nn = NeuralNetwork(weights=test_array)

arr = nn.output_weights()

k = 0