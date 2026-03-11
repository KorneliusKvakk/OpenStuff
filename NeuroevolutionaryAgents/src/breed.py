from configNeuroevolutionaryAgents import *

from genome import *

class Breed:
    def __init__(self, genome : Genome):
        self.Genomes = []
        self.Genomes.append(genome)
        self.mascot = genome
        self.champion = genome
        self.sharedFitness = 0.0

    def AddGenome(self, newGenome : Genome):
        self.Genomes.append(newGenome)

    def UpdateChampion(self):
        for genome in self.Genomes:
            if genome.fitness > self.champion.fitness:
                self.champion = genome