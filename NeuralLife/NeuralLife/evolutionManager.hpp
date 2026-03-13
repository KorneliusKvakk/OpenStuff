#pragma once
#include "creature.hpp"

struct Breed {
    std::vector<Genome> Members;
    Genome mascot; // mascot member representing genome
    Genome champion; // fittest member
    float sharedFitness = 0.f;
    Breed(Genome genome) {
        this->Members.push_back(genome);
        this->mascot = genome;
        this->champion = genome;
    }
    void AddMember(Genome genome) {
        Members.push_back(genome);
    }
    void UpdateChampion(Genome newChampion) {
        champion = newChampion;
    }
    void SetSharedFitnessAdjustment(float sharedFitnessAdjustment) {
        sharedFitness += sharedFitnessAdjustment;
    }
};

class EvolutionManager {
    private:
        std::vector<Genome> Genomes;
        std::vector<Breed> Breeds;
        Genome genesisGenome;
    public:
        EvolutionManager();
        ~EvolutionManager();
        InnovationCounter GenomeInnovationCounter;
        void GenerateGenesisGenome();
        Creature GenerateGenesisCreature();
        Genome MutateGenome(Genome genome);
        Genome Crossover(Genome parent1, Genome parent2);
        float GetGenomeCompatibilityDistance(Genome genome1, Genome genome2);
};