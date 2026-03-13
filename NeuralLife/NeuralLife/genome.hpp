#pragma once
#include "config.hpp"

const struct InnovationCounter {
private:
	size_t innovations = 0;
public:
	size_t GetNewInnovation() {
		innovations++;
		return { innovations };
	}
};

const struct NodeGene {
private:
	NetworkNodeType type;
	size_t id;
	size_t layerNumber;
public:
	NodeGene(NetworkNodeType type, size_t id, size_t layerNumber) {
		this->type = type;
		this->id = id;
		this->layerNumber = layerNumber;
	}
	NetworkNodeType GetType() {
		return { type };
	};
	size_t GetId() {
		return { id };
	};
	void SetLayerNumber(size_t newLayerNumber) {
		layerNumber = newLayerNumber;
	};
	size_t GetLayerNumber() {
		return { layerNumber };
	};
	NodeGene Copy() {
		return { NodeGene(type, id, layerNumber) };
	};
};

const struct ConnectionGene {
private:
	size_t inNode;
	size_t outNode;
	float weight;
	size_t innovation;
	bool enabled;
	bool recurrent;
public:
	ConnectionGene(size_t inNode, size_t outNode, float weight, size_t innovation, bool enabled, bool recurrent) {
		this->inNode = inNode;
		this->outNode = outNode;
		this->weight = weight;
		this->innovation = innovation;
		this->enabled = enabled;
		this->recurrent = recurrent;
	}
	size_t GetInNode() {
		return { inNode };
	};
	size_t GetOutNode() {
		return { outNode };
	};
	void SetWeight(float weight_new) {
		this->weight = weight_new;
	};
	float GetWeight() {
		return { weight };
	};
	size_t GetInnovation() {
		return { innovation };
	};
	void Enable() {
		enabled = true;
	};
	void Disable() {
		enabled = false;
	};
	bool IsEnabled() {
		return { enabled };
	};
	bool IsRecurrent() {
		return { recurrent };
	};
	ConnectionGene Copy() {
		return{ ConnectionGene(inNode, outNode, weight, innovation, enabled, recurrent) };
	};
};

const class Genome {
private:
	size_t id;
	std::map<size_t, NodeGene> NodeGenes;
	std::map<size_t, ConnectionGene> ConnectionGenes;
	float fitness;
public:
	Genome(size_t newId);
	Genome();
	~Genome();
	void AddNodeGene(NodeGene nodeGene);
	void AddConnectionGene(ConnectionGene connectionGene);
	void MutateAddNode();
	void MutateAddConnection();
	void SetConnectionWeight(size_t inNode, size_t outNode, float newWeight);
	void MutateConnectionWeight();
	void MutateEnableConnection();
	void MutateDisableConnection();
	void UpdateLayerNumbers();
	void MutateStats();
	void SetFitnessAdjustment(float fitnessAdjustment);
	void SetId(size_t newId);
	size_t GetId();
	std::map<size_t, NodeGene> GetNodeGenes();
	std::map<size_t, ConnectionGene> GetConnectionGenes();
	float GetFitness();
	InnovationCounter NodeInnovationCounter;
	InnovationCounter ConnectionInnovationCounter;
	// creature stats
	int n_mutateableParameters;
	bool isHerbivore;
	bool isCarnivore;
	float healthShare;
	float attackShare;
	float speedShare;
	float size = INITIAL_SIZE;
	Color color;
	// creature stats
	float biasValue;
	int counterOscillator;
	float oscillatorFrequency;
	float oscillatorValue;
	float randomNoiseSeed;
	int counterRandomNoise;
	float randomNoiseFrequency;
	float randomNoiseValue;
};