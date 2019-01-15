import numpy as np

N_INPUT_NEURONS = 7
N_LAYER_1_NEURONS = 9
N_LAYER_2_NEURONS = 15
N_OUTPUT_NEURONS = 3 # forward, left or right

WEIGHTS_ROW_SIZE = N_INPUT_NEURONS * N_LAYER_1_NEURONS + \
                   N_LAYER_1_NEURONS * N_LAYER_2_NEURONS + \
                   N_LAYER_2_NEURONS * N_OUTPUT_NEURONS

# define the shapes of matrices that will store the weights connecting together layers
w_input_lay_1_shape = (N_LAYER_1_NEURONS, N_INPUT_NEURONS)
w_lay_1_lay_2_shape = (N_LAYER_2_NEURONS, N_LAYER_1_NEURONS)
w_lay_2_output_shape = (N_OUTPUT_NEURONS, N_LAYER_2_NEURONS)

class NeuralNetwork:

    def __init__(self,weights=None):

        if weights is None:
            self.init_neural_network()
        else:
            self.input_weights(weights)

    # at the beggining randomly initialize the neural network
    def init_neural_network(self):
        # initialize the weights
        self.w_input_lay1 = self.init_random_weights(w_input_lay_1_shape)
        self.w_lay1_lay2 = self.init_random_weights(w_lay_1_lay_2_shape)
        self.w_lay2_output = self.init_random_weights(w_lay_2_output_shape)

    def init_random_weights(self,shape):
        return np.random.choice(np.arange(-1, 1, step=0.01), size=shape, replace=True)

    # weights are stacked in columns for crossover and mutation, we need to stack them back into the shape of matrices of weights between the layers
    def input_weights(self,weights):
        self.w_input_lay1 = np.reshape(weights[ : N_INPUT_NEURONS * N_LAYER_1_NEURONS],newshape=w_input_lay_1_shape)
        self.w_lay1_lay2 = np.reshape(weights[N_INPUT_NEURONS * N_LAYER_1_NEURONS : N_INPUT_NEURONS * N_LAYER_1_NEURONS + N_LAYER_1_NEURONS * N_LAYER_2_NEURONS],newshape=w_lay_1_lay_2_shape)
        self.w_lay2_output = np.reshape(weights[N_INPUT_NEURONS * N_LAYER_1_NEURONS + N_LAYER_1_NEURONS * N_LAYER_2_NEURONS : ],newshape=w_lay_2_output_shape)

    def output_weights(self):
        return np.vstack((np.reshape(self.w_input_lay1,newshape=(N_INPUT_NEURONS * N_LAYER_1_NEURONS, 1)),
                        np.reshape(self.w_lay1_lay2, newshape=(N_LAYER_1_NEURONS * N_LAYER_2_NEURONS, 1)),
                        np.reshape(self.w_lay2_output, newshape=(N_LAYER_2_NEURONS * N_OUTPUT_NEURONS, 1)))).T

    # get the predicted outputs for the given input
    def forward_propagation(self,input):
        Z1 = np.matmul(self.w_input_lay1, input.T)
        A1 = np.tanh(Z1)
        Z2 = np.matmul(self.w_lay1_lay2, A1)
        A2 = np.tanh(Z2)
        Z3 = np.matmul(self.w_lay2_output, A2)
        A3 = self.softmax(Z3)
        return A3

    # outputs the direction the snake should take, -1 is left, 0 is go forward, 1 is right
    def predict_snake_direction(self,input):
        out = self.forward_propagation(input)
        return np.argmax(out) - 1


    def softmax(self,z):
        s = np.exp(z.T) / np.sum(np.exp(z.T), axis=1).reshape(-1, 1)
        return s





