#pragma once
#include "genome.hpp"
#include "neuron.hpp"
#include "config.hpp"

const class NeuralNetwork {
private:
	//size_t n_layers;
	std::vector<std::pair<size_t, size_t>> LayerNumbersToIDs; // neuron layer number (first) mapped to neuron ID (second)
	std::map<size_t, Neuron> Neurons; // neurons in genome mapped by ID
	std::vector<size_t> InputIDs;
	std::vector<size_t> OutputIDs;
	std::map<size_t, float> Actions;
public:
	NeuralNetwork();
	~NeuralNetwork();
	void GenerateFromGenome(Genome genome);
	std::map<size_t, float> Calculate(std::map<size_t, float> Senses);
};