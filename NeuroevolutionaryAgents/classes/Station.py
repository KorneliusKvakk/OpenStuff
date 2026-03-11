from configNeuroevolutionaryAgents import *

from Part import *

class Station:
    def __init__(self,
        id : int
        position : pygame.Vector2):
        self.id = id
        self.position = position
        self.Parts = []

    def GeneratePart(self):
        roll = random.randint(1, MAXROLL_PART_GENERATION)
        if roll == 1:
            newPart = Part(destinationId = random.randint(1, MAX_STATIONS), weight = random.uniform(MIN_PARTWEIGHT, MAX_PARTWEIGHT))
            self.Parts.append(newPart)

    def WithdrawPart(self):
        if len(self.Parts) > 0:
            partToWithdraw = self.Parts[0]
        del self.Parts[0]

        return partToWithdraw