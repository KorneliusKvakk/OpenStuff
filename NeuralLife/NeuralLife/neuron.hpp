#pragma once
#include "config.hpp"

const class Neuron {
private:
	std::map<size_t, float> Inputs; // inputs in neuron mapped by ID
	std::map<size_t, float> OutputWeights; // output weights mapped by ID
	NetworkNodeType type;
	size_t layerNumber; // layer number in neural network
	float inputSum;
	float output;
public:
	Neuron();
	~Neuron();
	void AddInputConnection(size_t inputID);
	void AddOutputConnection(size_t outputID, float weight);
	void FeedInput(size_t inputID, float inputValue);
	float ActivationFunctionBoundedReLu(float input);
	float ActivationFunctionReLu(float input);
	float ActivationFunctionSigmoid(float input);
	void CalculateOutput();
	void SetType(NetworkNodeType newType);
	void SetLayerNumber(size_t newLayerNumber);
	std::map<size_t, float> GetInputs();
	std::map<size_t, float > GetOutputWeights();
	NetworkNodeType GetType();
	size_t GetLayerNumber();
	float GetOutputValue();
};