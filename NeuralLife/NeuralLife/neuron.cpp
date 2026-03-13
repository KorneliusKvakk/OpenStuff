#pragma once
#include "neuron.hpp"

Neuron::Neuron()
{
	type = HIDDEN;
	layerNumber = 0;
	inputSum = 0.f;
	output = 0.f;
}

Neuron::~Neuron()
{

}

// add input connection with input ID (ID of neuron the input came from), input value set to 0 and activated to false
void Neuron::AddInputConnection(size_t inputID)
{
	Inputs.insert({ inputID, 0.f }); // inputID is the ID of the neuron giving the input
}

void Neuron::AddOutputConnection(size_t outputID, float weight)
{
	OutputWeights.insert({ outputID, weight });
}

// feed input with input ID (ID of neuron the input came from), input value and sets neuron input to activated
void Neuron::FeedInput(size_t inputID, float inputValue)
{
	Inputs[inputID] = inputValue; // inputID is the ID of the neuron giving the input
}

// trying bounded ReLu to output max 1
float Neuron::ActivationFunctionBoundedReLu(float input)
{
	return{ std::min(std::max(0.f, input), 1.f) }; // Bounded ReLu
}

float Neuron::ActivationFunctionReLu(float input)
{
	return{ std::max(0.f, input) }; // ReLu
}

float Neuron::ActivationFunctionSigmoid(float input)
{
	return{ 1.f / (1.f + std::exp(-input)) }; // Sigmoid
	//return{ std::tanh(input) }; // tanh
}

void Neuron::CalculateOutput()
{
	inputSum = 0.f;
	for (auto& input : Inputs) {
		inputSum += input.second;
	}
	// only apply activation function if not input neuron
	if (type == NetworkNodeType(INPUT)) {
		output = inputSum;
	}
	else {
		output = ActivationFunctionBoundedReLu(inputSum);
	}
}

void Neuron::SetType(NetworkNodeType newType)
{
	type = newType;
}

void Neuron::SetLayerNumber(size_t newLayerNumber)
{
	layerNumber = newLayerNumber;
}

std::map<size_t, float> Neuron::GetInputs()
{
	return { Inputs };
}

std::map<size_t, float> Neuron::GetOutputWeights()
{
	return { OutputWeights };
}

NetworkNodeType Neuron::GetType()
{
	return{ type };
}

size_t Neuron::GetLayerNumber()
{
	return{ layerNumber };
}

float Neuron::GetOutputValue()
{
	return{ output };
}