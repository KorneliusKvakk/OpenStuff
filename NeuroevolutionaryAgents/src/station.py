from configNeuroevolutionaryAgents import *

from part import *

class Station:
    def __init__(self,
        ID : int,
        position : pygame.Vector2):
        self.ID = ID
        self.position = position
        self.Parts = []
        self.NewPart()
        
    def NewPart(self):
        destinationId = self.ID
        while destinationId == self.ID:
            destinationId = random.randint(1, MAX_STATIONS)
        newPart = Part(destinationId, weight = random.uniform(MIN_PARTWEIGHT, MAX_PARTWEIGHT))
        self.Parts.append(newPart)

    def GeneratePart(self):
        roll = random.randint(1, MAXROLL_PART_GENERATION)
        if roll == 1:
            self.NewPart()

    def WithdrawPart(self):
        partToWithdraw = self.Parts[-1]
        del self.Parts[-1]

        return partToWithdraw