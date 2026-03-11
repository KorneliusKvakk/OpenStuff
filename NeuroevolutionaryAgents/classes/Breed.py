from configNeuroevolutionaryAgents import *

class Breed:
    def __init__(self, genome : Genome):
        self.Members = []
        self.Members.append(genome)
        self.mascot = genome
        self.champion = genome
        self.sharedFitness = 0.0

    def AddMember(self, newGenome : Genome):
        self.Members.append(newGenome)

    def UpdateChampion(self, newChampion : Genome):
        self.champion = newChampion

    def SetSharedFitnessAdjustment(self, sharedFitnessAdjustment : float):
        self.sharedFitness += sharedFitnessAdjustment