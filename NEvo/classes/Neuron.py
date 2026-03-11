"""
Created on January 1 00:00 2025
@author: Johan Andreas Stendal
This class defines the neural evolution neuron
"""

from configNEvo import *

class Neuron:
    def __init__(self):
        self.Inputs = {}
        self.OutputWeights = {}
        self.networkNodeType = NetworkNodeType.HIDDEN
        self.layerNumber = 0
        self.output = 0.0

    def AddInputConnection(self, inputID : int):
        self.Inputs[inputID] = 0.0

    def AddOutputConnection(self, outputID : int, weight : float):
        self.OutputWeights[outputID] = weight

    def FeedInput(self, inputID : int, inputValue : float):
        self.Inputs[inputID] = inputValue

    def ActivationFunctionBoundedReLu(self, inputValue : float):
        return min(max(0.0, inputValue), 1.0)

    def ActivationFunctionReLu(self, inputValue : float):
        return max(0.0, inputValue)

    def ActivationFunctionSigmoid(self, inputValue : float):
        return 1.0 / (1.0 + math.exp(-inputValue))

    def CalculateOutput(self):
        inputSum = 0.0
        for inputValue in self.Inputs.values():
            inputSum += inputValue
        # only apply activation function if not input neuron
        if self.networkNodeType == NetworkNodeType.INPUT:
            self.output = inputSum
        else:
            self.output = self.ActivationFunctionBoundedReLu(inputSum)

    def SetNetworkNodeType(self, newNetworkNodeType : NetworkNodeType):
        self.networkNodeType = newNetworkNodeType

    def SetLayerNumber(self, newLayerNumber : int):
        self.layerNumber = newLayerNumber

    def GetInputs(self):
        return self.Inputs

    def GetOutputWeights(self):
        return self.OutputWeights

    def GetNetworkNodeType(self):
        return self.networkNodeType

    def GetLayerNumber(self):
        return self.layerNumber
        
    def GetOutputValue(self):
        return self.output