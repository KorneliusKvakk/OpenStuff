#include "neuralNetwork.hpp"

NeuralNetwork::NeuralNetwork()
{
	// init actions map
	for (size_t i = n_Senses + 1; i <= n_Senses + n_Actions; i++) {
		Actions.insert({ i, 0.f });
	}
}

NeuralNetwork::~NeuralNetwork()
{

}

void NeuralNetwork::GenerateFromGenome(Genome genome)
{
	// add node genes to neurons
	for (auto& nodeGene : genome.GetNodeGenes()) {
		Neuron neuron;
		neuron.SetType(HIDDEN);
		if (nodeGene.second.GetType() == NetworkNodeType::INPUT) {
			InputIDs.push_back(nodeGene.second.GetId());
			neuron.AddInputConnection(0); // id 0 because the input comes from "before" the input layer
			neuron.SetType(INPUT);
		}
		else if (nodeGene.second.GetType() == NetworkNodeType::OUTPUT) {
			OutputIDs.push_back(nodeGene.second.GetId());
			neuron.SetType(OUTPUT);
		}
		neuron.SetLayerNumber(nodeGene.second.GetLayerNumber());
		LayerNumbersToIDs.push_back({ nodeGene.second.GetLayerNumber(), nodeGene.second.GetId() });
		Neurons.insert({ nodeGene.second.GetId(), neuron });
	}
	// sort neuron layer numbers to IDs mapping so that network layers are calculated sequentially
	std::sort(LayerNumbersToIDs.begin(), LayerNumbersToIDs.end());
	// add connection genes to neurons
	for (auto& connectionGene : genome.GetConnectionGenes()) {
		if (connectionGene.second.IsEnabled() == false) {
			continue;
		}
		// for neuron that leads in to connection, add output connection; out node ID and weight
		Neurons.at(connectionGene.second.GetInNode()).AddOutputConnection(connectionGene.second.GetOutNode(), connectionGene.second.GetWeight());
		// for neuron that recieves from connection, add input connection; in node ID
		Neurons.at(connectionGene.second.GetOutNode()).AddInputConnection(connectionGene.second.GetInNode());
	}
}

std::map<size_t, float> NeuralNetwork::Calculate(std::map<size_t, float> Senses)
{
	// feed input neurons with initial input values from the senses
	for (auto& sense : Senses) {
		Neurons.at(sense.first).FeedInput(0, sense.second); // feed input neurons from Senses, ID 0 because the input comes from "before" the input layer
	}
	// loop through the rest of the network in order of the order number of the neurons
	for (auto& layerNumberToID : LayerNumbersToIDs) {
		// calculate output
		Neurons.at(layerNumberToID.second).CalculateOutput();
		if (Neurons.at(layerNumberToID.second).GetOutputWeights().size() > 0) { // if neuron has outputs
			// feed the next neurons
			for (auto& output : Neurons.at(layerNumberToID.second).GetOutputWeights()) {
				Neurons.at(output.first).FeedInput(layerNumberToID.second, output.second * Neurons.at(layerNumberToID.second).GetOutputValue());
			}
		}
	}
	// get the output from output neurons into network output (Actions)
	for (size_t i = n_Senses + 1; i <= n_Senses + n_Actions; i++) {
		Actions[i] = Neurons.at(i).GetOutputValue();
	}
	// return network output (Actions)
	return { Actions };
}