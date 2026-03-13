#include "genome.hpp"

Genome::Genome(size_t newId)
{
    this->id = newId;
    fitness = 0.f;
    // creature stats
    n_mutateableParameters = 8;
    isHerbivore = true;
    isCarnivore = false;
    healthShare = 0.5f;
    attackShare = 0.5f;
    speedShare = 0.5f;
    size = INITIAL_SIZE;
    color = COLOR_HERBIVORE;
    // creature stats
    biasValue = 1.f;
    counterOscillator = 0;
    oscillatorFrequency = GenerateRandomFloatUniform(0.1f, 10.f);
    oscillatorValue = 0.f;
    randomNoiseSeed = GenerateRandomFloatUniform(-1000.f, 1000.f);
    counterRandomNoise = 0;
    randomNoiseFrequency = GenerateRandomFloatUniform(0.1f, 10.f);
    randomNoiseValue = 0.f;
}

Genome::Genome()
{
    id = 0;
    fitness = 0.f;
    // creature stats
    n_mutateableParameters = 8;
    isHerbivore = true;
    isCarnivore = false;
    healthShare = 0.5f;
    attackShare = 0.5f;
    speedShare = 0.5f;
    size = INITIAL_SIZE;
    color = { 0, 0, 0, 0 };
    // creature stats
    biasValue = 1.f;
    counterOscillator = 0;
    oscillatorFrequency = GenerateRandomFloatUniform(0.1f, 10.f);
    oscillatorValue = 0.f;
    randomNoiseSeed = GenerateRandomFloatUniform(-1000.f, 1000.f);
    counterRandomNoise = 0;
    randomNoiseFrequency = GenerateRandomFloatUniform(0.1f, 10.f);
    randomNoiseValue = 0.f;
}

Genome::~Genome()
{

}

void Genome::AddNodeGene(NodeGene nodeGene)
{
    // add node gene to nodes at index of gene id
    NodeGenes.insert({ nodeGene.GetId(), nodeGene });
}

void Genome::AddConnectionGene(ConnectionGene connectionGene)
{
    ConnectionGenes.insert({ connectionGene.GetInnovation(), connectionGene });
}

void Genome::SetConnectionWeight(size_t inNode, size_t outNode, float newWeight)
{
    for (auto& connectionGene : ConnectionGenes) {
        if (connectionGene.second.GetInNode() == inNode and connectionGene.second.GetOutNode() == outNode) {
            connectionGene.second.SetWeight(newWeight);
        }
    }
}

// mutate genome by adding a node in place of a connection
void Genome::MutateAddNode()
{
    // do nothing if number of node genes is already at maximum
    if (NodeGenes.size() > maxNodeGenes) {
        return;
    }
    // get suitable connection genes that are enabled and non-recurrent
    std::vector<ConnectionGene> suitableConnectionGenes;
    for (auto& connectionGene : ConnectionGenes) {
        if (connectionGene.second.IsEnabled() == true and connectionGene.second.IsRecurrent() == false) {
            suitableConnectionGenes.push_back(connectionGene.second);
        }
    }
    if (suitableConnectionGenes.empty()) {
        return; // unable to find suitable connection to add node to
    }
    // get random suitable connection in network
    int roll = GenerateRandomInt(0, static_cast<int>(suitableConnectionGenes.size()) - 1);
    // get the in and out nodes of chosen connection
    NodeGene inNodeGene = NodeGenes.at(suitableConnectionGenes[roll].GetInNode());
    NodeGene outNodeGene = NodeGenes.at(suitableConnectionGenes[roll].GetOutNode());
    // disable original connection
    ConnectionGenes.at(suitableConnectionGenes[roll].GetInnovation()).Disable();
    // create new node to fit on top of chosen connection
    size_t layerNumber = inNodeGene.GetLayerNumber() + 1;
    NodeGene newNodeGene = { NetworkNodeType::HIDDEN, NodeInnovationCounter.GetNewInnovation(), layerNumber };
    // create connections in to and out from new node gene
    ConnectionGene connectionGeneIntoNewNode = {
        inNodeGene.GetId(),
        newNodeGene.GetId(),
        1.f,
        ConnectionInnovationCounter.GetNewInnovation(),
        true,
        false,
    };
    ConnectionGene connectionGeneOutofNewNode = {
        newNodeGene.GetId(),
        outNodeGene.GetId(),
        suitableConnectionGenes[roll].GetWeight(),
        ConnectionInnovationCounter.GetNewInnovation(),
        true,
        false,
    };
    // add to node and connection genes
    AddNodeGene(newNodeGene);
    AddConnectionGene(connectionGeneIntoNewNode);
    AddConnectionGene(connectionGeneOutofNewNode);
    // refresh the genome layer numbers of all node genes starting from input layer
    UpdateLayerNumbers();
}

// mutate genome by adding a connection between two nodes
void Genome::MutateAddConnection()
{
    // get two random nodes in network representing the in and out nodes of the connection
    int roll_1 = GenerateRandomInt(1, static_cast<int>(NodeGenes.size()));
    NodeGene randomNodeGeneIn = NodeGenes.at(roll_1);
    int roll_2 = GenerateRandomInt(1, static_cast<int>(NodeGenes.size()));
    NodeGene randomNodeGeneOut = NodeGenes.at(roll_2);
    // return if connection is impossible
    if (randomNodeGeneIn.GetType() == NetworkNodeType::OUTPUT) {
        return;
    }
    if (randomNodeGeneIn.GetType() == NetworkNodeType::INPUT && randomNodeGeneOut.GetType() == NetworkNodeType::INPUT) {
        return;
    }
    // return if connection already exists
    bool connectionExists = false;
    for (auto& connectionGene : ConnectionGenes) {
        if (connectionGene.second.GetInNode() == randomNodeGeneIn.GetId() && connectionGene.second.GetOutNode() == randomNodeGeneOut.GetId()) { // existing connection
            connectionExists = true;
            break;
        }
    }
    if (connectionExists) {
        return;
    }
    // check if new connection is recurrent
    bool isRecurrent = false;
    if (randomNodeGeneIn.GetLayerNumber() > randomNodeGeneOut.GetLayerNumber()) {
        isRecurrent = true;
    }
    // if all tests are passed, create new connection gene
    ConnectionGene newConnectionGene = {
        randomNodeGeneIn.GetId(),
        randomNodeGeneOut.GetId(),
        GenerateRandomFloatUniform(minConnectionWeight, maxConnectionWeight),
        ConnectionInnovationCounter.GetNewInnovation(),
        true,
        isRecurrent,
    };
    // add to connection genes
    AddConnectionGene(newConnectionGene);
    // refresh the genome layer numbers of all node genes starting from input layer
    UpdateLayerNumbers();
}

// mutate genome by changing the weight of an enabled connection
void Genome::MutateConnectionWeight()
{
    // get enabled connection genes
    std::vector<ConnectionGene> enabledConnectionGenes;
    for (auto& connectionGene : ConnectionGenes) {
        if (connectionGene.second.IsEnabled()) {
            enabledConnectionGenes.push_back(connectionGene.second);
        }
    }
    if (enabledConnectionGenes.empty()) {
        return; // unable to find suitable connection to add node to
    }
    // get random enabled connection in network
    int roll_1 = GenerateRandomInt(0, static_cast<int>(enabledConnectionGenes.size()) - 1);
    // roll if weight should be perturbed or replaced
    float roll_2 = GenerateRandomFloatUniform(0.f, 1.f);
    if (roll_2 < perturbingProbability) {
        float newWeight = ConnectionGenes.at(enabledConnectionGenes[roll_1].GetInnovation()).GetWeight() + GenerateRandomFloatGaussian(0.f, perturbingSigma);
        newWeight = ClampFloat(newWeight, minConnectionWeight, maxConnectionWeight);
        //connection.second.SetWeight(connection.second.GetWeight() + GenerateRandomFloatUniform(-perturbingRadius, perturbingRadius)); // perturbe weight with uniform distribution
        ConnectionGenes.at(enabledConnectionGenes[roll_1].GetInnovation()).SetWeight(newWeight); // perturbe weight with normal distribution
    }
    else { // set new random weight with uniform distribution
        ConnectionGenes.at(enabledConnectionGenes[roll_1].GetInnovation()).SetWeight(GenerateRandomFloatUniform(minConnectionWeight, maxConnectionWeight));
    }
}

// mutate genome by enabling a connection
void Genome::MutateEnableConnection()
{
    // get disabled connection genes
    std::vector<ConnectionGene> disabledConnectionGenes;
    for (auto& connectionGene : ConnectionGenes) {
        if (connectionGene.second.IsEnabled() == false) {
            disabledConnectionGenes.push_back(connectionGene.second);
        }
    }
    if (disabledConnectionGenes.empty()) {
        return; // unable to find suitable connection to enable
    }
    // get random enabled connection in network
    int roll = GenerateRandomInt(0, static_cast<int>(disabledConnectionGenes.size()) - 1);
    // enable connection in connection genes
    ConnectionGenes.at(disabledConnectionGenes[roll].GetInnovation()).Enable();
    // refresh the genome layer numbers of all node genes starting from input layer
    UpdateLayerNumbers();
}

// mutate genome by disabling a connection
void Genome::MutateDisableConnection()
{
    // get enabled connection genes
    std::vector<ConnectionGene> enabledConnectionGenes;
    for (auto& connectionGene : ConnectionGenes) {
        if (connectionGene.second.IsEnabled()) {
            enabledConnectionGenes.push_back(connectionGene.second);
        }
    }
    if (enabledConnectionGenes.empty()) {
        return; // unable to find suitable connection to disable, lucky genome
    }
    // get random enabled connection in network
    int roll = GenerateRandomInt(0, static_cast<int>(enabledConnectionGenes.size()) - 1);
    // disable connection in connection genes
    ConnectionGenes.at(enabledConnectionGenes[roll].GetInnovation()).Disable();
    // refresh the genome layer numbers of all node genes starting from input layer
    UpdateLayerNumbers();
}

void Genome::UpdateLayerNumbers()
{
    // update the genome layer numbers of all node genes starting from input layer
    // always have to update for added node genes, connection genes, enabled and disabled connection genes
    size_t newLayerNumber;
    std::vector<ConnectionGene> nextConnectionGenes;
    std::vector<ConnectionGene> nextConnectionGenesBuffer;
    // initial next connections starting from input layer
    for (auto& connectionGene : ConnectionGenes) {
        if (connectionGene.second.IsEnabled() == true and connectionGene.second.IsRecurrent() == false) {
            if (NodeGenes.at(connectionGene.second.GetInNode()).GetType() == INPUT) {
                nextConnectionGenes.push_back(connectionGene.second);
            }
        }
    }
    // loop over next connection genes until output layer is reached
    while (nextConnectionGenes.size() > 0) {
        for (auto& nextConnectionGene : nextConnectionGenes) {
            if (nextConnectionGene.IsEnabled() == true and nextConnectionGene.IsRecurrent() == false) {
                newLayerNumber = NodeGenes.at(nextConnectionGene.GetInNode()).GetLayerNumber() + 1;
                if (NodeGenes.at(nextConnectionGene.GetOutNode()).GetLayerNumber() < newLayerNumber) { // making sure layer number is set to the highest one
                    NodeGenes.at(nextConnectionGene.GetOutNode()).SetLayerNumber(newLayerNumber);
                }
                // if connection goes out to output node, dont check for next connection genes
                if (NodeGenes.at(nextConnectionGene.GetOutNode()).GetType() == OUTPUT) {
                    continue;
                }
                // get connection genes going out from each next connection gene into buffer
                for (auto& outputConnectionGene : ConnectionGenes) {
                    if (outputConnectionGene.second.IsEnabled() == true and outputConnectionGene.second.IsRecurrent() == false) {
                        if (outputConnectionGene.second.GetInNode() == nextConnectionGene.GetOutNode()) {
                            nextConnectionGenesBuffer.push_back(outputConnectionGene.second);
                        }
                    }
                }
            }
        }
        // switch with buffer
        nextConnectionGenes.clear();
        nextConnectionGenes = nextConnectionGenesBuffer;
        nextConnectionGenesBuffer.clear();
    }
}

void Genome::MutateStats()
{
    int roll = GenerateRandomInt(1, n_mutateableParameters);
    if (roll == 1) { // switch food source
        if (isHerbivore) {
            isHerbivore = false;
            isCarnivore = true;
        }
        else if (isCarnivore) {
            isCarnivore = false;
            isHerbivore = true;
        }
    }
    else if (roll == 2) { // mutate healthShare
        healthShare += GenerateRandomFloatGaussian(0.f, perturbingSigma);
        healthShare = ClampFloat(healthShare, 0.1f, 1.f);

    }
    else if (roll == 3) { // mutate attackShare
        attackShare += GenerateRandomFloatGaussian(0.f, perturbingSigma);
        attackShare = ClampFloat(attackShare, 0.1f, 1.f);
    }
    else if (roll == 4) { // mutate speedShare
        speedShare += GenerateRandomFloatGaussian(0.f, perturbingSigma);
        speedShare = ClampFloat(speedShare, 0.1f, 1.f);
    }
    else if (roll == 5) { // mutate size
        size += size * GenerateRandomFloatGaussian(0.f, 0.1f);
        size = ClampFloat(size, 5.f, 30.f);
    }
    else if (roll == 6) { // mutate biasValue
        biasValue += GenerateRandomFloatGaussian(0.f, 0.1f);
        biasValue = ClampFloat(biasValue, -1.f, 1.f);
    }
    else if (roll == 7) { // mutate oscillatorFrequency
        oscillatorFrequency += oscillatorFrequency * GenerateRandomFloatGaussian(0.f, 0.5f);
        oscillatorFrequency = ClampFloat(oscillatorFrequency, 0.1f, 10.f);
    }
    else if (roll == 8) { // mutate randomNoiseFrequency
        randomNoiseFrequency += randomNoiseFrequency * GenerateRandomFloatGaussian(0.f, 0.5f);
        randomNoiseFrequency = ClampFloat(randomNoiseFrequency, 0.1f, 10.f);
    }
}

void Genome::SetFitnessAdjustment(float fitnessAdjustment)
{
    fitness += fitnessAdjustment;
}

void Genome::SetId(size_t newId)
{
    id = newId;
}

size_t Genome::GetId()
{
    return{ id };
}

std::map<size_t, NodeGene> Genome::GetNodeGenes()
{
    return{ NodeGenes };
}

std::map<size_t, ConnectionGene> Genome::GetConnectionGenes()
{
    return{ ConnectionGenes };
}

float Genome::GetFitness()
{
    return{ fitness };
}