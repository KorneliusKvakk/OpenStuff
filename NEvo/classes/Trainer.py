"""
Created on January 1 00:00 2025
@author: Johan Andreas Stendal
This class defines the neural evolution trainer
"""

import numpy as np
import pandas as pd
import time

from configNEvo import *

from EvolutionManager import EvolutionManager

class Trainer():
    def __init__(self,
        normalized_input_data,
        training_fraction = 0.75
        n_inputs = 10,
        hidden_layers = [10, 10, 10] : list,
        n_outputs = 1,
        n_epochs = 5000,
        epoch_step = 500,
        learning_rate = 1e-3,
        weight_NaMo = 1,
        weight_data = 0.1,
        batch_size = 8):

        # normalized input data
        self.normalized_input_data = normalized_input_data

        # neural network architecture
        self.n_inputs = n_inputs
        self.hidden_layers = hidden_layers
        self.n_outputs = n_outputs

        # training parameters
        self.n_epochs = n_epochs
        self.epoch_step = epoch_step
        self.learning_rate = learning_rate
        self.weight_NaMo = weight_NaMo
        self.weight_data = weight_data
        self.batch_size = batch_size
        
        # initialize the ANN model
        self.ann_model = ANN_model(
            n_inputs=n_inputs,
            hidden_layers=hidden_layers,
            n_outputs=n_outputs)
        self.model_name = 'model_1'

        # initialize loaded model
        self.ann_model_loaded = self.ann_model+

        # define the optimizer
        self.optimizer = optim.Adam(ann_model.parameters(), lr=learning_rate)

        # Split the input data into training and test sets
        training_data_size = int(training_fraction * len(self.normalized_input_data))
        test_data_size = len(self.normalized_input_data) - training_data_size
        self.normalized_training_data, self.normalized_test_data = random_split(self.normalized_input_data, [training_data_size, test_data_size])

        # Create DataLoaders for training and testing
        self.training_loader = DataLoader(self.normalized_training_data, batch_size=batch_size, shuffle=True)
        self.test_loader = DataLoader(self.normalized_test_data, batch_size=batch_size, shuffle=False)

        # Create DataLoader for PINN
        self.PINN_training_data = TensorDataset(training_inputs_PINN, training_targets_PINN)
        self.PINN_loader = DataLoader(self.PINN_training_data, batch_size=batch_size, shuffle=True)

        # training metrics
        self.losses_data = []
        self.losses_test = []
        self.combined_losses = []
        self.estimated_training_time = 0
        self.training_time = 0

        # initialize datasets
        self.normalized_training_data = np.array([], columns=training_data_columns)
        self.normalized_training_predictions_data = np.array([], columns=predictions_columns)
        self.normalized_training_predictions_NaMo = np.array([], columns=predictions_columns)
        self.normalized_training_predictions_test = np.array([], columns=predictions_columns)
        self.normalized_predictions = np.array([], columns=predictions_columns)

    def CalcualteScheilIntegralPINN(self, time, temperature):