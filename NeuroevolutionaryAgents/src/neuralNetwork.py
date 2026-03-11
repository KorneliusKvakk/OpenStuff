from configNeuroevolutionaryAgents import *

from genome import *
from neuron import *

class NeuralNetwork:
    def __init__(self):
        self.LayerNumbersToNodeIDs = []
        self.Neurons = {}
        self.InputIDs = []
        self.OutputIDs = []
        self.Actions = {}
        
    def GenerateFromGenome(self, genome : Genome):
        # add node genes to neurons
        for nodeGeneId, nodeGene in genome.GetNodeGenes().items():
            neuron = Neuron()
            neuron.SetNetworkNodeType(NetworkNodeType.HIDDEN)
            if nodeGene.GetNetworkNodeType() == NetworkNodeType.INPUT:
                self.InputIDs.append(nodeGene.GetNodeId())
                neuron.AddInputConnection(0) # id 0 because the input comes from "before" the input layer
                neuron.SetNetworkNodeType(NetworkNodeType.INPUT)
            elif nodeGene.GetNetworkNodeType() == NetworkNodeType.OUTPUT:
                self.OutputIDs.append(nodeGene.GetNodeId())
                neuron.SetNetworkNodeType(NetworkNodeType.OUTPUT)
            neuron.SetLayerNumber(nodeGene.GetLayerNumber())
            self.LayerNumbersToNodeIDs.append((nodeGene.GetLayerNumber(), nodeGene.GetNodeId()))
            self.Neurons[nodeGene.GetNodeId()] = neuron
        # sort neuron layer numbers to IDs mapping so that network layers are calculated sequentially
        self.LayerNumbersToNodeIDs = sorted(self.LayerNumbersToNodeIDs, key=lambda tup: tup[0])
        # add connection genes to neurons
        for connectionGeneId, connectionGene in genome.GetConnectionGenes().items():
            if connectionGene.IsEnabled() == False:
                continue
            # for neuron that leads in to connection, add output connection; out node ID and weight
            self.Neurons[connectionGene.GetInNode()].AddOutputConnection(connectionGene.GetOutNode(), connectionGene.GetWeight())
            # for neuron that recieves from connection, add input connection; in node ID
            self.Neurons[connectionGene.GetOutNode()].AddInputConnection(connectionGene.GetInNode())
            
    def Calculate(self, Senses : dict):
        # feed input neurons with initial input values from the senses
        for senseKey, senseValue in Senses.items():
            self.Neurons[senseKey].FeedInput(0, senseValue) # feed input neurons from Senses, ID 0 because the input comes from "before" the input layer
        # loop through the rest of the network in order of the order number of the neurons
        for layerNumber, nodeId in self.LayerNumbersToNodeIDs:
            # calculate output
            self.Neurons[nodeId].CalculateOutput()
            if len(self.Neurons[nodeId].GetOutputWeights()) > 0: # if neuron has outputs
                # feed the next neurons
                for outputID, outputWeight in self.Neurons[nodeId].GetOutputWeights().items():
                    self.Neurons[outputID].FeedInput(nodeId, outputWeight * self.Neurons[nodeId].GetOutputValue())
        # get the output from output neurons into network output (Actions)
        for outputID in self.OutputIDs:
            self.Actions[outputID] = self.Neurons[outputID].GetOutputValue()
        # return network output (Actions)
        return self.Actions