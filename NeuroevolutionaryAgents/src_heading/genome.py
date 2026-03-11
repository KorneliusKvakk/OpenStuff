from configNeuroevolutionaryAgents import *

class InnovationCounter:
    def __init__(self):
        self.n_innovations = 0

    def GetNewInnovation(self):
        self.n_innovations += 1
        return self.n_innovations

class NodeGene:
    def __init__(self, networkNodeType : NetworkNodeType, nodeId : int, layerNumber : int):
        self.networkNodeType = networkNodeType
        self.nodeId = nodeId
        self.layerNumber = layerNumber

    def SetLayerNumber(self, newLayerNumber : int):
        self.layerNumber = newLayerNumber

    def Copy(self):
        return NodeGene(self.type, self.nodeId, self.layerNumber)

    def GetNetworkNodeType(self):
        return self.networkNodeType

    def GetNodeId(self):
        return self.nodeId

    def GetLayerNumber(self):
        return self.layerNumber

class ConnectionGene:
    def __init__(self, inNode : int, outNode : int, weight : float, innovation : int, enabled : bool, recurrent : bool):
        self.inNode = inNode
        self.outNode = outNode
        self.weight = weight
        self.innovation = innovation
        self.enabled = enabled
        self.recurrent = recurrent

    def SetWeight(self, newWeight : float):
        self.weight = newWeight

    def Enable(self):
        self.enabled = True

    def Disable(self):
        self.enabled = False

    def Copy(self):
        return ConnectionGene(self.inNode, self.outNode, self.weight, self.innovation, self.enabled, self.recurrent)

    def GetInNode(self):
        return self.inNode

    def GetOutNode(self):
        return self.outNode

    def GetWeight(self):
        return self.weight

    def GetInnovation(self):
        return self.innovation

    def IsEnabled(self):
        return self.enabled

    def IsRecurrent(self):
        return self.recurrent

class Genome:
    def __init__(self, genomeId : int):
        self.genomeId = genomeId
        self.NodeGenes = []
        self.ConnectionGenes = []
        self.nodeInnovationCounter = InnovationCounter()
        self.connectionInnovationCounter = InnovationCounter()
        self.fitness = 0
        # stats
        self.n_mutateableParameters = 8
        # senses
        self.biasValue = 1.0
        self.counterOscillator = 0
        self.oscillatorFrequency = random.uniform(0.1, 10.0)
        self.oscillatorValue = 0.0
        self.randomNoiseSeed = random.randint(-1000, 1000)
        self.counterRandomNoise = 0
        self.randomNoiseFrequency = random.uniform(0.1, 10.0)
        self.randomNoiseValue = 0.0
        
    def AddNodeGene(self, newNodeGene : NodeGene):
        self.NodeGenes.append(newNodeGene)

    def AddConnectionGene(self, newConnectionGene : ConnectionGene):
        self.ConnectionGenes.append(newConnectionGene)

    def SetConnectionWeight(self, inNode : int, outNode : int, newWeight : float):
        for connectionGene in self.ConnectionGenes:
            if connectionGene.GetInNode() == inNode and connectionGene.GetOutNode() == outNode:
                connectionGene.SetWeight(newWeight)
                
    def MutateAddNode(self):
        if len(self.NodeGenes) > maxNodeGenes:
            return
        # get suitable connection genes that are enabled and non-recurrent
        suitableConnectionGenes = []
        for connectionGene in self.ConnectionGenes:
            if connectionGene.IsEnabled() == True and connectionGene.IsRecurrent() == False:
                suitableConnectionGenes.append(connectionGene)
        if not suitableConnectionGenes:
            return
        # get random suitable connection
        suitableConnectionGene = random.choice(suitableConnectionGenes)
        # get the in and out nodes of chosen connection
        inNodeGene = suitableConnectionGene.GetInNode()
        outNodeGene = suitableConnectionGene.GetOutNode()
        # disable original connection
        self.ConnectionGenes[suitableConnectionGene.GetInnovation()].Disable()
        # create new node to fit on top of chosen connection
        layerNumber = inNodeGene.GetLayerNumber() + 1
        newNodeGene = NodeGene(NetworkNodeType.HIDDEN, self.nodeInnovationCounter.GetNewInnovation(), layerNumber)
        # create connections in to and out from new node gene
        connectionGeneIntoNewNode = ConnectionGene(
            inNodeGene.GetNodeId(),
            newNodeGene.GetNodeId(),
            1.0,
            self.connectionInnovationCounter.GetNewInnovation(),
            True,
            False
        )
        connectionGeneOutofNewNode = ConnectionGene(
            newNodeGene.GetNodeId(),
            outNodeGene.GetNodeId(),
            suitableConnectionGene.GetWeight(),
            self.connectionInnovationCounter.GetNewInnovation(),
            True,
            False
        )
        # add to node and connection genes
        self.AddNodeGene(newNodeGene)
        self.AddConnectionGene(connectionGeneIntoNewNode)
        self.AddConnectionGene(connectionGeneOutofNewNode)
        # refresh the genome layer numbers of all node genes starting from input layer
        self.UpdateLayerNumbers()

    def MutateAddConnection(self):
        # get two random nodes in network representing the in and out nodes of the connection
        randomNodeGeneIn = random.choice(self.NodeGenes)
        randomNodeGeneOut = random.choice(self.NodeGenes)
        # return if connection is impossible
        if randomNodeGeneIn.GetType() == NetworkNodeType.OUTPUT:
            return
        if randomNodeGeneIn.GetType() == NetworkNodeType.INPUT and randomNodeGeneOut.GetType() == NetworkNodeType.INPUT:
            return
        # return if connection already exists
        connectionExists = False
        for connectionGene in self.ConnectionGenes:
            if connectionGene.GetInNode() == randomNodeGeneIn.GetNodeId() and connectionGene.GetOutNode() == randomNodeGeneOut.GetNodeId():
                connectionExists = True
                break
        if connectionExists:
            return
        # check if new connection is recurrent
        isRecurrent = False
        if randomNodeGeneIn.GetLayerNumber() > randomNodeGeneOut.GetLayerNumber():
            isRecurrent = True
        # if all tests are passed, create new connection gene
        newConnectionGene = ConnectionGene(
            randomNodeGeneIn.GetNodeId(),
            randomNodeGeneOut.GetNodeId(),
            random.uniform(minConnectionWeight, maxConnectionWeight),
            self.connectionInnovationCounter.GetNewInnovation(),
            True,
            isRecurrent
        )
        # add to connection genes
        self.AddConnectionGene(newConnectionGene)
        # refresh the genome layer numbers of all node genes starting from input layer
        self.UpdateLayerNumbers()
        
    def MutateConnectionWeight(self):
        # get enabled connection genes
        enabledConnectionGenes = []
        for connectionGene in self.ConnectionGenes:
            if connectionGene.IsEnabled():
                enabledConnectionGenes.append(connectionGene)
        if not enabledConnectionGenes:
            return # unable to find suitable connection to add node to
        # get random enabled connection in network
        enabledConnectionGene = random.choice(enabledConnectionGenes)
        # roll if weight should be perturbed or replaced
        roll = random.uniform(0.0, 1.0)
        if roll < perturbingProbability:
            newWeight = self.ConnectionGenes[enabledConnectionGene.GetInnovation()].GetWeight() + random.gauss(0.0, perturbingSigma)
            newWeight = ClampFloat(newWeight, minConnectionWeight, maxConnectionWeight)
            # perturbe weight with normal distribution
            self.onnectionGenes[enabledConnectionGene.GetInnovation()].SetWeight(newWeight)
        else: # set new random weight with uniform distribution
            self.ConnectionGenes[enabledConnectionGene.GetInnovation()].SetWeight(random.uniform(minConnectionWeight, maxConnectionWeight))

    def MutateEnableConnection(self):
        # get disabled connection genes
        disabledConnectionGenes = []
        for connectionGene in self.ConnectionGenes:
            if not connectionGene.IsEnabled():
                disabledConnectionGenes.append(connectionGene)
        if not disabledConnectionGenes:
            return # unable to find suitable connection to enable
        # get random enabled connection in network
        disabledConnectionGene = random.choice(disabledConnectionGenes)
        # enable connection in connection genes
        self.ConnectionGenes[disabledConnectionGene.GetInnovation()].Enable()
        # refresh the genome layer numbers of all node genes starting from input layer
        self.UpdateLayerNumbers()

    def MutateDisableConnection(self):
        # get enabled connection genes
        enabledConnectionGenes = []
        for connectionGene in self.ConnectionGenes:
            if connectionGene.IsEnabled():
                enabledConnectionGenes.append(connectionGene)
        if not enabledConnectionGenes:
            return # unable to find suitable connection to enable
        # get random enabled connection in network
        enabledConnectionGene = random.choice(enabledConnectionGenes)
        # enable connection in connection genes
        self.ConnectionGenes[enabledConnectionGene.GetInnovation()].Disable()
        # refresh the genome layer numbers of all node genes starting from input layer
        self.UpdateLayerNumbers()

    def UpdateLayerNumbers(self):
        # update the genome layer numbers of all node genes starting from input layer, always have to update for added node genes
        newLayerNumber = 0
        nextConnectionGenes = []
        nextConnectionGenesBuffer = []
        # initial next connections starting from input layer
        for connectionGene in self.ConnectionGenes:
            if connectionGene.IsEnabled() == True and connectionGene.IsRecurrent() == False:
                if self.NodeGenes[connectionGene.GetInNode()].GetNetworkNodeType() == NetworkNodeType.INPUT:
                    nextConnectionGenes.append(connectionGene)
        # loop over next connection genes until output layer is reached
        while len(nextConnectionGenes) > 0:
            for nextConnectionGene in nextConnectionGenes:
                if nextConnectionGene.IsEnabled() == True and nextConnectionGene.IsRecurrent() == False:
                    newLayerNumber = self.NodeGenes[nextConnectionGene.GetInNode()].GetLayerNumber() + 1
                    if self.NodeGenes[nextConnectionGene.GetOutNode()].GetLayerNumber() < newLayerNumber: # making sure layer number is set to the highest one
                        self.NodeGenes[nextConnectionGene.GetOutNode()].SetLayerNumber(newLayerNumber)
                    # if connection goes out to output node, dont check for next connection genes
                    if self.NodeGenes[nextConnectionGene.GetOutNode()].GetNetworkNodeType() == NetworkNodeType.OUTPUT:
                        continue
                    # get connection genes going out from each next connection gene into buffer
                    for outputConnectionGene in self.ConnectionGenes:
                        if outputConnectionGene.IsEnabled() == True and outputConnectionGene.IsRecurrent() == False:
                            if outputConnectionGene.GetInNode() == nextConnectionGene.GetOutNode():
                                nextConnectionGenesBuffer.append(outputConnectionGene)
            # switch with buffer
            nextConnectionGenes.clear()
            nextConnectionGenes = nextConnectionGenesBuffer
            nextConnectionGenesBuffer.clear()

    def MutateStats(self):
        roll = random.randint(1, self.n_mutateableParameters)
        if roll == 1:
            if self.isHerbivore == True:
                self.isHerbivore == False
                self.isCarnivore = True
            elif self.isCarnivore == True:
                self.isCarnivore == False
                self.isHerbivore = True
        elif roll == 2:
            self.healthShare += random.gauss(0.0, perturbingSigma)
            self.healthShare = ClampFloat(self.healthShare, 0.1, 10.0)
        elif roll == 3:
            self.attackShare += random.gauss(0.0, perturbingSigma)
            self.attackShare = ClampFloat(self.attackShare, 0.1, 10.0)
        elif roll == 4:
            self.speedShare += random.gauss(0.0, perturbingSigma)
            self.speedShare = ClampFloat(self.speedShare, 0.1, 10.0)
        elif roll == 5:
            self.size += self.size * random.gauss(0.0, 0.1)
            self.size = ClampFloat(self.size, 5.0, 30.0)
        elif roll == 6:
            self.biasValue += random.gauss(0.0, perturbingSigma)
            self.biasValue = ClampFloat(self.biasValue, -1.0, 1.0)
        elif roll == 7:
            self.oscillatorFrequency += random.gauss(0.0, perturbingSigma)
            self.oscillatorFrequency = ClampFloat(self.oscillatorFrequency, 0.1, 10.0)
        elif roll == 8:
            self.randomNoiseFrequency += random.gauss(0.0, perturbingSigma)
            self.randomNoiseFrequency = ClampFloat(self.randomNoiseFrequency, 0.1, 10.0)

    def SetFitnessAdjustment(self, fitnessAdjustment : float):
        self.fitness += fitnessAdjustment

    def SetGenomeId(self, newGenomeId : int):
        self.genomeId = newGenomeId

    def GetGenomeId(self):
        return self.genomeId

    def GetNodeGenes(self):
        return self.NodeGenes

    def GetConnectionGenes(self):
        return self.ConnectionGenes

    def GetFitness(self):
        return self.fitness