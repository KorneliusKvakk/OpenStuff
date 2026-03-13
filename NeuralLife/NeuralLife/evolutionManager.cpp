#include "evolutionManager.hpp"

EvolutionManager::EvolutionManager()
{
    genesisGenome = Genome(0);
    GenerateGenesisGenome();
    Genomes.push_back(genesisGenome);
    Breeds.push_back(Breed(genesisGenome));
}

EvolutionManager::~EvolutionManager()
{

}

void EvolutionManager::GenerateGenesisGenome()
{
    // add all input node genes
    for (size_t i = 0; i < n_Senses; i++) {
        genesisGenome.AddNodeGene(NodeGene(NetworkNodeType::INPUT, genesisGenome.NodeInnovationCounter.GetNewInnovation(), 1));
    }
    // add all output node genes
    for (size_t i = 0; i < n_Actions; i++) {
        genesisGenome.AddNodeGene(NodeGene(NetworkNodeType::OUTPUT, genesisGenome.NodeInnovationCounter.GetNewInnovation(), 2));
    }
    // add connections
    for (size_t i = 1; i < n_Senses + 1; i++) {
        for (size_t k = n_Senses + 1; k < n_Senses + n_Actions + 1; k++) {
            genesisGenome.AddConnectionGene(ConnectionGene(
                genesisGenome.GetNodeGenes().at(i).GetId(),
                genesisGenome.GetNodeGenes().at(k).GetId(),
                0.f,
                genesisGenome.ConnectionInnovationCounter.GetNewInnovation(),
                true,
                false));
        }
    }
    genesisGenome.SetConnectionWeight(6, 12, 1.f); // TAGET_DISTANCE_Y->MOVE_NORTH
    genesisGenome.SetConnectionWeight(6, 13, -1.f); // TAGET_DISTANCE_Y->MOVE_SOUTH
    genesisGenome.SetConnectionWeight(5, 14, -1.f); // TAGET_DISTANCE_X->MOVE_EAST
    genesisGenome.SetConnectionWeight(5, 15, 1.f); // TAGET_DISTANCE_X->MOVE_WEST
    genesisGenome.SetConnectionWeight(1, 16, 1.f); // BIAS->ACTIVITY
}

Creature EvolutionManager::GenerateGenesisCreature()
{
    NeuralNetwork genesisNet = NeuralNetwork();
    genesisNet.GenerateFromGenome(genesisGenome);
    Vector2 position = { GenerateRandomFloatUniform(0.f, static_cast<float>(SCREEN_WIDTH)), GenerateRandomFloatUniform(0.f, static_cast<float>(SCREEN_HEIGHT)) };
    Creature genesisCreature = Creature(genesisGenome, genesisNet, position);

    return { genesisCreature };
}

Genome EvolutionManager::MutateGenome(Genome genome)
{
    Genome mutatedGenome = genome;
    int rollMutationType = 0;
    float rollMutate = GenerateRandomFloatUniform(0.f, 1.f);
    if (rollMutate <= mutationProbability) {
        rollMutationType = GenerateRandomInt(1, 6);
    }
    if (rollMutationType == 1) {
        mutatedGenome.MutateAddNode();
    }
    else if (rollMutationType == 2) {
        mutatedGenome.MutateAddConnection();
    }
    else if (rollMutationType == 3) {
        mutatedGenome.MutateConnectionWeight();
    }
    else if (rollMutationType == 4) {
        mutatedGenome.MutateEnableConnection();
    }
    else if (rollMutationType == 5) {
        mutatedGenome.MutateDisableConnection();
    }
    else if (rollMutationType == 6) {
        mutatedGenome.MutateStats();
    }

    return { mutatedGenome };
}

Genome EvolutionManager::Crossover(Genome parent1, Genome parent2)
{
    // crossover function to breed two parents, parent1 should always be the more fit parent
    Genome childGenome;
    // add all node genes from most fit parent
    for (auto& parent1NodeGene : parent1.GetNodeGenes()) {
        childGenome.AddNodeGene(parent1NodeGene.second.Copy());
    }
    // TODO go throught and check if innovation number is needed, maybe just map key is needed?
    // check if parents have matching connection genes in terms of innovation number
    for (auto& parent1ConnectionGene : parent1.GetConnectionGenes()) {
        for (auto& parent2ConnectionGene : parent2.GetConnectionGenes()) {
            if (parent1ConnectionGene.second.GetInnovation() == parent2ConnectionGene.second.GetInnovation()) { // matching connection gene by key/innovation
                // copy parent1 gene
                ConnectionGene childConnectionGene = parent1ConnectionGene.second.Copy();
                // random choice between parents for matching genes
                int roll_1 = GenerateRandomInt(0, 1);
                if (roll_1 == 0) {
                    childConnectionGene = parent2ConnectionGene.second.Copy(); // switch to copy from parent2
                }
                // chance that gene will be disabled if disabled in either parent
                if (parent1ConnectionGene.second.IsEnabled() == false or parent2ConnectionGene.second.IsEnabled() == false) {
                    float roll_2 = GenerateRandomFloatUniform(0.f, 1.f);
                    if (roll_2 < inheritDisabledGeneProbability) {
                        childConnectionGene.Disable();
                    }
                }
                childGenome.AddConnectionGene(childConnectionGene);
            }
            else { // disjoint or excess gene is always added from more fit parent1
                ConnectionGene childConnectionGene = parent1ConnectionGene.second.Copy();
                // chance that gene will be disabled if disabled in parent1 genome
                if (parent1ConnectionGene.second.IsEnabled() == false) {
                    float roll_3 = GenerateRandomFloatUniform(0.f, 1.f);
                    if (roll_3 < inheritDisabledGeneProbability) {
                        childConnectionGene.Disable();
                    }
                }
                childGenome.AddConnectionGene(childConnectionGene);
            }
        }
    }

    return { childGenome };
}

float EvolutionManager::GetGenomeCompatibilityDistance(Genome genome1, Genome genome2)
{
    // assuming maps are already sorted, TODO: check if they are actually sorted
    // TODO: is the -1 needed?
    // find highest innovation number of each genome
    size_t highestInnovation1 = std::max(genome1.GetNodeGenes().size(), genome1.GetConnectionGenes().size());
    size_t highestInnovation2 = std::max(genome2.GetNodeGenes().size(), genome2.GetConnectionGenes().size());
    // count number of matching node genes
    size_t n_matchingGenes = 0;
    for (auto& nodeGeneGenome1 : genome1.GetNodeGenes()) {
        for (auto& nodeGeneGenome2 : genome2.GetNodeGenes()) {
            if (nodeGeneGenome1.second.GetId() == nodeGeneGenome2.second.GetId()) {
                n_matchingGenes++;
            }
        }
    }
    // count number of matching connection genes and get total weight difference between matching connection genes
    float weightDifference = 0.f;
    for (auto& connectionGeneGenome1 : genome1.GetConnectionGenes()) {
        for (auto& connectionGeneGenome2 : genome2.GetConnectionGenes()) {
            if (connectionGeneGenome1.second.GetInnovation() == connectionGeneGenome2.second.GetInnovation()) {
                n_matchingGenes++;
                weightDifference += std::abs(connectionGeneGenome1.second.GetWeight() - connectionGeneGenome2.second.GetWeight());
            }
        }
    }
    // calculate average weight difference of matching connection genes between the two genomes
    float avgWeightDifference = weightDifference / static_cast<float>(n_matchingGenes);
    // count number of disjoint and excess genes (nonmatching genes)
    size_t n_totalNonMatchingGenes = (highestInnovation1 - n_matchingGenes) + (highestInnovation2 - n_matchingGenes);
    // number of total genes in the larger genome
    size_t n_totalGenesLargerGenome = std::max(highestInnovation1, highestInnovation2);
    // calculate compatibility distance between the two genomes
    float compatibilityDistance = static_cast<float>(c1) * static_cast<float>(n_totalNonMatchingGenes) / static_cast<float>(n_totalGenesLargerGenome) + static_cast<float>(c2) * avgWeightDifference;
    
    return { compatibilityDistance };
}