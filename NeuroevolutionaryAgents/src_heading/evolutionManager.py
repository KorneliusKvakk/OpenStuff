from configNeuroevolutionaryAgents import *

from genome import *
from breed import *
from agent import *

class EvolutionManager:
    def __init__(self):
        self.Genomes = []
        self.Breeds = []
        self.genomeInnovationCounter = InnovationCounter()
        self.genesisGenome = Genome(0)
        
    def GenerateGenesisGenome(self):
        for i in range(n_Senses):
            self.genesisGenome.AddNodeGene(NodeGene(NetworkNodeType.INPUT, self.genesisGenome.nodeInnovationCounter.GetNewInnovation(), 1))
        for i in range(n_Actions):
            self.genesisGenome.AddNodeGene(NodeGene(NetworkNodeType.OUTPUT, self.genesisGenome.nodeInnovationCounter.GetNewInnovation(), 2))
        for i in range(n_Senses):
            for k in range(n_Senses, n_Senses + n_Actions):
                self.genesisGenome.AddConnectionGene(ConnectionGene(
                    self.genesisGenome.GetNodeGenes()[i].GetNodeId(),
                    self.genesisGenome.GetNodeGenes()[k].GetNodeId(),
                    0.0,
                    self.genesisGenome.connectionInnovationCounter.GetNewInnovation(),
                    True,
                    False
                ))
        self.genesisGenome.SetConnectionWeight(10, 19, 1.0) # TAGET_DISTANCE_Y -> MOVE_NORTH
        self.genesisGenome.SetConnectionWeight(10, 20, -1.0) # TAGET_DISTANCE_Y -> MOVE_SOUTH
        self.genesisGenome.SetConnectionWeight(9, 21, -1.0) # TAGET_DISTANCE_X -> MOVE_EAST
        self.genesisGenome.SetConnectionWeight(9, 22, 1.0) # TAGET_DISTANCE_X -> MOVE_WEST
        self.Genomes.append(self.genesisGenome)
        self.Breeds.append(Breed(self.genesisGenome))

    def GenerateGenesisAgent(self, initialPosition : pygame.Vector2):
        genesisNet = NeuralNetwork()
        genesisNet.GenerateFromGenome(self.genesisGenome)
        return Agent(self.genesisGenome, genesisNet, initialPosition)

    def Genesis(self):
        pass

    def MutateGenome(self, genome : Genome):
        rollMutate = random.uniform(0.0, 1.0),
        if rollMutate <= mutationProbability:
            rollMutationType = random.randint(1, 6)
            if rollMutationType == 1:
                genome.MutateAddNode()
            if rollMutationType == 2:
                genome.MutateAddConnection()
            if rollMutationType == 3:
                genome.MutateConnectionWeight()
            if rollMutationType == 4:
                genome.MutateEnableConnection()
            if rollMutationType == 5:
                genome.MutateDisableConnection()
            if rollMutationType == 6:
                genome.MutateStats()
        return genome

    def GenerateAgent(self, initialPosition : pygame.Vector2):
        return Agent(genome, net, initialPosition)

    def Crossover(self, parent1 : Genome , parent2 : Genome):
        # most fit parent must be parent1
        childGenome = Genome(0)
        # add all node genes from most fit parent
        for parent1NodeGene in parent1.GetNodeGenes():
            childGenome.AddNodeGene(parent1NodeGene.Copy())
        # check if parents have matching connection genes in terms of innovation number
        for parent1ConnectionGene in parent1.GetConnectionGenes():
            for parent2ConnectionGene in parent2.GetConnectionGenes():
                if parent1ConnectionGene.second.GetInnovation() == parent2ConnectionGene.second.GetInnovation(): # matching connection gene by key/innovation
                    # copy parent1 gene
                    childConnectionGene = parent1ConnectionGene.Copy()
                    # random choice between parents for matching genes
                    roll_1 = random.random.randint(0, 1)
                    if roll_1 == 0:
                        childConnectionGene = parent2ConnectionGene.Copy() # switch to copy from parent2
                    # chance that gene will be disabled if disabled in either parent
                    if parent1ConnectionGene.IsEnabled() == False or parent2ConnectionGene.IsEnabled() == False:
                        roll_2 = random.uniform(0.0, 1.0)
                        if roll_2 < inheritDisabledGeneProbability:
                            childConnectionGene.Disable()
                    childGenome.AddConnectionGene(childConnectionGene)
                else: # disjoint or excess gene is always added from more fit parent1
                    childConnectionGene = parent1ConnectionGene.Copy()
                    # chance that gene will be disabled if disabled in parent1 genome
                    if parent1ConnectionGene.IsEnabled() == False:
                        roll_3 = random.uniform(0.0, 1.0)
                        if roll_3 < inheritDisabledGeneProbability:
                            childConnectionGene.Disable()
                    childGenome.AddConnectionGene(childConnectionGene)
        return childGenome
        
    def GetGenomeCompatibilityDistance(self, genome1 : Genome , genome2 : Genome):
        # find highest innovation number of each genome
        highestInnovation1 = max(len(genome1.GetNodeGenes()), len(genome1.GetConnectionGenes()))
        highestInnovation2 = max(len(genome2.GetNodeGenes()), len(genome2.GetConnectionGenes()))
        # count number of matching node genes
        n_matchingGenes = 0
        for nodeGeneGenome1 in genome1.GetNodeGenes():
            for nodeGeneGenome2 in genome2.GetNodeGenes():
                if nodeGeneGenome1.GetNodeId() == nodeGeneGenome2.GetNodeId():
                    n_matchingGenes += 1
        # count number of matching connection genes and get total weight difference between matching connection genes
        weightDifference = 0.0
        for connectionGeneGenome1 in genome1.GetConnectionGenes():
            for connectionGeneGenome2 in genome2.GetConnectionGenes():
                if connectionGeneGenome1.GetInnovation() == connectionGeneGenome2.GetInnovation():
                    n_matchingGenes += 1
                    weightDifference += abs(connectionGeneGenome1.GetWeight() - connectionGeneGenome2.GetWeight())
        # calculate average weight difference of matching connection genes between the two genomes
        avgWeightDifference = weightDifference / float(n_matchingGenes)
        # count number of disjoint and excess genes (nonmatching genes)
        n_totalNonMatchingGenes = (highestInnovation1 - n_matchingGenes) + (highestInnovation2 - n_matchingGenes)
        # number of total genes in the larger genome
        n_totalGenesLargerGenome = max(highestInnovation1, highestInnovation2)
        # calculate compatibility distance between the two genomes
        compatibilityDistance = c1 * float(n_totalNonMatchingGenes) / float(n_totalGenesLargerGenome) + c2 * avgWeightDifference
        return compatibilityDistance