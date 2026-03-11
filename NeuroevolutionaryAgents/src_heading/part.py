from configNeuroevolutionaryAgents import *

class Part():
    def __init__(self,
        destinationId : int,
        weight : float):
        self.destinationId = destinationId
        self.weight = weight